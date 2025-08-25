# URL Shortener

A simple, efficient URL shortening service built with FastAPI and MongoDB.

## Live Deployment

- Production URL: https://src.archax.site/
- Interactive API Docs (Swagger UI): https://src.archax.site/docs
- Health Check: https://src.archax.site/health

## Features

- **URL Shortening**: Convert long URLs into short, easy-to-share links
- **Redirection**: Shortened URLs automatically redirect to original destinations
- **Analytics**: Track how many times each shortened URL has been accessed (stored as `count`)
- **IP Ownership**: The originating client IP is stored; only the creator's IP can update or delete
- **URL Management**: Update or delete existing short URLs
- **Static Frontend**: Simple UI served from `/static` at the root page
- **OpenAPI Docs**: Auto-generated docs at `/docs`

## Requirements

- Python 3.11+
- MongoDB instance (Atlas or self‑hosted)

## Environment Variables

Create a `.env` (NOT committed) or set variables in your hosting provider:

```
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>/<db>?retryWrites=true&w=majority
```

## Installation (Local)

```bash
git clone <repository-url>
cd urlShortner
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run locally (root main.py or api/main.py):
```bash
python main.py           # if using root file
# or
uvicorn api.main:app --reload
```
Default dev command here uses port 3030 in code; adjust with `--port` if needed.

Visit:
- App UI: http://localhost:3030/
- Docs: http://localhost:3030/docs
- Health: http://localhost:3030/health

## API Endpoints

### 1. Shorten a URL
`POST /shorten`
```json
{
  "url": "https://example.com/very/long/url"
}
```
Response:
```json
{
  "url": "http://localhost:3030/abc123de"
}
```
(HTTP 201)

### 2. Redirect
`GET /{uuid}`
Redirects (302) to original URL or returns custom 404 page.

### 3. Update a Short URL
`POST /update`
```json
{
  "uuid": "abc123de",
  "url": "https://new-destination.com"
}
```
Requires same creator IP as original.

### 4. Delete a Short URL
`GET /delete/{uuid}`
(Deletion via GET chosen for simplicity of the static frontend; in production prefer `DELETE /urls/{uuid}`.)

### 5. Health
`GET /health` → `{ "status": "ok" }`

### 6. Docs / Schema
- Swagger UI: `GET /docs`
- OpenAPI JSON: `GET /openapi.json`

## Example (Python requests)
```python
import requests
base = "http://localhost:3030"

r = requests.post(f"{base}/shorten", json={"url": "https://www.google.com"})
print(r.json())
short = r.json()["url"].rsplit('/', 1)[-1]

# Update
requests.post(f"{base}/update", json={"uuid": short, "url": "https://example.org"})
# Delete
requests.get(f"{base}/delete/{short}")
```

## Project Structure

- `api/main.py` – FastAPI app (Vercel entrypoint)
- `main.py` – Alternate local entry (can be removed if not used)
- `database/database.py` – MongoDB connection (Motor)
- `utils/utlis.py` – Helper for generating short IDs
- `static/` – Frontend HTML/CSS/JS + 404 page
- `test/` – Test script
- `config.py` – Legacy config (env handled via `os.getenv`)

## Deployment

### Vercel (Serverless)
1. Add `MONGO_URI` in Vercel Project Settings → Environment Variables (Production & Preview).
2. Ensure `vercel.json` points to `api/main.py`.
3. Push to main → Vercel builds and deploys.
4. Verify `/health` & `/docs`.

### Docker
A simple Dockerfile is included.
```bash
docker build -t url-shortener .
docker run -p 8000:8000 -e MONGO_URI=your_mongo_uri url-shortener
```
Visit http://localhost:8000/ and http://localhost:8000/docs

(If using `api/main.py` with Docker, adjust CMD to `uvicorn api.main:app`.)

## Security Notes
- IP-based ownership is a lightweight safeguard; for real auth integrate API keys or OAuth.
- Rotate credentials if `.env` was ever committed.
- Validate and sanitize user input if expanding feature set.

## Roadmap / Possible Improvements
- Custom aliases (user-defined short codes)
- Rate limiting per IP
- Expiration / TTL for links
- Real DELETE endpoint & auth tokens
- Basic analytics endpoint

## License

MIT License (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
