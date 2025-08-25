import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    mongo_uri = os.getenv("MONGO_URI")


