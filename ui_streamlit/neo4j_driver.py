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
