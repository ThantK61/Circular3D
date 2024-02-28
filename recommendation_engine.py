import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def transformation(input_data):
    dataset = pd.read_csv(input_data)  # Corrected variable name from input_date to input_data
    transformed_data = dataset[['Material', 'Material Identity', 'Density (kg/m^3)', 'Young Modulus (MPa)', 'Poisson Ratio',
                                'Thermal Conductivity (W/m/K)', 'Expansion Coefficient (mum/m/K)', 'Specific Heat (J/kg/K)']]
    # Ensure all columns are numeric, converting if necessary
    numeric_columns = ['Density (kg/m^3)', 'Young Modulus (MPa)', 'Poisson Ratio', 'Thermal Conductivity (W/m/K)', 
                       'Expansion Coefficient (mum/m/K)', 'Specific Heat (J/kg/K)']
    for col in numeric_columns:
        transformed_data[col] = pd.to_numeric(transformed_data[col], errors='coerce')
    return transformed_data

def get_recommendations(user_requirements):
    input_data = 'material_dataset.csv'
    material_data = transformation(input_data)  # Use the transformation function to ensure data is clean
    material_properties = material_data.drop(columns=['Material', 'Material Identity'])  # Ensure only numeric columns are included
    
    scaler = StandardScaler()
    material_properties_normalized = scaler.fit_transform(material_properties)
    
    # Adjust user_requirements to match the structure expected for scaling
    user_requirements.pop('Material Identity', None)  # Remove non-numeric fields
    user_requirements_df = pd.DataFrame(user_requirements, index=[0])
    
    # Convert all user input to numeric, handling non-numeric gracefully
    for column in user_requirements_df.columns:
        user_requirements_df[column] = pd.to_numeric(user_requirements_df[column], errors='coerce')
    
    user_requirements_normalized = scaler.transform(user_requirements_df)
    
    similarities = cosine_similarity(material_properties_normalized, user_requirements_normalized)
    material_data['Similarity'] = similarities[:, 0]
    recommendations = material_data.sort_values(by='Similarity', ascending=False)  # Corrected method name sort_vaslues to sort_values
    
    return recommendations[['Material', 'Similarity']]