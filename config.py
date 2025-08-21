import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    mongo_uri = os.getenv("MONGO_URI")
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 3000))

