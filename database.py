import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

URI = os.getenv("COGNODB_URI", "").strip()
USERNAME = os.getenv("COGNODB_USERNAME", "cognodb").strip()
PASSWORD = os.getenv("COGNODB_PASSWORD", "").strip()


def get_driver():
    if not URI:
        raise ValueError("COGNODB_URI is missing. Add it to the .env file.")

    if not PASSWORD:
        raise ValueError("COGNODB_PASSWORD is missing. Add it to the .env file.")

    return GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )
