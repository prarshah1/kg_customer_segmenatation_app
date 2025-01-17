class SchemaMetadata:
    METADATA = {
        'Individual': {
            'description': 'Basic individual information about behaviorals',
            'properties': {
                'Age': {'range': '18-80', 'description': 'Age of the behavioral'},
                'Gender': {'values': ['Male', 'Female', 'Non-binary'], 'description': 'Gender identity'},
                'Marital_Status': {'values': ['Single', 'Married', 'Divorced'], 'description': 'Current marital status'},
                'Education_Level': {'values': ['High School', 'Bachelor', 'Master', 'PhD'], 'description': 'Highest education level achieved'},
                'Occupation': {'type': 'string', 'description': 'Current job or profession'},
                'Income_Level': {'range': '$20,000-$200,000', 'description': 'Annual income range'}
            }
        },
        'Economic': {
            'description': 'Economic and financial indicators',
            'properties': {
                'Employment_Status': {'values': ['Employed', 'Unemployed', 'Self-employed', 'Retired'], 'description': 'Current employment status'},
                'Income_Bracket': {'values': ['Low', 'Medium', 'High'], 'description': 'Income category'},
                'Credit_Score': {'range': '300-850', 'description': 'Credit score range'},
                'Investment_Activity': {'values': ['None', 'Low', 'Medium', 'High'], 'description': 'Level of investment activity'}
            }
        },
        # Add other node types with their metadata...
    }

    @staticmethod
    def get_node_metadata(label):
        return SchemaMetadata.METADATA.get(label, {
            'description': f'Information about {label}',
            'properties': {}
        })

    @staticmethod
    def format_property_details(prop_name, prop_info):
        details = []
        if 'range' in prop_info:
            details.append(f"Range: {prop_info['range']}")
        if 'values' in prop_info:
            details.append(f"Values: {', '.join(prop_info['values'])}")
        if 'description' in prop_info:
            details.append(f"Description: {prop_info['description']}")
        return f"**{prop_name}**\n" + "\n".join(details) 