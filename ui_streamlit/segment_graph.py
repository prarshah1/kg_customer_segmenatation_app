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
segment_descriptions = {"L1A1D1": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: <18 | Digital: Daily"},
"L1A1D2": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: <18 | Digital: Weekly"},
"L1A1D3": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: <18 | Digital: Occasionally"},
"L1A2D1": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 18-24 | Digital: Daily"},
"L1A2D2": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 18-24 | Digital: Weekly"},
"L1A2D3": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 18-24 | Digital: Occasionally"},
"L1A3D1": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 25-34 | Digital: Daily"},
"L1A3D2": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 25-34 | Digital: Weekly"},
"L1A3D3": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 25-34 | Digital: Occasionally"},
"L1A4D1": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 35-44 | Digital: Daily"},
"L1A4D2": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 35-44 | Digital: Weekly"},
"L1A4D3": {"desc": "Lifestyle: Young (Single individuals without children, aged between <18 and 44) | Age: 35-44 | Digital: Occasionally"},
"L2A2D1": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 18-24 | Digital: Daily"},
"L2A2D2": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 18-24 | Digital: Weekly"},
"L2A2D3": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 18-24 | Digital: Occasionally"},
"L2A3D1": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 25-34 | Digital: Daily"},
"L2A3D2": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 25-34 | Digital: Weekly"},
"L2A3D3": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 25-34 | Digital: Occasionally"},
"L2A4D1": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 35-44 | Digital: Daily"},
"L2A4D2": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 35-44 | Digital: Weekly"},
"L2A4D3": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 35-44 | Digital: Occasionally"},
"L2A5D1": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 45-54 | Digital: Daily"},
"L2A5D2": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 45-54 | Digital: Weekly"},
"L2A5D3": {"desc": "Lifestyle: Married families (Married individuals with children, aged between 18 and 54) | Age: 45-54 | Digital: Occasionally"},
"L3A2D1": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 18-24 | Digital: Daily"},
"L3A2D2": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 18-24 | Digital: Weekly"},
"L3A2D3": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 18-24 | Digital: Occasionally"},
"L3A3D1": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 25-34 | Digital: Daily"},
"L3A3D2": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 25-34 | Digital: Weekly"},
"L3A3D3": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 25-34 | Digital: Occasionally"},
"L3A4D1": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 35-44 | Digital: Daily"},
"L3A4D2": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 35-44 | Digital: Weekly"},
"L3A4D3": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 35-44 | Digital: Occasionally"},
"L3A5D1": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 45-54 | Digital: Daily"},
"L3A5D2": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 45-54 | Digital: Weekly"},
"L3A5D3": {"desc": "Lifestyle: Married Couples (Married individuals without children, aged between 18 and 54) | Age: 45-54 | Digital: Occasionally"},
"L4A2D1": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 18-24 | Digital: Daily"},
"L4A2D2": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 18-24 | Digital: Weekly"},
"L4A2D3": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 18-24 | Digital: Occasionally"},
"L4A3D1": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 25-34 | Digital: Daily"},
"L4A3D2": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 25-34 | Digital: Weekly"},
"L4A3D3": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 25-34 | Digital: Occasionally"},
"L4A4D1": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 35-44 | Digital: Daily"},
"L4A4D2": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 35-44 | Digital: Weekly"},
"L4A4D3": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 35-44 | Digital: Occasionally"},
"L4A5D1": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 45-54 | Digital: Daily"},
"L4A5D2": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 45-54 | Digital: Weekly"},
"L4A5D3": {"desc": "Lifestyle: Divorced (Divorced individuals, aged between 18 and 54) | Age: 45-54 | Digital: Occasionally"},
"L5A6D1": {"desc": "Lifestyle: Empty Nesters (Individuals without children, aged between 55 and 64) | Age: 55-64 | Digital: Daily"},
"L5A6D2": {"desc": "Lifestyle: Empty Nesters (Individuals without children, aged between 55 and 64) | Age: 55-64 | Digital: Weekly"},
"L5A6D3": {"desc": "Lifestyle: Empty Nesters (Individuals without children, aged between 55 and 64) | Age: 55-64 | Digital: Occasionally"},
"L6A7D1": {"desc": "Lifestyle: Retirees (Individuals aged 65+ without children) | Age: 65+ | Digital: Daily"},
"L6A7D2": {"desc": "Lifestyle: Retirees (Individuals aged 65+ without children) | Age: 65+ | Digital: Weekly"},
"L6A7D3": {"desc": "Lifestyle: Retirees (Individuals aged 65+ without children) | Age: 65+ | Digital: Occasionally"},
}


def get_color_lifestyle(lifestyle_index):
    # lifestyle_index is between 1 to 6
    colors = {
        '1': '#ADD8E6',  # lightblue
        '2': '#90EE90',  # lightgreen
        '3': '#FFFFE0',  # lightyellow
        '4': '#AFEEEE',  # lightturquoise
        '5': '#FFB6C1',  # lightpink
        '6': '#E0FFFF'   # lightcyan
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


def display_segments():
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    # Secure Neo4j connection with SSL
    ssl_context = ssl.create_default_context()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    segment_info = {}

    with driver.session() as session:
        for segment_name in segment_descriptions.keys():
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
            segment_descriptions[labels[i]]["x,y"] = f"{x_pos,y_pos}"

    # Customize the layout
    fig.update_layout(
        # dragmode='select',
        title="Segment Bubble Chart",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # Hide x-axis
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # Hide y-axis
        height=600,
        width=800
    )
    fig_col, desc_col = st.columns([0.6, 0.4])
    with fig_col:
        st.session_state.selected_segment = st.plotly_chart(fig, on_select="rerun")
    with desc_col:
        st.markdown("""
        <h2>Segment ID</h2>

        <p>A unique identifier created to segment individuals based on their life-stage, age, and digital engagement level, with the following format:</p>

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
                &lt;18, 2. 18-24, 3. 25-34, 4. 35-44, 5. 45-54, 6. 55-64, 7. 65+
            </li>
            <li><strong>Digital Engagement (D):</strong>   
                Daily, Weekly, Occasionally
            </li>
        </ul>
        """, unsafe_allow_html=True)

    if st.session_state.selected_segment is not None:
        selected_point = st.session_state.selected_segment["selection"]["points"]
        if len(selected_point) > 0:
                with st.spinner('Loading graph data...'):
                    x = float(selected_point[0]['x'])
                    y = float(selected_point[0]['y'])
                    segment_id = ""
                    for key in segment_descriptions.keys():
                        if segment_descriptions[key]["x,y"] == f"{x,y}":
                            segment_id = key
                            break
                    st.markdown(f"<h5 style='color: #4A90E2;'>Segment Description:</h5><p style='font-size: 16px;'><b>   - {segment_descriptions[segment_id]['desc'].replace('|', '<br>   -')}</b></p>", unsafe_allow_html=True)
                    html_file = graph_generator_obj.get_segment_graph_data(segment_id)
                    # Display the graph
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_string = f.read()
                    html(html_string, height=800)
