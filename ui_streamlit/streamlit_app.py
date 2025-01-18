import os
import time
import networkx as nx
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import base64

import streamlit as st
from streamlit_agraph import agraph, Config
from segment_graph import display_segments
from graph_generator import data_descriptions
from campaign import campaign_generation

if "G" not in st.session_state:
    from graph_generator import GraphGenerator
    graph_generator_obj = GraphGenerator()
    st.session_state.G = graph_generator_obj.get_schema_data()

if "id_label_mapping" not in st.session_state:
    st.session_state.id_label_mapping = {}

if "selected_segment" not in st.session_state:
    st.session_state.selected_segment = None

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

# Configure page settings
st.set_page_config(
    page_title="AXIS",
    page_icon="🔍",
    layout="wide"
)

# Sidebar navigation
st.sidebar.header("AXIS")
page_options = ["Dataset Visualization", "Consumer Segmentation", "Campaign Generator"]
page = st.sidebar.radio("", page_options)

# Show selected view
def show_schema_page():
    # Create the equivalent Node and Edge lists
    nodes = []
    edges = []
    config = Config(
        width=1000,
        height=800,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        node={'color': 'color', 'size': 'size', 'renderLabel': True, "fixed": False, "group": "graph_id", },
        link={'labelProperty': 'label', 'renderLabel': False, },
        collapsible=True,
        staticGraph=False,
        linkLength=290,  # Reduced link length for more compact layout
        gravity=-100,  # Increased negative gravity for better distribution
        physics=True,
        centralGravity=0.3,  # Reduced central gravity to allow more even distribution
        springLength=300,  # Reduced spring length for more compact layout
        springConstant=0.05,
        maxVelocity=50,
        minVelocity=0.01,
        solve="barnesHut",
        stabilization={
            "enabled": True,
            "iterations": 100,  # More iterations for better stabilization
            "updateInterval": 200,
            "onlyDynamicEdges": False,
            "fit": True,
        },
        nodes={
            "font": {
                "align": "below",
                "color": "#000000",
                "size": 12,
            },
            "fixed": False
        },
        edges={
            "smooth": False,
            "font": {
                "size": 10,
                "align": "center",
            },
            "length": 290,  # Adjusted edge length for better distribution
            "arrowStrikethrough": False,
            "arrows": {
                "to": {
                    "enabled": True,
                    "type": "arrow",
                    "scaleFactor": 1.2
                }
            }
        }
    )

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

    for node in st.session_state.G.nodes(data=True):
        node_id = node[0]
        node_data = node[1]
        label = node_data.get('label', '')
        color = label_info.get(label, {'color': '#B366FF'})["color"]

        # Simplified node label
        display_name = str(node_data.get(label_info[label]["value"] if False else 'name', ''))
        label_value = f"{display_name}" if False else label

        image_path = label_info.get(label, {}).get("image", None)
        image_b64 = get_image_b64(image_path) if image_path else None

        nodes.append(Node(id=node_id, label=label_value, color=color, shape="circularImage", image=image_b64,
                          renderLabel=True))
        st.session_state.id_label_mapping[node_id] = label_value

    for edge in st.session_state.G.edges(data=True):
        relationship_name = edge[2].get('type', '') or edge[2].get('label', '')
        direction = edge[2].get('direction', 'forward')
        from_node = edge[1] if direction == 'reverse' else edge[0]
        to_node = edge[0] if direction == 'reverse' else edge[1]

        edges.append(Edge(source=from_node, target=to_node, label=relationship_name))

    return_value = None

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    if return_value is None:
        data_descriptions.show_dataset_description(return_value)
    else:
        data_descriptions.show_dataset_description(st.session_state.id_label_mapping[return_value])

if page == page_options[0]:
    st.header("Dataset Visualization")
    show_schema_page()
elif page == page_options[1]:
    display_segments()
elif page == page_options[2]:
    campaign_generation()
else:
    st.write("Select from navigation")
