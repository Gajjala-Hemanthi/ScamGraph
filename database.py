import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(
    os.path.join(BASE_DIR, ".env"),
    override=True
)

URI = os.getenv("COGNODB_URI", "").strip()
USERNAME = os.getenv("COGNODB_USERNAME", "").strip()
PASSWORD = os.getenv("COGNODB_PASSWORD", "").strip()

print("URI starts with:", URI[:10])

if not URI:
    raise ValueError("COGNODB_URI is empty.")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)