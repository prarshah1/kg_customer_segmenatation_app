import streamlit as st
import plotly.graph_objects as go
import math
from neo4j import GraphDatabase
import ssl
import os
from dotenv import load_dotenv
from graph_generator import GraphGenerator
from streamlit.components.v1 import html

load_dotenv()
graph_generator_obj = GraphGenerator()
import streamlit as st


def get_color_lifestyle(lifestyle_index):
    # lifestyle_index is between 1 to 6
    colors = {
        '1': '#ADD8E6',  # lightblue
        '2': '#90EE90',  # lightgreen
        '3': '#FFFFE0',  # lightyellow
        '4': '#AFEEEE',  # lightturquoise
        '5': '#FFB6C1',  # lightpink
        '6': '#E0FFFF'  # lightcyan
    }
    return colors.get(lifestyle_index, 'lightblue')  # Default to 'lightblue' if index is out of range


def get_size_digital(digital):
    # values are between 1 and 3
    size_mapping = {
        '1': 45,
        '2': 55,
        '3': 65
    }
    return size_mapping.get(digital, 60)  # Default to 40 if digital is out of range

def generate_segment_graph():
    st.session_state.segment_descriptions = {"L1A1D1": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: <18 | Digital: Daily"},
                        "L1A1D2": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: <18 | Digital: Weekly"},
                        "L1A1D3": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: <18 | Digital: Occasionally"},
                        "L1A2D1": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 18-24 | Digital: Daily"},
                        "L1A2D2": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 18-24 | Digital: Weekly"},
                        "L1A2D3": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 18-24 | Digital: Occasionally"},
                        "L1A3D1": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 25-34 | Digital: Daily"},
                        "L1A3D2": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 25-34 | Digital: Weekly"},
                        "L1A3D3": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 25-34 | Digital: Occasionally"},
                        "L1A4D1": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 35-44 | Digital: Daily"},
                        "L1A4D2": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 35-44 | Digital: Weekly"},
                        "L1A4D3": {
                            "desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 35-44 | Digital: Occasionally"},
                        "L2A2D1": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 18-24 | Digital: Daily"},
                        "L2A2D2": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 18-24 | Digital: Weekly"},
                        "L2A2D3": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 18-24 | Digital: Occasionally"},
                        "L2A3D1": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 25-34 | Digital: Daily"},
                        "L2A3D2": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 25-34 | Digital: Weekly"},
                        "L2A3D3": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 25-34 | Digital: Occasionally"},
                        "L2A4D1": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 35-44 | Digital: Daily"},
                        "L2A4D2": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 35-44 | Digital: Weekly"},
                        "L2A4D3": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 35-44 | Digital: Occasionally"},
                        "L2A5D1": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 45-54 | Digital: Daily"},
                        "L2A5D2": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 45-54 | Digital: Weekly"},
                        "L2A5D3": {
                            "desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 45-54 | Digital: Occasionally"},
                        "L3A2D1": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 18-24 | Digital: Daily"},
                        "L3A2D2": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 18-24 | Digital: Weekly"},
                        "L3A2D3": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 18-24 | Digital: Occasionally"},
                        "L3A3D1": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 25-34 | Digital: Daily"},
                        "L3A3D2": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 25-34 | Digital: Weekly"},
                        "L3A3D3": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 25-34 | Digital: Occasionally"},
                        "L3A4D1": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 35-44 | Digital: Daily"},
                        "L3A4D2": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 35-44 | Digital: Weekly"},
                        "L3A4D3": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 35-44 | Digital: Occasionally"},
                        "L3A5D1": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 45-54 | Digital: Daily"},
                        "L3A5D2": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 45-54 | Digital: Weekly"},
                        "L3A5D3": {
                            "desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 45-54 | Digital: Occasionally"},
                        "L4A2D1": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 18-24 | Digital: Daily"},
                        "L4A2D2": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 18-24 | Digital: Weekly"},
                        "L4A2D3": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 18-24 | Digital: Occasionally"},
                        "L4A3D1": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 25-34 | Digital: Daily"},
                        "L4A3D2": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 25-34 | Digital: Weekly"},
                        "L4A3D3": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 25-34 | Digital: Occasionally"},
                        "L4A4D1": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 35-44 | Digital: Daily"},
                        "L4A4D2": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 35-44 | Digital: Weekly"},
                        "L4A4D3": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 35-44 | Digital: Occasionally"},
                        "L4A5D1": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 45-54 | Digital: Daily"},
                        "L4A5D2": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 45-54 | Digital: Weekly"},
                        "L4A5D3": {
                            "desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 45-54 | Digital: Occasionally"},
                        "L5A6D1": {
                            "desc": "Lifestyle: Empty Nesters (Individuals without children, aged between 55 and 64) | Age: 55-64 | Digital: Daily"},
                        "L5A6D2": {
                            "desc": "Lifestyle: Empty Nesters (Individuals without children, aged between 55 and 64) | Age: 55-64 | Digital: Weekly"},
                        "L5A6D3": {
                            "desc": "Lifestyle: Empty Nesters (Individuals without children, aged between 55 and 64) | Age: 55-64 | Digital: Occasionally"},
                        "L6A7D1": {
                            "desc": "Lifestyle: Retirees (Individuals aged 65+ without children) | Age: 65+ | Digital: Daily"},
                        "L6A7D2": {
                            "desc": "Lifestyle: Retirees (Individuals aged 65+ without children) | Age: 65+ | Digital: Weekly"},
                        "L6A7D3": {
                            "desc": "Lifestyle: Retirees (Individuals aged 65+ without children) | Age: 65+ | Digital: Occasionally"},
                        }

    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    # Secure Neo4j connection with SSL
    ssl_context = ssl.create_default_context()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    segment_info = {}

    with driver.session() as session:
        for segment_name in st.session_state.segment_descriptions.keys():
            count_query = f"""
            MATCH (d:Individual)-[:BELONGS_TO]->(s:Segment {{Name: '{segment_name}'}}), (d)-[:HAS_DIGITAL_ENGAGEMENT]->(de:DigitalEngagement)
            RETURN count(s) AS count, apoc.agg.first(d.`age_range`) AS age, apoc.agg.first(de.`internet_usage_frequency`) AS digital
            """
            result = session.run(count_query)
            segment_info[segment_name] = result.data()[0]

    # Prepare data for bubble chart
    data = [math.ceil(math.log(x["count"])) for x in segment_info.values()]  # Use counts for bubble sizes
    labels = list(segment_info.keys())  # Use segment names for labels
    age_categories = [x["age"] for x in segment_info.values()]  # Use age categories
    digital_categories = [x["digital"] for x in segment_info.values()]  # Use digital engagement types
    # Generate positions for the bubbles to create a honeycomb pattern
    positions = []
    rows = 6  # Number of rows
    cols = 10  # Number of columns
    radius = 1.5  # Adjust bubble radius

    for row in range(rows):
        for col in range(cols):
            # Alternating x-position for honeycomb pattern (offset for odd rows)
            x_pos = col * 2 * radius
            if row % 2 == 1:  # Odd rows get an offset for staggered effect
                x_pos += radius
            y_pos = row * 2 * radius  # Regular vertical spacing
            positions.append((x_pos, y_pos))

    # Create the bubble chart using Plotly
    fig = go.Figure()

    for i, (x_pos, y_pos) in enumerate(positions):
        if i < len(labels):
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[y_pos],
                mode='markers+text',
                marker=dict(
                    size=get_size_digital(str(labels[i]).split("D")[1][:1]),  # Bubble size scaled by the count
                    color=get_color_lifestyle(str(labels[i]).split("L")[1][:1]),
                    opacity=0.8,
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                text=labels[i],
                textposition='middle center',  # Corrected the value here
                hoverinfo='text+name',
                name=labels[i]
            ))
            st.session_state.segment_descriptions[labels[i]]["x,y"] = f"{x_pos, y_pos}"

    # Customize the layout
    fig.update_layout(
        # dragmode='select',
        title="Customer Segments",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # Hide x-axis
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # Hide y-axis
        height=600,
        width=800
    )
    return fig


def display_segment_stats(segment_id):
    st.markdown("<strong><hr></strong>", unsafe_allow_html=True)
    image_path = f"{os.getcwd()}/resources/lifestyle/{segment_id[:2]}.png"
    st.markdown(
        f"<h5 style='color: #4A90E2; text-align: center;'>Segment Description</h5>",
        unsafe_allow_html=True)
    img_col, desc_col = st.columns([0.5, 0.5])
    with img_col:
        st.image(image_path)
    with desc_col:
        st.markdown(f"<p style='font-size: 16px;'><b>  <br><br><br> - {st.session_state.segment_descriptions[segment_id]['desc'].replace('|', '<br>   -')}</b></p>", unsafe_allow_html=True)

    # Define the query to get stats for the given segment_id
    query = f"""
    MATCH (d:Individual)-[:BELONGS_TO]->(s:Segment {{Name: '{segment_id}'}})
    OPTIONAL MATCH (d)-[:HAS_ECONOMIC]->(e:Economic)
    OPTIONAL MATCH (d)-[:HAS_DIGITAL_ENGAGEMENT]->(de:DigitalEngagement)
    OPTIONAL MATCH (d)-[:HAS_TECHNOLOGY]->(t:Technology)
    OPTIONAL MATCH (d)-[:HAS_BEHAVIOR]->(b:Behavioral)
    OPTIONAL MATCH (d)-[:HAS_PSYCHOGRAPHY]->(p:Psychographic)
    OPTIONAL MATCH (d)-[:HAS_HEALTH]->(h:HealthWellness)
    OPTIONAL MATCH (d)-[:LOCATED_IN]->(g:Geographic)
    OPTIONAL MATCH (d)-[:HAS_FAMILY_STRUCTURE]->(f:FamilyStructure)
    RETURN 
        d AS individual,
        e.annual_income_range AS `Annual Income Range`,
        de.`internet_usage_frequency` AS `Internet Usage`,
        t.`tech-savvy_level` AS `Tech Savvy`,
        b.advertisement_response_rate AS `Advertisement Response Rate`,
        b.shopping_frequency AS `Shopping Frequency`,
        p.media_consumption AS `Media Consumption`,
        p.hobbies AS `Hobbies`,
        h.fitness_level AS `Fitness Level`,
        g.state AS `State`,
        f.children_count AS `Children Count`,
        f.pet_ownership AS `Pet Ownership`
    """

    from neo4j_driver import get_query_results
    result = get_query_results(query)
    # Extract the data
    # st.write(result)


    # Collect distinct values for each attribute across all individuals
    from collections import Counter
    import plotly.express as px

    # Define the attributes to keep and their display logic
    attributes_to_keep = {
        "geographic_mobility": "max",
        "age_range": "max",
        "marital_status": "distinct",
        "Annual Income Range": "max",
        "Internet Usage": "max",
        "Shopping Frequency": "max",
        "Media Consumption": "distinct",
        "Hobbies": "distinct",
        "Fitness Level": "max",
        "State": "distinct",
        "Children Count": "distinct",
        "Pet Ownership": "max",
    }

    # Initialize distinct values
    distinct_values = {key: [] for key in attributes_to_keep.keys()}

    # Collect values for each attribute
    def convert_to_title(attribute):
        return ' '.join(word.capitalize() for word in attribute.split('_'))

    for entry in result:
        individual = entry["individual"]
        for key in distinct_values.keys():
            if key in individual:
                distinct_values[key].append(individual[key])
            elif key in entry:
                distinct_values[key].append(entry[key])

    # Display distinct values based on the specified logic
    markdown_output = ""
    markdown_output += "| Attribute | Value | Attribute | Value |\n"
    markdown_output += "|-----------|-------|-----------|-------|\n"

    attributes_list = list(distinct_values.items())
    for i in range(0, len(attributes_list), 2):
        attr1, values1 = attributes_list[i]
        display_attr1 = convert_to_title(attr1)
        if attributes_to_keep[attr1] == "max":
            most_common_value1 = Counter(values1).most_common(1)
            value1 = most_common_value1[0][0] if most_common_value1 else ""
        elif attributes_to_keep[attr1] == "distinct":
            value1 = ', '.join(sorted(set(values1)))

        if i + 1 < len(attributes_list):
            attr2, values2 = attributes_list[i + 1]
            display_attr2 = convert_to_title(attr2)
            if attributes_to_keep[attr2] == "max":
                most_common_value2 = Counter(values2).most_common(1)
                value2 = most_common_value2[0][0] if most_common_value2 else ""
            elif attributes_to_keep[attr2] == "distinct":
                value2 = ', '.join(sorted(set(values2)))
        else:
            display_attr2 = ""
            value2 = ""

        markdown_output += f"| **{display_attr1}** | {value1} | **{display_attr2}** | {value2} |\n"

    st.markdown(markdown_output)
    st.markdown("<strong><hr></strong>", unsafe_allow_html=True)

  
def display_segments():
    st.markdown("""
    <h2>Customer Segments</h2>

    <p>Segments are defined by a unique identifier created to segment individuals based on their life-stage, age, and digital engagement level, with the following format:</p>

    <p><strong>L {Lifestage Index} A {Age Index} D {Digital Engagement Index}</strong></p>

    <ul>
        <li><strong>Lifestage (L):</strong>   
            <span style='color:#5F9EA0;'>Young</span>, 
            <span style='color:#4682B4;'>Married Families</span>, 
            <span style='color:#BDB76B;'>Married Couples</span>, 
            <span style='color:#5F9EA0;'>Divorced</span>, 
            <span style='color:#CD5C5C;'>Empty Nesters</span>, 
            <span style='color:#B0E0E6;'>Retirees</span>
        </li>
        <li><strong>Age (A):</strong>   
            &lt; 18,&nbsp; 18-24,&nbsp; 25-34,&nbsp; 35-44,&nbsp; 45-54,&nbsp; 55-64,&nbsp; 65+
        </li>
        <li><strong>Digital Engagement (D):</strong>   
            Daily, Weekly, Occasionally
        </li>
    </ul>
    """, unsafe_allow_html=True)

    st.session_state.selected_segment = st.plotly_chart(st.session_state.fig, on_select="rerun")

    if st.session_state.selected_segment is not None:
        selected_point = st.session_state.selected_segment["selection"]["points"]
        if len(selected_point) > 0:
            with st.spinner('Loading graph data...'):
                x = float(selected_point[0]['x'])
                y = float(selected_point[0]['y'])
                segment_id = ""
                for key in st.session_state.segment_descriptions.keys():
                    if st.session_state.segment_descriptions[key]["x,y"] == f"{x, y}":
                        segment_id = key
                        st.session_state.selected_segment = key
                        break
                display_segment_stats(segment_id)
                html_file = graph_generator_obj.get_segment_graph_data(segment_id)
                # Display the graph
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_string = f.read()
                html(html_string, height=800)
