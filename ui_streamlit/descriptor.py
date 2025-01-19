import random
import streamlit as st
from matplotlib import pyplot as plt
import os
import pandas as pd
from neo4j_driver import get_query_results


class DatasetDescriptor:
    def __init__(self):
        # Create DatasetDescriptor instances for each dataset
        self.data_information = {
            "Segment": """
    <h2>Customer Segments</h2>

    <p>Segments are defined by a unique identifier created to segment individuals based on their life-stage, age, and digital engagement level, with the following format:</p>

    <p><strong>L {Lifestage Index} A {Age Index} D {Digital Engagement Index}</strong></p>

    <ul>
        <li><strong>Lifestage (L):</strong>   
            <span style='color:#5F9EA0;'>Young</span>, 
            <span style='color:#32CD32;'>Married Families</span>, 
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
    """,
    "Individual": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides detailed <b>individual</b> insights including attributes such as:
                <ul>
                    <li><b>Demographics:</b> Age range, gender, marital status</li>
                    <li><b>Education and Occupation:</b> Education level, occupation</li>
                    <li><b>Personal Details:</b> Ethnicity, language preferences, nationality</li>
                    <li><b>Other Attributes:</b> Geographic mobility, citizenship status, military service</li>
                </ul>
                Each individual is uniquely identified by their name and date of birth.
            </p>
        </div>
        """,
    "Economic": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides comprehensive <b>economic</b> insights including attributes such as:
                <ul>
                    <li><b>Income and Employment:</b> Annual income range, employment status, job title</li>
                    <li><b>Financial Details:</b> Property ownership, tax bracket, wealth index</li>
                    <li><b>Investment and Savings:</b> Investment types, retirement savings</li>
                    <li><b>Debt and Credit:</b> Debt levels, credit worthiness</li>
                </ul>
                Each record is categorized by socio-economic classification and affluence level.
            </p>
        </div>
        """,
    "Geographic": """
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
        """,
    "Behavioral": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides detailed <b>behavioral</b> insights including attributes such as:
                <ul>
                    <li><b>Shopping Habits:</b> Purchase history, product preferences, shopping frequency</li>
                    <li><b>Payment and Loyalty:</b> Payment methods, loyalty program enrollment</li>
                    <li><b>Engagement and Response:</b> Content engagement level, advertisement response rate</li>
                    <li><b>Other Attributes:</b> Cart abandonment rate, event participation</li>
                </ul>
                Each record reflects the consumer's interaction with products and services.
            </p>
        </div>
        """,
    "Psychographic": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides comprehensive <b>psychographic</b> insights including attributes such as:
                <ul>
                    <li><b>Lifestyle and Values:</b> Lifestyle preferences, personal values, social values orientation</li>
                    <li><b>Interests and Hobbies:</b> Hobbies, media consumption, travel preferences</li>
                    <li><b>Attitudes and Risk:</b> Attitudes towards technology, risk tolerance</li>
                    <li><b>Community and Culture:</b> Community involvement, cultural activities participation</li>
                </ul>
                Each record captures the psychological attributes influencing consumer behavior.
            </p>
        </div>
        """,
    "DigitalEngagement": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides detailed <b>digital engagement</b> insights including attributes such as:
                <ul>
                    <li><b>Internet and Device Usage:</b> Internet usage frequency, device preferences</li>
                    <li><b>Social Media and Apps:</b> Social media platforms, app usage patterns</li>
                    <li><b>Online Activities:</b> E-commerce activity, online content creation</li>
                    <li><b>Privacy and Communication:</b> Privacy settings used, digital communication channels</li>
                </ul>
                Each record reflects the individual's interaction with digital platforms and services.
            </p>
        </div>
        """,
    "Financial": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides comprehensive <b>financial</b> insights including attributes such as:
                <ul>
                    <li><b>Credit and Spending:</b> Credit score, spending patterns, credit card usage</li>
                    <li><b>Savings and Investments:</b> Savings account usage, investment portfolios</li>
                    <li><b>Loans and Insurance:</b> Loan information, insurance policies</li>
                    <li><b>Financial Planning:</b> Financial goals, budget adherence, tax planning strategies</li>
                </ul>
                Each record reflects the individual's financial behavior and planning.
            </p>
        </div>
        """,
    "FamilyStructure": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides detailed <b>family structure</b> insights including attributes such as:
                <ul>
                    <li><b>Family Composition:</b> Children count, family decision maker</li>
                    <li><b>Responsibilities and Habits:</b> Family responsibilities, family vacation habits</li>
                    <li><b>Household Dynamics:</b> Household chores arrangement, household technology usage</li>
                    <li><b>Communication and Traditions:</b> Family communication practices, family traditions</li>
                </ul>
                Each record captures the dynamics and structure of family units.
            </p>
        </div>
        """,
    "HealthWellness": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides comprehensive <b>health and wellness</b> insights including attributes such as:
                <ul>
                    <li><b>Health and Fitness:</b> Health insurance type, fitness level, dietary preferences</li>
                    <li><b>Medical and Wellness:</b> Medical condition monitoring, wellness program participation</li>
                    <li><b>Habits and Awareness:</b> Sleep habits, mental health awareness</li>
                    <li><b>Alternative Practices:</b> Alternative medicine use, stress management techniques</li>
                </ul>
                Each record reflects the individual's health and wellness practices.
            </p>
        </div>
        """,
    "Technology": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides detailed <b>technology adoption</b> insights including attributes such as:
                <ul>
                    <li><b>Purchase and Usage:</b> Technology purchase history, device usage patterns</li>
                    <li><b>Security and Preferences:</b> Online security measures, software use preferences</li>
                    <li><b>Support and Participation:</b> Tech support utilization, e-government participation</li>
                    <li><b>Emerging Trends:</b> Interest in emerging tech, tech event attendance</li>
                </ul>
                Each record reflects the individual's interaction with technology and adoption trends.
            </p>
        </div>
        """,
    "Education": """
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color:#4682B4; font-family:Arial, sans-serif;">Dataset Overview</h3>
            <p style="font-size:16px; color:#333; line-height:1.6;">
                This dataset provides comprehensive <b>education</b> insights including attributes such as:
                <ul>
                    <li><b>Level and Field:</b> Education level, field of study</li>
                    <li><b>Institution and Performance:</b> Institution type, academic performance</li>
                    <li><b>Engagement and Aid:</b> Online learning engagement, scholarships/financial aid</li>
                    <li><b>Continuing Education:</b> Continuing education, post-graduation education</li>
                </ul>
                Each record reflects the individual's educational background and pursuits.
            </p>
        </div>
        """
}

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
        # Fetch datasets and their descriptions
        # datasets = [
        #     {"name": "Individual", "description": self.individual},
        #     {"name": "Economic", "description": self.economic},
        #     {"name": "Geographic", "description": self.geographic},
        #     {"name": "Behavioral", "description": self.behavioral},
        #     {"name": "Psychographic", "description": self.psychographic},
        #     {"name": "DigitalEngagement", "description": self.digital_engagement},
        #     {"name": "Financial", "description": self.financial},
        #     {"name": "FamilyStructure", "description": self.family_structure},
        #     {"name": "HealthWellness", "description": self.health_wellness},
        #     {"name": "Technology", "description": self.technology},
        #     {"name": "Education", "description": self.education},
        #     {"name": "Segment", "description": self.segment}
        # ]

        # Create a dropdown for dataset selection
        if dataset_name is None:
            self.show_datasets_count_percentage(self.dataset_counts)
        elif dataset_name in self.datasets:
                self.generate_charts(dataset_name)
        else:
            st.write("Dataset name not present in knowledge graph")

            

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

    # def individual(self):
    #     import streamlit as st
    #     import pandas as pd
    #     import plotly.express as px
    #     st.header("Dataset: Individual")

    #     # Fetch data from Neo4j
    #     query = """
    #     MATCH (i:Individual) RETURN i.age_range AS age_range, i.gender AS Gender, 
    #     i.marital_status AS marital_status, i.education_level AS Education_Level, 
    #     i.household_size AS Household_Size, i.nationality AS Nationality, 
    #     i.occupation AS Occupation
    #     """
    #     result = get_query_results(query)
    #     data = pd.DataFrame(result)

    #     # Age Distribution
    #     st.write("**Age Distribution**")
    #     age_dist = data["age_range"].value_counts()
    #     st.bar_chart(age_dist)

    #     # Gender Distribution
    #     gender_fig = px.pie(data, names="Gender", title="Gender Distribution")
    #     st.plotly_chart(gender_fig)

    #     # Marital Status Distribution
    #     marital_status_counts = data["marital_status"].value_counts()
    #     marital_fig = px.bar(data, x=marital_status_counts.index,
    #                          y=marital_status_counts.values,
    #                          title="Marital Status Distribution")
    #     st.plotly_chart(marital_fig)

    #     # Education Level
    #     education_counts = data["Education_Level"].value_counts().reset_index()
    #     education_counts.columns = ['Education_Level', 'Count']
    #     education_fig = px.bar(education_counts, x='Education_Level',
    #                            y='Count',
    #                            title="Education Level Distribution")
    #     st.plotly_chart(education_fig)

    #     # Household Size
    #     household_counts = data["Household_Size"].value_counts().reset_index()
    #     household_counts.columns = ['Household_Size', 'Count']
    #     household_fig = px.bar(household_counts, x='Household_Size', y='Count', title="Household Size Distribution")
    #     st.plotly_chart(household_fig)

    #     # Drill-Down Charts (e.g., Occupation by Nationality)
    #     occupation_fig = px.bar(data, x="Nationality", color="Occupation", barmode="group",
    #                             title="Occupation by Nationality")
    #     st.plotly_chart(occupation_fig)


    # def economic(self):
    #     import plotly.express as px
    #     import streamlit as st

    #     # Fetch economic data from Neo4j
    #     query = """
    #     MATCH (e:Economic) RETURN e.annual_income_range AS Annual_Income_Range, 
    #     e.employment_status AS Employment_Status, e.job_title AS Job_Title, 
    #     e.industry AS Industry, e.property_ownership AS Property_Ownership, 
    #     e.socio_economic_classification AS Socio_Economic_Classification, 
    #     e.tax_bracket AS Tax_Bracket, e.wealth_index AS Wealth_Index, 
    #     e.debt_levels AS Debt_Levels, e.retirement_savings AS Retirement_Savings, 
    #     e.investment_types AS Investment_Types, e.household_expenses AS Household_Expenses, 
    #     e.credit_worthiness AS Credit_Worthiness, e.income_growth_rate AS Income_Growth_Rate, 
    #     e.employment_history AS Employment_History
    #     """
    #     result = get_query_results(query)
    #     data = pd.DataFrame(result)

    #     # Annual Income Range Distribution
    #     st.write("**Annual Income Range Distribution**")
    #     income_dist = data["Annual_Income_Range"].value_counts()
    #     st.bar_chart(income_dist)

    #     # Employment Status Distribution
    #     employment_fig = px.pie(data, names="Employment_Status", title="Employment Status Distribution")
    #     st.plotly_chart(employment_fig)

    #     # Job Title Distribution
    #     job_title_counts = data["Job_Title"].value_counts()
    #     job_title_fig = px.bar(data, x=job_title_counts.index, y=job_title_counts.values, title="Job Title Distribution")
    #     st.plotly_chart(job_title_fig)

    #     # Industry Distribution
    #     industry_counts = data["Industry"].value_counts().reset_index()
    #     industry_counts.columns = ['Industry', 'Count']
    #     industry_fig = px.bar(industry_counts, x='Industry', y='Count', title="Industry Distribution")
    #     st.plotly_chart(industry_fig)

    #     # Property Ownership Distribution
    #     property_counts = data["Property_Ownership"].value_counts().reset_index()
    #     property_counts.columns = ['Property_Ownership', 'Count']
    #     property_fig = px.bar(property_counts, x='Property_Ownership', y='Count', title="Property Ownership Distribution")
    #     st.plotly_chart(property_fig)

    #     return self.datasets[1]

    def display_map(self):
        import plotly.express as px
        import streamlit as st

        query = """
        match (i:Individual) - [:LOCATED_IN] -> (g:Geographic) return i, g.latitude, g.longitude
        """
        result = get_query_results(query)


        # Create a scatter mapbox plot using Plotly with additional hover information
        fig = px.scatter_mapbox(
            result,
            lat='g.latitude',
            lon='g.longitude',
            hover_name='i',
            hover_data={'i': True},  # Show additional info on hover
            height=500,
            zoom=5  # Set initial zoom level
        )

        # Update layout for mapbox with zoom enabled
        fig.update_layout(mapbox_style="open-street-map")

        # Display the plot in Streamlit with zoom controls
        st.plotly_chart(fig, use_container_width=True)


    # def behavioral(self):
    #     import plotly.express as px
    #     import streamlit as st

    #     # Query to fetch behavioral data from Neo4j
    #     query = """
    #     MATCH (b:Behavioral)
    #     RETURN b.purchase_history AS purchase_history,
    #            b.product_preferences AS product_preferences,
    #            b.brand_affinity AS brand_affinity,
    #            b.payment_methods AS payment_methods,
    #            b.channel_preferences AS channel_preferences,
    #            b.cart_abandonment_rate AS cart_abandonment_rate
    #     """
    #     result = get_query_results(query)

    #     # Convert result to DataFrame
    #     behavioral_df = pd.DataFrame(result)

    #     # Create charts for the 5 most important/most used attributes
    #     # Create a pie chart for cart abandonment rate
    #     cart_abandonment_counts = behavioral_df['cart_abandonment_rate'].value_counts().reset_index()
    #     cart_abandonment_counts.columns = ['Cart Abandonment Rate', 'Count']
    #     fig = px.pie(cart_abandonment_counts, names='Cart Abandonment Rate', values='Count', 
    #                  title="Cart Abandonment Rate Distribution")
    #     st.plotly_chart(fig)
    #     attributes = ["purchase_history", "product_preferences", "brand_affinity", "payment_methods", "channel_preferences"]
    #     for attribute in attributes:
    #         counts = behavioral_df[attribute].value_counts().reset_index()
    #         counts.columns = [attribute, 'Count']
    #         fig = px.bar(counts, x=attribute, y='Count', title=f"{attribute.replace('_', ' ').title()} Distribution")
    #         st.plotly_chart(fig)


    #     return self.datasets[3]

    # def psychographic(self):
    #     import plotly.express as px
    #     import streamlit as st

    #     # Query to fetch psychographic data from Neo4j
    #     query = """
    #     MATCH (p:Psychographic)
    #     RETURN p.lifestyle AS lifestyle,
    #            p.personality AS personality,
    #            p.values AS values,
    #            p.attitudes AS attitudes,
    #            p.interests AS interests
    #     """
    #     result = get_query_results(query)

    #     # Convert result to DataFrame
    #     psychographic_df = pd.DataFrame(result)

    #     # Create charts for the 5 most important/most used attributes
    #     attributes = ["lifestyle", "personality", "values", "attitudes", "interests"]
    #     for attribute in attributes:
    #         counts = psychographic_df[attribute].value_counts().reset_index()
    #         counts.columns = [attribute, 'Count']
    #         fig = px.bar(counts, x=attribute, y='Count', title=f"{attribute.replace('_', ' ').title()} Distribution")
    #         st.plotly_chart(fig)

    #     return self.datasets[4]

    # def digital_engagement(self):
    #     import plotly.express as px
    #     import streamlit as st

    #     # Query to fetch digital engagement data from Neo4j
    #     query = """
    #     MATCH (d:DigitalEngagement)
    #     RETURN d.internet_usage AS internet_usage,
    #            d.device_preferences AS device_preferences,
    #            d.social_media_usage AS social_media_usage,
    #            d.online_shopping AS online_shopping,
    #            d.streaming_services AS streaming_services
    #     """
    #     result = get_query_results(query)

    #     # Convert result to DataFrame
    #     digital_engagement_df = pd.DataFrame(result)

    #     # Create charts for the 5 most important/most used attributes
    #     attributes = ["internet_usage", "device_preferences", "social_media_usage", "online_shopping", "streaming_services"]
    #     for attribute in attributes:
    #         counts = digital_engagement_df[attribute].value_counts().reset_index()
    #         counts.columns = [attribute, 'Count']
    #         fig = px.bar(counts, x=attribute, y='Count', title=f"{attribute.replace('_', ' ').title()} Distribution")
    #         st.plotly_chart(fig)

    #     return self.datasets[5]

    
    def generate_charts(self, data_type):
        import plotly.express as px
        import random

        if data_type not in self.datasets:
            return

        st.markdown(self.data_information[data_type], unsafe_allow_html=True)

        if data_type == "Segment":
            return

        if data_type == "Geographic":
            self.display_map()

        # Define a query to fetch data from Neo4j based on the data_type
        query = f"""
        MATCH (n:{data_type})
        RETURN n
        """
        result = get_query_results(query)

        # Convert result to DataFrame
        data_df = pd.json_normalize(result, sep='_')

        # Iterate over properties in the DataFrame
        for column in data_df.columns:
            # Check if the property has less than 10 unique categories
            if isinstance(data_df[column].iloc[0], dict) or data_df[column].nunique() < 10:
                # Randomly choose between a pie chart and a bar chart
                chart_type = random.choice(['pie', 'bar'])

                if chart_type == 'pie':
                    fig = px.pie(data_df, names=column, title=f"{column.replace('_', ' ').title()[2:]} Distribution")
                else:
                    counts = data_df[column].value_counts().reset_index()
                    counts.columns = [column, 'Count']
                    fig = px.bar(counts, x=column, y='Count', title=f"{column.replace('_', ' ').title()[2:]} Distribution")
                fig.update_layout(width=500, height=400)
                # Plot the chart using Streamlit with a fixed width of 600
                st.plotly_chart(fig)
        return
        
