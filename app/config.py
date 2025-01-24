import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    PROPERTY_KEY = os.getenv("PROPERTY_KEY")
    PROPERTY_HOST = os.getenv("PROPERTY_HOST")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
