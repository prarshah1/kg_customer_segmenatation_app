import base64

from neo4j import GraphDatabase
import random
import ssl
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password")
BLOOM_URL = os.getenv("BLOOM_URL", "http://localhost:7475/browser/")

# Secure Neo4j connection with SSL
ssl_context = ssl.create_default_context()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def get_query_results(query):
    with driver.session() as session:
        result = session.run(query).data()
    return result

def get_image_b64(image_path):
    if image_path:
        try:
            with open(f"{os.getcwd()}/resources/icons/{image_path}", "rb") as img_file:
                base64_image = "data:image/png;base64," + base64.b64encode(img_file.read()).decode()
            return base64_image
        except FileNotFoundError:
            st.error(f"Image file not found: {image_path}")
            return None
    return None

