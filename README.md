# URL Shortener

A simple, efficient URL shortening service built with FastAPI and MongoDB.

## Features

- **URL Shortening**: Convert long URLs into short, easy-to-share links
- **Redirection**: Shortened URLs automatically redirect to original destinations
- **Analytics**: Track how many times each shortened URL has been accessed
- **IP Tracking**: Record the IP address of users who create shortened URLs
- **URL Management**:
  - Update the destination of shortened URLs
  - Delete shortened URLs when they're no longer needed
- **Security**: Only the creator of a URL (verified by IP) can modify it

## Requirements

- Python 3.6+
- FastAPI
- Uvicorn
- Motor (async MongoDB driver)
- Requests (for testing)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd urlShortner
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install fastapi uvicorn motor requests
   ```

4. Configure your MongoDB connection in `config.py`

## Usage

### Starting the Server

```
python main.py
```

This starts the server on http://localhost:3000 by default.

### API Endpoints

#### 1. Shorten a URL

```
POST /shorten
```

**Request body:**
```json
{
  "url": "https://example.com/very/long/url/that/needs/shortening"
}
```

**Response:**
```json
{
  "url": "http://localhost:3000/abc123de"
}
```

Note: URLs must start with http:// or https://

#### 2. Access a shortened URL

```
GET /{short_id}
```

This will redirect to the original URL.

#### 3. Update a URL's destination

```
POST /update
```

**Request body:**
```json
{
  "uuid": "abc123de",
  "url": "https://new-destination.com"
}
```

Only the original creator (verified by IP address) can update a URL.

#### 4. Delete a shortened URL

```
DELETE /del
```

**Request body:**
```json
{
  "url": "abc123de"
}
```

## Testing

The repository includes a `qwe.py` script that demonstrates how to interact with the API:

```python
import requests

# Create a shortened URL
response = requests.post(
    "http://localhost:3000/shorten",
    json={"url": "https://google.com"}
)
print("Full response:", response.text)

# Delete a shortened URL
response = requests.delete(
    "http://localhost:3000/del",
    json={"url": "abc123de"}
)
print("Full response:", response.text)

# Update a shortened URL
response = requests.post(
    "http://localhost:3000/update",
    json={
        "uuid": "abc123de",
        "url": "https://yahoo.com"
    }
)
print("Full response:", response.text)
```

## Code Structure

- **main.py**: Main application with FastAPI routes
- **config.py**: Configuration settings
- **database/database.py**: MongoDB connection setup
- **utils/utlis.py**: Utility functions (e.g., UUID shortening)
- **test/test.py**: Test scripts for the application
- **.env**: Environment variables (not tracked in git)
- **.gitignore**: Specifies intentionally untracked files
- **requirements.txt**: Project dependencies

## License

MIT License

Copyright (c) 2025

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
