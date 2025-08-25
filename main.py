import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database.database import collection
from utils.utlis import shorten_uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = FastAPI()


class URL(BaseModel):
    url: str


class UpdateURL(BaseModel):
    uuid: str
    url: str
    creator_ip: str = None

@app.post("/shorten")
async def root(request: Request, arg: URL):
    client_ip = request.client.host
    url = arg.url
    if not url.startswith(('http://', 'https://')):
        return JSONResponse(
        status_code=400,
        content={"error": "URL should start with http:// or https://"}
    )
    short = shorten_uuid()
    await collection.insert_one({"_id": short, "redirect": url, "count": 0, "creator_ip": client_ip})
    base_url = f"{request.url.scheme}://{request.url.netloc}"

    shortened_url = f"{base_url}/{short}"
    return JSONResponse(
        status_code=201,
        content={"url": shortened_url}
    )


@app.get("/{uuid}")
async def redirect(uuid: str):
    org_url = await collection.find_one({"_id": uuid})
    if org_url:
        url = org_url['redirect']
        await collection.update_one(
            {"_id": uuid},
            {"$inc": {"count": 1}}
        )
        return RedirectResponse(url=url, status_code=302)
    else:
        return FileResponse("static/404.html", status_code=404)



@app.get("/delete/{uuid}")
async def delete_url(request: Request, uuid: str):
    org_url = await collection.find_one({"_id": uuid})
    if not org_url:
        return JSONResponse(
            status_code=404,
            content={"detail": f"URL with ID '{uuid}' not found"}
        )

    if request.client.host != org_url.get('creator_ip'):
        return JSONResponse(
            status_code=403,
            content={"detail": "You are not authorized to delete this URL"}
        )

    await collection.delete_one({"_id": uuid})
    return JSONResponse(
        content={"detail": f"URL with ID '{uuid}' deleted"},
        status_code=200
    )

@app.post("/update")
async def update(request: Request, url: UpdateURL):
    org_url = await collection.find_one({"_id": url.uuid})
    if not org_url:
        return JSONResponse(
            status_code=404,
            content={"detail": f"URL with ID '{url.uuid}' not found"}
        )

    if request.client.host != org_url.get('creator_ip'):
        return JSONResponse(
            status_code=403,
            content={"detail": "You are not the creator of this URL"}
        )

    client_ip = request.client.host

    if not url.url.startswith(('http://', 'https://')):
        return JSONResponse(
            status_code=400,
            content={"error": "URL should start with http:// or https://"}
        )

    await collection.update_one(
        {"_id": url.uuid},
        {"$set": {"redirect": url.url, "creator_ip": client_ip}}
    )
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    shortened_url = f"{base_url}/{url.uuid}"
    return JSONResponse(
        status_code=200,
        content={"detail": f"URL with ID '{url.uuid}' updated", "url": shortened_url}
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.exception_handler(404)
async def custom_404_handler(request, exc):
    return FileResponse("static/404.html", status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3030, log_level="debug")
