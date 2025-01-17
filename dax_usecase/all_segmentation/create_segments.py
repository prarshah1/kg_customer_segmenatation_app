from neo4j import GraphDatabase
import ssl
from dax_usecase import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Secure Neo4j connection with SSL
ssl_context = ssl.create_default_context()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# # MATCH (individual:Individual)-[:HAS_ECONOMIC]->(economic:Economic),
# #       (individual)-[:HAS_DIGITAL_ENGAGEMENT]->(digital_engagement:DigitalEngagement),
# #       (individual)-[:HAS_TECHNOLOGY]->(technology:Technology),
# #       (individual)-[:HAS_BEHAVIOR]->(behavioral:Behavioral)
# # WHERE individual.`age_range` = '18-24' OR individual.`age_range` = '25-34'
# #   AND economic.`Annual Income Range` = "Low"  // Filter by income range
# #   AND economic.`Wealth Index` <= 3  // Filter by wealth index
# #   AND digital_engagement.`Internet Usage Frequency` = "Daily"  // Filter by digital engagement
# #   AND technology.`Tech-Savvy Level` = "High"  // Filter by tech-savvy level
# # RETURN individual, economic, digital_engagement, technology, behavioral
# # Limit 30

# "age_range": random_choice(["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"], num_records),
# "marital_status": random_choice(["Single", "Married", "Divorced"], num_records),
# "Annual Income Range": random_choice(["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", ">$200k"],
# "Wealth Index": random_choice(["Low", "Medium", "High"], num_records),
# "Retirement Savings": random_choice(["<$50k", "$50k-$100k", "$100k-$200k", ">$200k"], num_records),
# "Attitudes Towards Technology": random_choice(["Enthusiastic", "Neutral", "Resistant"], num_records),
# "Internet Usage Frequency": random_choice(["Daily", "Weekly", "Occasionally"], num_records),
# "children_count": random_choice(["None", "1-2", "3-4", "5+"], num_records),



# Define the attributes
lifetages = ["Young", "Married Families", "Married Couples", "Divorced", "Empty Nesters", "Retirees"]
ages = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
digitals = ["Daily", "Weekly", "Occasionally"]

def get_lifestage_query(lifestage):
    if lifestage == "Young":
        return f'd.`marital_status` = "Single" AND fs.`children_count` = "None" and d.`age_range` in ["<18", "18-24", "25-34", "35-44"]'
    elif lifestage == "Married Families":
        return f'd.`marital_status` = "Married" AND fs.`children_count` in ["1-2", "3-4", "5+"] and d.`age_range` in ["18-24", "25-34", "35-44", "45-54"]'
    elif lifestage == "Married Couples":
        return f'd.`marital_status` = "Married" AND fs.`children_count` = "None" and d.`age_range` in ["18-24", "25-34", "35-44", "45-54"]'
    elif lifestage == "Divorced":
        return f'd.`marital_status` = "Divorced" AND d.`age_range` in ["18-24", "25-34", "35-44", "45-54"]'
    elif lifestage == "Empty Nesters":
        return f'fs.`children_count` = "None" AND d.`age_range` in [ "55-64"]'
    elif lifestage == "Retirees":
        return f'd.`age_range` = "65+" AND fs.`children_count` = "None"'
    return f"TRUE"


segments = []

# Create the nested loops to combine the categories
for lifestage in lifetages:
    for age in ages:
        for digital in digitals:
            if lifestage == "Retirees" and age != "65+":
                continue
            if lifestage == "Empty Nesters" and age not in ["55-64"]:
                continue
            if lifestage == "Married Families" and age not in ["18-24", "25-34", "35-44", "45-54"]:
                continue
            if lifestage == "Young" and age not in ["<18", "18-24", "25-34", "35-44"]:
                continue
            if lifestage == "Married Couples" and age not in ["18-24", "25-34", "35-44", "45-54"]:
                continue
            if lifestage == "Divorced" and age not in ["18-24", "25-34", "35-44", "45-54"]:
                continue

            # Create a segment name (can be more descriptive)
            segment_name = f"{lifestage.capitalize()} | Age: {age} | Digital: {digital}"
            query = f"""
                    MATCH (d:Individual)-[fsr:HAS_FAMILY_STRUCTURE]->(fs:FamilyStructure), (d)-[:HAS_DIGITAL_ENGAGEMENT]->(de:DigitalEngagement)
                    WHERE {get_lifestage_query(lifestage)} AND d.`age_range` = "{age}" AND de.`internet_usage_frequency` = '{digital}'
                    """
            # Store the segment name and query
            segments.append({"segment": segment_name, "query": query, "cluster_id": f"L{lifetages.index(lifestage) + 1}A{ages.index(age) + 1}D{digitals.index(digital)+1}"})

    # Print the generated segments and their corresponding queries
with driver.session() as session:
    for segment in segments:
        print(f"cluster_id: {segment['cluster_id']}")
        # session.run("Create (s:Segment {Name: '" + segment['cluster_id'] + "'}) Return s;")
        print(f"Segment: {segment['segment']}")
        # print(f"Cypher Query: {segment['query']}")
        print("-" * 80)
        query_with_segment = segment['query'] + """
                WITH d
                MERGE (s:Segment {Name: '""" + segment['cluster_id'] + """'})
                MERGE (d)-[:BELONGS_TO]->(s)  // Create relationship between individual and the segment
                RETURN d, s
                """
        session.run(query_with_segment)
        print(session.run(segment['query'] + """ Return COUNT(d)""").data())
driver.close()
