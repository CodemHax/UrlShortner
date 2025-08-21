from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import logging
from utils.utlis import shorten_uuid
from database.database import collection

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
        return JSONResponse(
            status_code=404,
            content={"detail": f"URL with ID '{uuid}' not found"}
        )

@app.delete("/del")
async def delete(url : URL):
      del_link = url.url
      org_url = await collection.find_one({"_id": del_link})
      if org_url:
          await collection.delete_one({"_id": del_link})
          return JSONResponse(
              status_code=204
          )
      else:
          return JSONResponse(
              status_code=404,
              content={"detail": f"URL with ID '{del_link}' not found"}
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
# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=3000, log_level="debug")
