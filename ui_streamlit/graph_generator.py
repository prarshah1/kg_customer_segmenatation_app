from dotenv import load_dotenv
load_dotenv()
from pyvis.network import Network
import streamlit as st
import base64
from neo4j import GraphDatabase
import networkx as nx
import json
from datetime import date, datetime
import ssl
import os
from dotenv import load_dotenv
from custom_json_encoder import CustomJSONEncoder
from descriptor import DatasetDescriptor
data_descriptions = DatasetDescriptor()
from streamlit_agraph import agraph, Node, Edge, Config


load_dotenv()

class GraphGenerator:
    def __init__(self):
        NEO4J_URI = os.getenv("NEO4J_URI")
        NEO4J_USER = os.getenv("NEO4J_USER")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
        ssl_context = ssl.create_default_context()
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def clean_neo4j_properties(self, props):
        cleaned = {}
        for key, value in props.items():
            if hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
                cleaned[key] = f"{value.year}-{value.month:02d}-{value.day:02d}"
            elif isinstance(value, (date, datetime)):
                cleaned[key] = value.isoformat()
            else:
                if isinstance(value, (str, int, float, bool, type(None))):
                    cleaned[key] = value
                else:
                    cleaned[key] = str(value)
        return cleaned


    def get_all_graph_data(self):
        with self.driver.session() as session:
            query = """
            MATCH (n)-[r]->(m)
            WITH n, r, m
            LIMIT 100
            RETURN collect(distinct n) as nodes, collect(distinct r) as rels, collect(distinct m) as targets
            """
            result = session.run(query).single()
            return self._create_networkx_graph(result)

    def get_schema_data(self):
        with self.driver.session() as session:
            result = session.run("CALL db.schema.visualization()").single()
            nodes = result["nodes"]
            relationships = result["relationships"]

            G = nx.DiGraph()

            for node in nodes:
                node_id = node.id
                node_labels = list(node.labels)
                node_props = self.clean_neo4j_properties(dict(node.items()))
                G.add_node(node_id,
                           label=node_labels[0],
                           title=json.dumps(node_props, cls=CustomJSONEncoder),
                           **node_props)

            for rel in relationships:
                source_id = rel.start_node.id
                target_id = rel.end_node.id
                rel_props = self.clean_neo4j_properties(dict(rel.items())) if rel.items() else {}
                G.add_edge(source_id,
                           target_id,
                           title=rel.type,
                           label=rel.type,
                           **rel_props)
            data_descriptions.set_dataset_counts(self.get_dataset_counts())
            return G

    def get_dataset_counts(self):
        with self.driver.session() as session:
            return session.run("""
                CALL db.labels() YIELD label
                CALL {
                    WITH label
                    MATCH (n)
                    WHERE label in labels(n)
                    RETURN count(n) as count
                }
                RETURN label, count
            """).data()

    def _create_networkx_graph(self, result):
        G = nx.MultiDiGraph()
        nodes = set()

        for node in result['nodes']:
            node_id = node.id
            node_labels = list(node.labels)
            node_props = self.clean_neo4j_properties(dict(node.items()))

            if node_id not in nodes:
                G.add_node(node_id,
                           label=node_labels[0],
                           title=json.dumps(node_props),
                           **node_props)
                nodes.add(node_id)

        for rel in result.get('rels', []):
            source_id = rel.start_node.id
            target_id = rel.end_node.id
            rel_props = self.clean_neo4j_properties(dict(rel.items())) if rel.items() else {}
            G.add_edge(source_id,
                       target_id,
                       key=rel.id,
                       title=rel.type,
                       label=rel.type,
                       type=rel.type,
                       **rel_props)

        for node in result.get('targets', []):
            node_id = node.id
            if node_id not in nodes:
                G.add_node(node_id,
                           label="",
                           title="",
                           **{})
                nodes.add(node_id)

        return G

    def get_image_b64(self, image_path):
        if image_path:
            try:
                with open(f"{os.getcwd()}/resources/icons/{image_path}", "rb") as img_file:
                    base64_image = "data:image/png;base64," + base64.b64encode(img_file.read()).decode()
                return base64_image
            except FileNotFoundError:
                st.error(f"Image file not found: {image_path}")
                return None
        return None

    def create_pyvis_html_for_segment(self, nx_graph, show_node_data=True):
        # Create Pyvis network with modified settings
        net = Network(height="750px",
                      width="100%",
                      bgcolor="#ffffff",
                      font_color="black",
                      directed=True)

        # Modified physics settings for increased node distance
        net.set_options("""
        {
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -100000,
                    "centralGravity": 0.1,
                    "springLength": 300,
                    "springConstant": 0.2,
                    "damping": 1
                },
                "maxVelocity": 50,
                "minVelocity": 0.1,
                "solver": "barnesHut",
                "stabilization": {
                    "enabled": true,
                    "iterations": 1000,
                    "updateInterval": 100,
                    "onlyDynamicEdges": false,
                    "fit": false
                }
            },
            "nodes": {
                "font": {
                    "align": "middle"
                }
            },
            "edges": {
                "smooth": false,
                "font": {
                    "size": 12,
                    "align": "middle",
                    "background": "#ffffff"
                },
                "arrowStrikethrough": false
            }
        }
        """)
        # Add nodes with different colors based on labels
        label_info = {
            'Individual': {'color': '#FF9999', 'image': "individual.png", 'value': "name"},
            'Economic': {'color': '#99FF99', 'image': "economic.png", 'value': "socio-economic_classification"},
            'Geographic': {'color': '#9999FF', 'image': "geographic.png", 'value': "state"},
            'Behavioral': {'color': '#FFFF99', 'image': "behavioral.png", 'value': "advertisement_response_rate"},
            'Psychographic': {'color': '#FF99FF', 'image': "psycographic.png", 'value': "risk_tolerance"},
            'DigitalEngagement': {'color': '#99FFFF', 'image': "digital.png", 'value': "internet_usage_frequency"},
            'Financial': {'color': '#FFB366', 'image': "financial_behavior.png", 'value': "credit_score"},
            'FamilyStructure': {'color': '#B366FF', 'image': "family_structure.png", 'value': "children_count"},
            'HealthWellness': {'color': '#66FFB3', 'image': "hospital.png", 'value': "fitness_level"},
            'Technology': {'color': '#66B3FF', 'image': "technology.png", 'value': "tech-savvy_level"},
            'Education': {'color': '#FFB366', 'image': "education.png", 'value': "education_level"},
            'Segment': {'color': '#B366FF', 'image': "segment.png", 'value': "name"},
        }

        # Convert NetworkX graph to Pyvis
        for node in nx_graph.nodes(data=True):
            node_id = node[0]
            node_data = node[1]
            label = node_data.get('label', '')
            color = label_info.get(label, '#B366FF')["color"]

            # Simplified node label
            display_name = str(node_data.get(label_info.get(label, 'Name')["value"], ''))

            label_value = f"{display_name}" if show_node_data else label
            net.add_node(node_id,
                         label=label_value,
                         title=node_data.get('title', ''),
                         shape="image",
                         image=self.get_image_b64(label_info.get(label)["image"]),
                         color=color)

        # Add edges with arrows and relationship names
        for edge in nx_graph.edges(data=True):
            relationship_name = edge[2].get('type', '') or edge[2].get('label', '')
            # Get edge direction from edge data
            direction = edge[2].get('direction', 'forward')
            from_node = edge[1] if direction == 'reverse' else edge[0]
            to_node = edge[0] if direction == 'reverse' else edge[1]

            net.add_edge(from_node,
                         to_node,
                         title=edge[2].get('title', ''),
                         label=relationship_name,  # Display relationship name on the arrow
                         physics=True,
                         length=300,  # Increased edge length
                         smooth=False  # Straight lines instead of curves
                         )

        # Save to a fixed location
        net.save_graph("segment_graph.html")
        return "segment_graph.html"

    # def get_segment_graph_data(self, segment_num):
    #     with self.driver.session() as session:
    #         query = f"""
    #         MATCH (d:Individual)-[dsr:BELONGS_TO]->(s:Segment), (d)-[r]->(m)
    #         WHERE s.Name = 'S{segment_num}'
    #         WITH d, r, m
    #         LIMIT 200
    #         RETURN collect(distinct d) as nodes, collect(distinct r) as rels, collect(distinct m) as targets
    #         """
    #         result = session.run(query).single()
    #         return self._create_networkx_graph(result)

    def get_segment_graph_data(self, segment_id):
        with self.driver.session() as session:
            query = f"""
            MATCH (d:Individual)-[dsr:BELONGS_TO]->(s:Segment), (d)-[r]->(m)
            WHERE s.Name = '{segment_id}'
            WITH d, r, m
            LIMIT 200
            RETURN collect(distinct d) + collect(distinct m) as nodes, collect(distinct r) as rels
            """
            result = session.run(query).single()
            nodes = result["nodes"]
            relationships = result["rels"]

            # Create NetworkX graph
            G = nx.DiGraph()  # Changed to DiGraph for directed relationships

            # Process nodes
            for node in nodes:
                node_id = node.id
                node_labels = list(node.labels)
                node_props = self.clean_neo4j_properties(dict(node.items()))
                G.add_node(node_id,
                           label=node_labels[0],
                           title=json.dumps(node_props, cls=CustomJSONEncoder),
                           **node_props)

            # Process relationships
            for rel in relationships:
                source_id = rel.start_node.id
                target_id = rel.end_node.id
                rel_props = self.clean_neo4j_properties(dict(rel.items())) if rel.items() else {}
                G.add_edge(source_id,
                           target_id,
                           title=rel.type,
                           label=rel.type,
                           **rel_props)

            # Create visualization
            return self.create_pyvis_html_for_segment(G)
