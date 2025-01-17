from pyspark.sql import SparkSession
from dax_usecase import NEO4J_URI, NEO4J_PASSWORD, NEO4J_USER
from pyspark.sql.functions import monotonically_increasing_id

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Neo4j Node Loader") \
    .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.3.2_for_spark_3") \
    .config("spark.neo4j.bolt.url", NEO4J_URI) \
    .config("spark.neo4j.bolt.user", NEO4J_USER) \
    .config("spark.neo4j.bolt.password", NEO4J_PASSWORD) \
    .getOrCreate()

data_dir_path = "dax_usecase/data/all_v1"

# Load and save each dataset as a node in Neo4j
datasets = [
    ("Individual", "/Individual_Dataset.csv"),
    ("Economic", "/Economic_Dataset.csv"),
    ("Geographic", "/Geographic_Dataset.csv"),
    ("Behavioral", "/Behavioral_Dataset.csv"),
    ("Psychographic", "/Psychographic_Dataset.csv"),
    ("DigitalEngagement", "/Digital_Engagement_Dataset.csv"),
    ("FamilyStructure", "/Family_Structure_Dataset.csv"),
    ("Financial", "/Financial_Behavior_Dataset.csv"),
    ("HealthWellness", "/Health_and_Wellness_Dataset.csv"),
    ("Technology", "/Technology_Adoption_Dataset.csv"),
    ("Education", "/Education_Dataset.csv")
]

for label, file_path in datasets:
    df = spark.read.csv(data_dir_path + file_path, header=True, inferSchema=True).withColumn("id", monotonically_increasing_id())
    df.write \
        .option("url", NEO4J_URI) \
        .option("user", NEO4J_USER) \
        .option("password", NEO4J_PASSWORD) \
        .option("authentication.basic.username", NEO4J_USER) \
        .option("authentication.basic.password", NEO4J_PASSWORD) \
        .option("node.keys", "id") \
        .format("org.neo4j.spark.DataSource") \
        .mode("Overwrite") \
        .option("node.keys", "id") \
        .option("labels", label) \
        .save()
