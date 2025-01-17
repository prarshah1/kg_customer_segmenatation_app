import random
import streamlit as st
from matplotlib import pyplot as plt


class DatasetDescriptor:
    def __init__(self):
        # Create DatasetDescriptor instances for each dataset
        self.datasets = [
            "Individual",
            "Economic",
            "Geographic",
            "Behavioral",
            "Psychographic",
            "DigitalEngagement",
            "Financial",
            "FamilyStructure",
            "HealthWellness",
            "Technology",
            "Education",
            "Segment"
        ]
        self.dataset_counts = None
        return

    def set_dataset_counts(self, dataset_counts):
        self.dataset_counts = dataset_counts
    def show_dataset_description(self, dataset_name):
            # st.header(f"Dataset Description: {dataset_name}")
            # Fetch datasets and their descriptions
            datasets = [
                {"name": "Individual", "description": self.individual},
                {"name": "Economic", "description": self.economic},
                {"name": "Geographic", "description": self.geographic},
                {"name": "Behavioral", "description": self.behavioral},
                {"name": "Psychographic", "description": self.psychographic},
                {"name": "DigitalEngagement", "description": self.digital_engagement},
                {"name": "Financial", "description": self.financial},
                {"name": "FamilyStructure", "description": self.family_structure},
                {"name": "HealthWellness", "description": self.health_wellness},
                {"name": "Technology", "description": self.technology},
                {"name": "Education", "description": self.education},
                {"name": "Segment", "description": self.segment}
            ]

            # Create a dropdown for dataset selection
            if dataset_name == None:
                self.show_datasets_count_percentage(self.dataset_counts)
            else:
                dataset_names = [dataset["name"] for dataset in datasets]

            # Display the description of the selected dataset
            for dataset in datasets:
                if dataset["name"] == dataset_name:
                    # st.write(f"**Description:**")
                    dataset['description']()
                    break


    def show_datasets_count_percentage(self, label_counts):
        st.subheader("Dataset Counts")
        try:
            # Create a pie chart for segments with reduced size and fonts
            labels = [item['label'] if item["label"] != "Segment" else "" for item in label_counts]
            sizes = [item['count'] if item["label"] != "Segment" else "" for item in label_counts]
            labels.remove("")
            sizes.remove("")
            colors = plt.cm.Paired(range(len(labels)))

            fig, ax = plt.subplots(figsize=(3, 3))  # Reduced figure size
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=-100,
                   textprops={'fontsize': 5})  # Reduced font size
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig, use_container_width=False)

        except Exception as e:
            st.error(f"Error fetching graph statistics: {str(e)}")

    # Create a function for each dataset
    def individual(self):
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        st.header("Dataset: Individual")

        # Generate or load data
        data = pd.read_csv("dax_usecase/data/all_v1/Individual_Dataset.csv")

        # Age Distribution
        st.write("Age Distribution")
        age_dist = data["age_range"].value_counts()
        st.bar_chart(age_dist)

        # Gender Distribution
        st.subheader("Gender Distribution")
        gender_fig = px.pie(data, names="Gender", title="Gender Distribution")
        st.plotly_chart(gender_fig)

        # marital_status Distribution
        st.subheader("marital_status")
        marital_fig = px.bar(data, x=data["marital_status"].value_counts().index,
                             y=data["marital_status"].value_counts(),
                             title="marital_status Distribution")
        st.plotly_chart(marital_fig)

        # Education Level
        st.subheader("Education Level")
        education_fig = px.bar(data, x=data["Education Level"].value_counts().index,
                               y=data["Education Level"].value_counts(),
                               title="Education Level Distribution")
        st.plotly_chart(education_fig)

        # Household Size
        st.subheader("Household Size")
        household_fig = px.bar(data, x=data["Household Size"].value_counts().index,
                               y=data["Household Size"].value_counts(),
                               title="Household Size Distribution")
        st.plotly_chart(household_fig)

        # Filters for Exploration
        st.subheader("Filter Data")
        age_filter = st.multiselect("Select age_range", options=data["age_range"].unique())
        gender_filter = st.multiselect("Select Gender", options=data["Gender"].unique())

        filtered_data = data
        if age_filter:
            filtered_data = filtered_data[filtered_data["age_range"].isin(age_filter)]
        if gender_filter:
            filtered_data = filtered_data[filtered_data["Gender"].isin(gender_filter)]

        st.write(filtered_data)

        # Drill-Down Charts (e.g., Occupation by Nationality)
        st.subheader("Occupation by Nationality")
        occupation_fig = px.bar(filtered_data, x="Nationality", color="Occupation", barmode="group",
                                title="Occupation by Nationality")
        st.plotly_chart(occupation_fig)

        # Export Filtered Data
        st.download_button(
            label="Download Filtered Data",
            data=filtered_data.to_csv(index=False).encode("utf-8"),
            file_name="filtered_individual_data.csv",
            mime="text/csv"
        )

        # return self.datasets[0]

    def economic(self):
        return self.datasets[1]

    def geographic(self):
        import streamlit as st
        import plotly.express as px
        import pandas as pd
        import streamlit as st

        st.markdown("""
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides comprehensive <b>geographic</b> and <b>individual insights</b> across various cities in the USA. It includes attributes such as:
                <ul>
                    <li><b>Location details:</b> State, city, zip/postal code</li>
                    <li><b>Neighborhood characteristics:</b> Type, distance to urban centers, climate zone</li>
                    <li><b>Socioeconomic indicators:</b> School district quality, real estate values, employment opportunities</li>
                    <li><b>Environmental and community factors:</b> Proximity to public transport, local amenities, home density, crime rates, and hazards</li>
                </ul>
                Each city is also enriched with <b>latitude and longitude coordinates</b>, enabling geospatial analysis and visualization.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Assuming self.datasets[2] contains a list of dictionaries with 'latitude' and 'longitude' keys
        data = pd.DataFrame([
            {'name': f'Location {i}', 'latitude': 40.7128 - random.randint(-1, 1),
             'longitude': -74.0060 - 10 * random.randint(-1, 1)} for i in range(1, 80)
        ])

        # Create a scatter mapbox plot using Plotly with zoom enabled
        fig = px.scatter_mapbox(
            data,
            lat='latitude',
            lon='longitude',
            hover_name='name',
            height=500,
            zoom=5  # Set initial zoom level
        )

        # Update layout for mapbox with zoom enabled
        fig.update_layout(mapbox_style="open-street-map")

        # Display the plot in Streamlit with zoom controls
        st.plotly_chart(fig, use_container_width=True)

        return self.datasets[2]

    def behavioral(self):
        return self.datasets[3]

    def psychographic(self):
        return self.datasets[4]

    def digital_engagement(self):
        return self.datasets[5]

    def financial(self):
        return self.datasets[6]

    def family_structure(self):
        return self.datasets[7]

    def health_wellness(self):
        return self.datasets[8]

    def technology(self):
        return self.datasets[9]

    def education(self):
        return self.datasets[10]

    def segment(self):
        return self.datasets[11]
