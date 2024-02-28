import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def transformation(input_data):
    dataset = pd.read_csv(input_date)
    #taking only the required columns
    transformed_data = dataset[['Material', 'Material Identity', 'Density (kg/m^3)', 'Young Modulus (MPa)', 'Poisson Ratio',
                          'Thermal Conductivity (W/m/K)', 'Expansion Coefficient (mum/m/K)', 'Specific Heat (J/kg/K)']]
    
    #changing the data type to correct format
    transformed_data['Density (kg/m^3)']=transformed_data['Density (kg/m^3)'].astype(float)
    transformed_data['Young Modulus (MPa)']=transformed_data['Young Modulus (MPa)'].astype(float)
    transformed_data['Poisson Ratio']= transformed_data['Poisson Ratio'].astype(float)
    transformed_data['Thermal Conductivity (W/m/K)'] = transformed_data['Thermal Conductivity (W/m/K)'].astype(float)
    transformed_data['Expansion Coefficient (mum/m/K)'] = transformed_data['Expansion Coefficient (mum/m/K)'].astype(float)
    transformed_data['Specific Heat (J/kg/K)'] = transformed_data['Specific Heat (J/kg/K)'].astype(float)

    # Returning the data set
    return transformed_data

def get_recommendations(user_requirements):
    # Load material data
    input_data = 'material_dataset.csv'
    material_data = pd.read_csv(input_data)

    # Extract only the properties columns for comparison
    material_properties = material_data.drop(columns=['Material', 'Material Identity'])

    # Normalize data
    scaler = StandardScaler()

    # Fit and transform the data
    material_properties_normalized = scaler.fit_transform(material_properties)

    # Remove Material Identity from user requirements
    user_requirements.pop('Material Identity', None)

    # Convert user requirements to DataFrame
    user_requirements_df = pd.DataFrame(user_requirements, index=[0])

    # Normalize user requirements
    user_requirements_normalized = scaler.transform(user_requirements_df)

    # Calculate cosine similarity
    similarities = cosine_similarity(material_properties_normalized, user_requirements_normalized)

    # Add similarity column to the dataset
    material_data['Similarity'] = similarities[:,0]

    # Sort by similarity
    recommendations = material_data.sort_values(by='Similarity', ascending=False)

    return recommendations[['Material', 'Similarity']]
