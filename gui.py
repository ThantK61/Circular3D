import streamlit as st
from recommendation_engine import get_recommendations

st.title("Material Recommendation System")

material_identity = st.text_input("Material Identity:")
density = st.number_input("Density (kg/m^3):", format="%f")
young_modulus = st.number_input("Young Modulus (MPa):", format="%f")
poisson_ratio = st.number_input("Poisson Ratio:", format="%f")
thermal_conductivity = st.number_input("Thermal Conductivity (W/m/K):", format="%f")
expansion_coefficient = st.number_input("Expansion Coefficient (mum/m/K):", format="%f")
specific_heat = st.number_input("Specific Heat (J/kg/K):", format="%f")

user_requirements = {
    'Material Identity': material_identity,
    'Density (kg/m^3)': density,
    'Young Modulus (MPa)': young_modulus,
    'Poisson Ratio': poisson_ratio,
    'Thermal Conductivity (W/m/K)': thermal_conductivity,
    'Expansion Coefficient (mum/m/K)': expansion_coefficient,
    'Specific Heat (J/kg/K)': specific_heat
}

if st.button("Get Recommendations"):
    recommendations = get_recommendations(user_requirements)
    st.text("Recommendations")
    df = recommendations[:5]
    st.write(df.to_html(index=False), unsafe_allow_html=True)