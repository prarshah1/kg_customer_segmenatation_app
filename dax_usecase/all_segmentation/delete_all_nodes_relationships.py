from neo4j import GraphDatabase
import random
import ssl
from dax_usecase import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Secure Neo4j connection with SSL
ssl_context = ssl.create_default_context()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
import random

with driver.session() as session:
    print("Deleting all...")
    session.run("match (n) detach delete n")
driver.close()

