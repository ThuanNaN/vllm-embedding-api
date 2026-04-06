import os

from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv("API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "BAAI/bge-small-en")
