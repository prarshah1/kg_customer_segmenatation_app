import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import ssl
import streamlit as st
from neo4j_graphrag.retrievers import Text2CypherRetriever
from streamlit_agraph import agraph, Node, Edge, Config

load_dotenv()

NEO4J_URI = "neo4j+ssc://6322fba3.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "kIiqS9f1fDgsLmmwRLsV7sQ0d9aBFITQuB6V7UbEVnc"

# Secure Neo4j connection with SSL
ssl_context = ssl.create_default_context()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Configuration for agraph
config = Config(
    width=500,
    height=500,
    directed=True,
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    collapsible=True,
    node={'labelProperty': 'label'},
    link={'labelProperty': 'label', 'renderLabel': True}
)

from neo4j_graphrag.llm import LLMInterface
from neo4j_graphrag.llm import OpenAILLM


def nl_to_cypher(query):
    # Create LLM object
    t2c_llm = OpenAILLM(model_name="gpt-3.5-turbo", api_key=st.secrets["OPENAI_API_KEY"])

    retriever = Text2CypherRetriever(
        driver=driver,
        llm=t2c_llm
    )
    cypher_query = retriever.search(query_text=query)
    return cypher_query


def expand_node(node_id):
    cypher_query = f"MATCH (n)-[r]-(m) WHERE id(n) = {node_id} RETURN n, r"
    with driver.session() as session:
        result = session.run(cypher_query)
        nodes = []
        edges = []
        for record in result:
            n, r, m = record["n"], record["r"], record["m"]
            nodes.append(Node(id=n.id, label=n["name"], size=20))
            nodes.append(Node(id=m.id, label=m["name"], size=20))
            edges.append(Edge(source=n.id, target=m.id, type="CURVE_SMOOTH"))
    return nodes, edges


# Streamlit UI
st.title("Natural Language to Cypher Graph Viewer")

if "nl_query" not in st.session_state:
    st.session_state.nl_query = None


def generate_graph():
    if st.session_state.nl_query:
        cypher_query = nl_to_cypher(st.session_state.nl_query).metadata.get("cypher", "")
        st.write("Generated Cypher Query:", cypher_query)
        # with driver.session() as session:
        #     result = session.run(cypher_query)
        #     nodes = []
        #     edges = []
        #     for record in result:
        #         n, r, m = record["n"], record["r"], record["m"]
        #         nodes.append(Node(id=n.id, label=n["name"], size=20))
        #         nodes.append(Node(id=m.id, label=m["name"], size=20))
        #         edges.append(Edge(source=n.id, target=m.id, type="CURVE_SMOOTH"))
        # return_value = agraph(nodes=nodes, edges=edges, config=config)
        #
        # if return_value and 'node' in return_value:
        #     clicked_node_id = return_value['node']
        #     st.write(f"Node {clicked_node_id} clicked. Expanding...")
        #     new_nodes, new_edges = expand_node(clicked_node_id)
        #     nodes.extend(new_nodes)
        #     edges.extend(new_edges)
        #     agraph(nodes=nodes, edges=edges, config=config)


st.session_state.nl_query = st.text_input("Enter your query:", "")
st.button("Generate Graph", on_click=generate_graph)
