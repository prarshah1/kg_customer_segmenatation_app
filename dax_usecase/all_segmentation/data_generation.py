import pandas as pd
import random
from faker import Faker
import pandas as pd
import random

# Initialize Faker for generating random data
fake = Faker()


# Generate individual data
def create_individual_data():
    num_records = 5000

    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    names = [
        "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", "Ivan", "Julia", "Kevin", "Laura",
        "Michael", "Nina", "Oscar", "Paula", "Quentin", "Rachel", "Samuel", "Tina", "Ursula", "Victor", "Wendy",
        "Xavier", "Yvonne", "Zack", "Amelia", "Benjamin", "Charlotte", "David", "Elena", "Frank", "Grace", "Harry",
        "Isabella", "Jack", "Karen", "Liam", "Mia", "Nathan", "Prarthana",
        "Olivia", "Peter", "Quincy", "Rebecca", "Sophia", "Thomas", "Uma", "Violet", "William", "Xena", "Yara", "Zane",
        "Aaron", "Bella", "Carter", "Daisy", "Ethan", "Faith", "Gabriel", "Harper",
        "Isaac", "Jade", "Kyle", "Lily", "Mason", "Nora", "Owen", "Piper", "Quinn", "Riley", "Sebastian", "Taylor",
        "Uriel", "Victoria", "Wyatt", "Ximena", "Yosef", "Zoey", "Adam", "Brooke", "Connor", "Delilah", "Elliot",
        "Felicity", "Gavin", "Hazel", "Ivy", "Jasper", "Kaitlyn", "Lucas", "PJ"
                                                                           "Anna", "Brandon", "Claire", "Derek",
        "Eleanor", "Finn", "Gianna", "Henry", "Isla", "Jacob", "Kylie", "Logan", "Madison", "Nicholas", "Olive",
        "Peyton", "Reed", "Sadie", "Theodore", "Ulysses", "Vivian", "Walker", "Xander", "Yvette", "Zara", "Aiden",
        "Blake", "Cecilia", "Dean", "Eve", "Flynn", "Gemma", "Hudson", "Iris", "Jordan", "Katherine", "Leah", "Miles",
        "Naomi", "Oliver", "Parker", "Quintin", "Rose", "Skylar", "Tanner", "Ulric", "Vanessa", "Warren", "Xenia",
        "Yasmin", "Zion", "Asher", "Brianna", "Colton", "Daphne", "Emmett", "Fiona", "Grayson", "Harley", "Ian",
        "Jamie", "Kennedy", "Landon", "Mila", "Noah", "Ophelia", "Paisley", "Quinton", "Ruby", "Sienna", "Tucker",
        "Uriah", "Veronica", "Wesley", "Xochitl", "Yvonne", "Zeke", "Ava", "Bryson", "Cameron", "Dakota", "Elias",
        "Felicity", "Gideon", "Harriet", "Imogen", "Julian", "Kayla", "Lincoln", "Maddox"
    ]

    individual_data = {
        "age_range": random_choice(["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"], num_records),
        "name": random_choice(names, num_records),
        "gender": random_choice(["Male", "Female", "Non-Binary"], num_records),
        "marital_status": random_choice(["Single", "Married", "Divorced"], num_records),
        "household_size": random_choice(["1", "2", "3-4", "5+"], num_records),
        "education_level": random_choice(["High School", "Undergraduate", "Postgraduate", "Doctorate"], num_records),
        "ethnicity": random_choice(["Caucasian", "African American", "Asian", "Hispanic", "Other"], num_records),
        "language_preferences": random_choice(["English", "Spanish", "French", "Mandarin", "Other"], num_records),
        "nationality": random_choice(["USA", "Canada", "UK", "India", "Australia"], num_records),
        "occupation": random_choice(["Professional", "Self-employed", "Retired", "Student"], num_records),
        "religion": random_choice(["Christianity", "Islam", "Hinduism", "Buddhism", "Atheism", "Other"], num_records),
        "date_of_birth": [fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d") for _ in
                          range(num_records)],
        "geographic_mobility": random_choice(["High", "Moderate", "Low"], num_records),
        "citizenship_status": random_choice(["Citizen", "Permanent Resident", "Work Visa", "Other"], num_records),
        "birthplace": random_choice(["Urban", "Rural", "Suburban"], num_records),
        "military_service": random_choice(["Yes", "No"], num_records),
    }

    # Convert to DataFrame
    individual_df = pd.DataFrame(individual_data)
    # Generate latitude and longitude

    # Save to CSV
    individual_df.to_csv(
        "dax_usecase/data/all_v1/Individual_Dataset.csv", index=False)

    print("Individual dataset created and saved as 'Individual_Dataset.csv'")


def create_economic_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate economic data
    economic_data = {
        "annual_income_range": random_choice(["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", ">$200k"],
                                             num_records),
        "employment_status": random_choice(["Employed", "Unemployed", "Part-time", "Freelancer"], num_records),
        "job_title": random_choice(["Manager", "Technician", "Clerk", "Consultant", "Other"], num_records),
        "industry": random_choice(["IT", "Healthcare", "Finance", "Education", "Other"], num_records),
        "property_ownership": random_choice(["Owner", "Renter", "Other"], num_records),
        "socio-economic_classification": random_choice(["Upper", "Upper-Middle", "Middle", "Lower-Middle", "Lower"],
                                                       num_records),
        "tax_bracket": random_choice(["<10%", "10-20%", "20-30%", "30-40%", "40%+"], num_records),
        "wealth_index": random_choice(["Low", "Medium", "High"], num_records),
        "debt_levels": random_choice(["No Debt", "Low Debt", "Moderate Debt", "High Debt"], num_records),
        "retirement_savings": random_choice(["<$50k", "$50k-$100k", "$100k-$200k", ">$200k"], num_records),
        "investment_types": random_choice(["Stocks", "Real Estate", "Mutual Funds", "Cryptocurrency", "None"],
                                          num_records),
        "household_expenses": random_choice(["<$1000", "$1000-$3000", "$3000-$5000", ">$5000"], num_records),
        "credit_worthiness": random_choice(["Excellent", "Good", "Fair", "Poor"], num_records),
        "income_growth_rate": random_choice(["Negative", "0-5%", "5-10%", "10%+"], num_records),
        "employment_history": random_choice(["Stable", "Frequent Changes", "Unstable"], num_records),
    }

    # Convert to DataFrame
    economic_df = pd.DataFrame(economic_data)

    # Function to categorize affluence based on Annual Income
    def get_affluence(income):
        if (income == "<$25k") or (income == "$50k-$100k"):
            return 'Low Affluence'
        elif 40000 == "$100k-$200k":
            return 'Medium Affluence'
        else:
            return 'High Affluence'

    # Apply the function to the 'Annual Income' column
    economic_df['affluence'] = economic_df['annual_income_range'].apply(get_affluence)

    # Save to CSV
    economic_df.to_csv("dax_usecase/data/all_v1/Economic_Dataset.csv",
                       index=False)

    print("Economic dataset created and saved as 'Economic_Dataset.csv'")


def create_geographic_data():
    bounding_boxes = {
        'Portland': {'min_lat': 30.4325, 'max_lat': 50.6529, 'min_lon': -115.8367, 'max_lon': -132.4722},
        'Salem': {'min_lat': 34.8897, 'max_lat': 54.9508, 'min_lon': -113.1209, 'max_lon': -132.9584},
        'Las Vegas': {'min_lat': 26.0119, 'max_lat': 46.2993, 'min_lon': -105.3161, 'max_lon': -124.9721},
        'Henderson': {'min_lat': 25.9786, 'max_lat': 46.1059, 'min_lon': -105.1645, 'max_lon': -124.9802},
        'Phoenix': {'min_lat': 23.2903, 'max_lat': 43.7487, 'min_lon': -102.3241, 'max_lon': -121.9280},
        'Tucson': {'min_lat': 22.0984, 'max_lat': 42.3050, 'min_lon': -101.0937, 'max_lon': -120.7353},
        'Salt Lake City': {'min_lat': 30.6995, 'max_lat': 50.8240, 'min_lon': -101.9611, 'max_lon': -121.7965},
        'West Valley City': {'min_lat': 30.6717, 'max_lat': 50.7285, 'min_lon': -102.0639, 'max_lon': -121.9436}
    }

    # Function to generate random coordinates within a bounding box
    def generate_coordinates(city):
        import random
        import time
        bbox = bounding_boxes[city]
        random.seed(time.time())
        lat = random.uniform(bbox['min_lat'], bbox['max_lat'])
        lon = random.uniform(bbox['min_lon'], bbox['max_lon'])
        return lat, lon

    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate geographic data
    geographic_data = {
        "country": ["USA"] * num_records,
        'state': random_choice(['Oregon', 'Oregon', 'Nevada', 'Nevada', 'Arizona', 'Arizona', 'Utah', 'Utah'],
                               num_records),
        'city': random_choice(['Portland', 'Salem', 'Las Vegas', 'Henderson', 'Phoenix', 'Tucson', 'Salt Lake City',
                               'West Valley City'], num_records),
        "zip/postal_code": [f"{random.randint(100, 999)}" for _ in range(num_records)],  # Random 5-digit zip codes
        "neighborhood_type": random_choice(["Urban", "Suburban", "Rural"], num_records),
        "distance_to_urban_centers": random_choice(["<5 km", "5-10 km", "10-20 km", "20+ km"], num_records),
        "climate_zone": random_choice(["Tropical", "Temperate", "Arid", "Polar"], num_records),
        "proximity_to_public_transport": random_choice(["High", "Moderate", "Low"], num_records),
        "local_amenities_access": random_choice(["High", "Moderate", "Low"], num_records),
        "home_density": random_choice(["High", "Medium", "Low"], num_records),
        "local_crime_rates": random_choice(["High", "Moderate", "Low"], num_records),
        "school_district_quality": random_choice(["Excellent", "Good", "Average", "Poor"], num_records),
        "real_estate_values": random_choice(["<$100k", "$100k-$300k", "$300k-$500k", ">$500k"], num_records),
        "environmental_hazards": random_choice(["None", "Low", "Moderate", "High"], num_records),
        "local_employment_opportunities": random_choice(["Excellent", "Good", "Fair", "Poor"], num_records),
    }

    # Convert to DataFrame
    geographic_df = pd.DataFrame(geographic_data)
    # Apply the function to each row
    geographic_df[['latitude', 'longitude']] = geographic_df['city'].apply(lambda x: pd.Series(generate_coordinates(x)))

    # Save to CSV
    geographic_df.to_csv("dax_usecase/data/all_v1/Geographic_Dataset.csv",
                         index=False)

    print("Geographic dataset created and saved as 'Geographic_Dataset.csv'")


def create_behavioral_data():
    # Number of records
    num_records = 1500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate behavioral data
    behavioral_data = {
        "purchase_history": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "product_preferences": random_choice(["Electronics", "Clothing", "Groceries", "Home Decor", "Books"],
                                             num_records),
        "brand_affinity": random_choice(["High", "Moderate", "Low"], num_records),
        "payment_methods": random_choice(["Credit Card", "Debit Card", "Cash", "Digital Wallet"], num_records),
        "channel_preferences": random_choice(["Online", "Offline", "Both"], num_records),
        "shopping_frequency": random_choice(["Daily", "Weekly", "Monthly", "Occasionally"], num_records),
        "average_purchase_value": random_choice(["<$50", "$50-$100", "$100-$500", ">$500"], num_records),
        "returned_items_frequency": random_choice(["High", "Moderate", "Low"], num_records),
        "loyalty_program_enrollment": random_choice(["Yes", "No"], num_records),
        "promotional_sensitivity": random_choice(["High", "Moderate", "Low"], num_records),
        "wishlist_activity": random_choice(["Active", "Inactive"], num_records),
        "cart_abandonment_rate": random_choice(["High", "Moderate", "Low"], num_records),
        "event_participation": random_choice(["Frequent", "Occasional", "Never"], num_records),
        "content_engagement_level": random_choice(["High", "Moderate", "Low"], num_records),
        "advertisement_response_rate": random_choice(["High", "Moderate", "Low"], num_records),
    }

    # Convert to DataFrame
    behavioral_df = pd.DataFrame(behavioral_data)

    # Save to CSV
    behavioral_df.to_csv("dax_usecase/data/all_v1/Behavioral_Dataset.csv",
                         index=False)

    print("Behavioral dataset created and saved as 'Behavioral_Dataset.csv'")


def create_psycographic_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate psychographic data
    psychographic_data = {
        "lifestyle_preferences": random_choice(["Active", "Sedentary", "Balanced"], num_records),
        "personal_values": random_choice(["Family", "Career", "Adventure", "Health", "Community"], num_records),
        "hobbies": random_choice(["Sports", "Reading", "Travel", "Gaming", "Cooking"], num_records),
        "media_consumption": random_choice(["TV", "Social Media", "News Websites", "Streaming", "Magazines"], num_records),
        "attitudes_towards_technology": random_choice(["Enthusiastic", "Neutral", "Resistant"], num_records),
        "risk_tolerance": random_choice(["High", "Moderate", "Low"], num_records),
        "social_values_orientation": random_choice(["Behavioralistic", "Collectivist"], num_records),
        "political_affiliation": random_choice(["Liberal", "Conservative", "Independent"], num_records),
        "community_involvement": random_choice(["Active", "Occasional", "Inactive"], num_records),
        "travel_preferences": random_choice(["Domestic", "International", "Adventure", "Luxury"], num_records),
        "cultural_activities_participation": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "leadership_propensity": random_choice(["High", "Moderate", "Low"], num_records),
        "charitable_activities": random_choice(["Frequent", "Occasional", "None"], num_records),
        "fashion_preferences": random_choice(["Trendy", "Classic", "Casual", "Minimalist"], num_records),
        "privacy_concerns": random_choice(["High", "Moderate", "Low"], num_records),
    }

    # Convert to DataFrame
    psychographic_df = pd.DataFrame(psychographic_data)

    # Save to CSV
    psychographic_df.to_csv(
        "dax_usecase/data/all_v1/Psychographic_Dataset.csv", index=False)
    print("Psychographic dataset created and saved as 'Psychographic_Dataset.csv'")


def create_digital_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate digital engagement data
    digital_engagement_data = {
        "internet_usage_frequency": random_choice(["Daily", "Weekly", "Occasionally"], num_records),
        "device_preferences": random_choice(["Smartphone", "Tablet", "Laptop", "Desktop"], num_records),
        "social_media_platforms": random_choice(["Facebook", "Twitter", "Instagram", "LinkedIn", "TikTok"], num_records),
        "website_types_visited": random_choice(["News", "E-commerce", "Entertainment", "Educational", "Social"], num_records),
        "app_usage_patterns": random_choice(["Frequent", "Moderate", "Rare"], num_records),
        "e-commerce_activity": random_choice(["High", "Moderate", "Low"], num_records),
        "digital_payment_usage": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "online_content_creation": random_choice(["Frequent", "Moderate", "None"], num_records),
        "newsletter_subscription": random_choice(["Yes", "No"], num_records),
        "online_forum_participation": random_choice(["Active", "Occasional", "None"], num_records),
        "privacy_settings_used": random_choice(["High", "Moderate", "Low"], num_records),
        "online_reviews_activity": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "live_streaming_engagement": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "online_spending_trends": random_choice(["<$50", "$50-$200", "$200-$500", ">$500"], num_records),
        "digital_communication_channels": random_choice(["Email", "Messaging Apps", "Video Calls", "Social Media"], num_records),
    }

    # Convert to DataFrame
    digital_engagement_df = pd.DataFrame(digital_engagement_data)

    # Save to CSV
    digital_engagement_df.to_csv(
        "dax_usecase/data/all_v1/Digital_Engagement_Dataset.csv",
        index=False)

    print("Digital Engagement dataset created and saved as 'Digital_Engagement_Dataset.csv'")


def create_financial_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate financial behavior data
    financial_behavior_data = {
        "credit_score": random_choice(["Excellent", "Good", "Fair", "Poor"], num_records),
        "spending_patterns": random_choice(["High", "Moderate", "Low"], num_records),
        "savings_account_usage": random_choice(["Frequent", "Occasional", "None"], num_records),
        "investment_portfolios": random_choice(["Stocks", "Bonds", "Real Estate", "Cryptocurrency", "None"], num_records),
        "loan_information": random_choice(["Yes", "No"], num_records),
        "mortgage_details": random_choice(["Yes", "No"], num_records),
        "credit_card_usage": random_choice(["High", "Moderate", "Low"], num_records),
        "insurance_policies": random_choice(["Health", "Life", "Car", "Home", "None"], num_records),
        "financial_goals": random_choice(["Retirement", "Buying a House", "Travel", "Education", "None"], num_records),
        "emergency_fund_status": random_choice(["Adequate", "Insufficient", "None"], num_records),
        "financial_planning_services": random_choice(["Yes", "No"], num_records),
        "budget_adherence": random_choice(["Excellent", "Good", "Fair", "Poor"], num_records),
        "debt_management_practices": random_choice(["Aggressive", "Moderate", "Conservative", "None"], num_records),
        "tax_planning_strategies": random_choice(["Yes", "No"], num_records),
        "charitable_contributions": random_choice(["Frequent", "Occasional", "None"], num_records),
    }

    # Convert to DataFrame
    financial_behavior_df = pd.DataFrame(financial_behavior_data)

    # Save to CSV
    financial_behavior_df.to_csv(
        "dax_usecase/data/all_v1/Financial_Behavior_Dataset.csv",
        index=False)

    print("Financial Behavior dataset created and saved as 'Financial_Behavior_Dataset.csv'")


def create_househould_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate family structure data
    family_structure_data = {
        "children_count": random_choice(["None", "1-2", "3-4", "5+"], num_records),
        "family_responsibilities": random_choice(["High", "Moderate", "Low"], num_records),
        "household_chores_arrangement": random_choice(["Shared", "Not Shared"], num_records),
        "pet_ownership": random_choice(["Yes", "No"], num_records),
        "family_decision_maker": random_choice(["Single", "Joint"], num_records),
        "family_vacation_habits": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "educational_priorities": random_choice(["High", "Moderate", "Low"], num_records),
        "work-life_balance_strategies": random_choice(["Balanced", "Flexible", "Strained"], num_records),
        "extended_family_proximity": random_choice(["Near", "Far", "None"], num_records),
        "family_traditions": random_choice(["Strong", "Moderate", "None"], num_records),
        "childcare_preferences": random_choice(["Daycare", "Stay-at-home", "Relative", "Nanny", "None"], num_records),
        "household_technology_usage": random_choice(["High", "Moderate", "Low"], num_records),
        "elder_care_involvement": random_choice(["High", "Moderate", "Low"], num_records),
        "family_communication_practices": random_choice(["Frequent", "Occasional", "Rare"], num_records),
        "household_media_consumption": random_choice(["High", "Moderate", "Low"], num_records),
    }

    # Convert to DataFrame
    family_structure_df = pd.DataFrame(family_structure_data)

    # Save to CSV
    family_structure_df.to_csv(
        "dax_usecase/data/all_v1/Family_Structure_Dataset.csv",
        index=False)

    print("Family Structure dataset created and saved as 'Family_Structure_Dataset.csv'")


def create_health_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate health and wellness data
    health_and_wellness_data = {
        "health_insurance_type": random_choice(["Private", "Public", "None"], num_records),
        "fitness_level": random_choice(["High", "Moderate", "Low"], num_records),
        "dietary_preferences": random_choice(["Vegetarian", "Vegan", "Non-Vegetarian", "Gluten-Free", "Other"],
                                             num_records),
        "medical_condition_monitoring": random_choice(["Frequent", "Occasional", "Rare", "None"], num_records),
        "health_product_usage": random_choice(["Frequent", "Occasional", "None"], num_records),
        "doctor_visit_frequency": random_choice(["Frequent", "Occasional", "Rare", "Never"], num_records),
        "health_supplement_intake": random_choice(["Frequent", "Occasional", "None"], num_records),
        "wellness_program_participation": random_choice(["Yes", "No"], num_records),
        "alternative_medicine_use": random_choice(["Frequent", "Occasional", "None"], num_records),
        "sleep_habits": random_choice(["Good", "Moderate", "Poor"], num_records),
        "stress_management_techniques": random_choice(["Exercise", "Meditation", "Therapy", "None"], num_records),
        "fitness_memberships": random_choice(["Yes", "No"], num_records),
        "medical_emergency_preparation": random_choice(["Yes", "No"], num_records),
        "health_screenings_regularity": random_choice(["Annual", "Occasional", "None"], num_records),
        "mental_health_awareness": random_choice(["High", "Moderate", "Low"], num_records),
    }
    # Convert to DataFrame
    health_and_wellness_df = pd.DataFrame(health_and_wellness_data)

    # Save to CSV
    health_and_wellness_df.to_csv(
        "dax_usecase/data/all_v1/Health_and_Wellness_Dataset.csv",
        index=False)

    print("Health and Wellness dataset created and saved as 'Health_and_Wellness_Dataset.csv'")


def create_technology_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate technology adoption data
    technology_adoption_data = {
        "technology_purchase_history": random_choice(["Frequent", "Occasional", "Rare", "None"], num_records),
        "device_usage_patterns": random_choice(["Smartphone", "Tablet", "Laptop", "Desktop"], num_records),
        "tech-savvy_level": random_choice(["High", "Moderate", "Low"], num_records),
        "online_security_measures": random_choice(["Strong", "Moderate", "Weak", "None"], num_records),
        "software_use_preferences": random_choice(["Open Source", "Proprietary", "Mixed"], num_records),
        "smart_home_devices_adopted": random_choice(["Yes", "No"], num_records),
        "diy_vs._professional_tech_use": random_choice(["DIY", "Professional", "Mixed"], num_records),
        "tech_support_utilization": random_choice(["Frequent", "Occasional", "None"], num_records),
        "interest_in_emerging_tech": random_choice(["High", "Moderate", "Low"], num_records),
        "e-government_participation": random_choice(["Yes", "No"], num_records),
        "digital_literacy_assessment": random_choice(["High", "Moderate", "Low"], num_records),
        "open_source_vs._proprietary_preferences": random_choice(["Open Source", "Proprietary", "Mixed"], num_records),
        "cloud_service_usage": random_choice(["Frequent", "Occasional", "None"], num_records),
        "online_subscription_services": random_choice(["Yes", "No"], num_records),
        "tech_event_attendance": random_choice(["Frequent", "Occasional", "None"], num_records),
    }

    # Convert to DataFrame
    technology_adoption_df = pd.DataFrame(technology_adoption_data)

    # Save to CSV
    technology_adoption_df.to_csv(
        "dax_usecase/data/all_v1/Technology_Adoption_Dataset.csv",
        index=False)

    print("Technology Adoption dataset created and saved as 'Technology_Adoption_Dataset.csv'")


def create_education_data():
    # Number of records
    num_records = 500

    # Helper function to generate random choices
    def random_choice(options, size):
        return [random.choice(options) for _ in range(size)]

    # Generate education data
    education_data = {
        "education_level": random_choice(
            ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "Doctorate", "None"],
            num_records),
        "field_of_study": random_choice(
            ["Engineering", "Health Sciences", "Business", "Arts", "Humanities", "Social Sciences", "Technology",
             "Other"], num_records),
        "institution_type": random_choice(["Public", "Private", "Online", "Vocational"], num_records),
        "graduation_year": random_choice([str(year) for year in range(2000, 2026)], num_records),
        "current_enrollment": random_choice(["Yes", "No"], num_records),
        "academic_performance": random_choice(["Excellent", "Good", "Average", "Below Average", "Not Applicable"],
                                              num_records),
        "continuing_education": random_choice(["Yes", "No"], num_records),
        "post-graduation_education": random_choice(["Pursuing Post-graduate", "Completed Post-graduate", "None"],
                                                   num_records),
        "scholarships/financial_aid": random_choice(["Yes", "No"], num_records),
        "online_learning_engagement": random_choice(["Frequent", "Occasional", "Rare", "None"], num_records),
    }

    # Convert to DataFrame
    education_df = pd.DataFrame(education_data)

    # Save to CSV
    education_df.to_csv("dax_usecase/data/all_v1/Education_Dataset.csv",
                        index=False)

    print("Education dataset created and saved as 'Education_Dataset.csv'")


create_individual_data()
create_economic_data()
create_geographic_data()
create_behavioral_data()
create_psycographic_data()
create_digital_data()
create_financial_data()
create_househould_data()
create_health_data()
create_technology_data()
create_education_data()
