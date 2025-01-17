from neo4j import GraphDatabase
import ssl
from dax_usecase import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import random
# Secure Neo4j connection with SSL
ssl_context = ssl.create_default_context()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# Generate random ID mapping for other node types
relationship_queries = []


# Function to create relationships with random ID ranges
def generate_relationship_query(node_label, relationship_type):
    query = f"""
            MATCH (a: Individual), (b: {node_label})
            WITH a, collect(b) AS allBs
            WITH a, allBs[toInteger(rand() * size(allBs))] AS randomB
            MERGE (a)-[:{relationship_type}]->(randomB);
        """

    # for individual_id in range(1, individual_id_range + 1):
    #     random_id = random.randint(1, 100)
    #     f"MATCH (d:Individual {{id: {individual_id}}}), ({node_label.lower()}:{node_label} {{id: {random_id}}}) " \
    #             f"MERGE (d)-[:{}]->({node_label.lower()});"
    relationship_queries.append(query)


# Generate all relationship queries
generate_relationship_query("Economic", "HAS_ECONOMIC")
generate_relationship_query("Geographic", "LOCATED_IN")
generate_relationship_query("Behavioral", "HAS_BEHAVIOR")
generate_relationship_query("Psychographic", "HAS_PSYCHOGRAPHY")
generate_relationship_query("DigitalEngagement", "HAS_DIGITAL_ENGAGEMENT")
generate_relationship_query("FamilyStructure", "HAS_FAMILY_STRUCTURE")
generate_relationship_query("Financial", "HAS_FINANCIAL")
generate_relationship_query("HealthWellness", "HAS_HEALTH")
generate_relationship_query("Technology", "HAS_TECHNOLOGY")
generate_relationship_query("Education", "HAS_EDUCATION")

with driver.session() as session:
    print("Adding relationships...")
    for query in relationship_queries:
        session.run(query)

driver.close()
