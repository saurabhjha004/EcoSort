import streamlit as st
import pandas as pd
from main import load_data, sort_products_by_emissions

# Set page title
st.set_page_config(page_title="EcoSort - Green Shopping", layout="wide")

# Load data
data = load_data()

# Sidebar for filtering
st.sidebar.header("Filter Options")
product_types = data['Material Type'].unique()
selected_product_type = st.sidebar.selectbox("Select Product Type", product_types)

# Weight filtering
weight_options = list(data['Weight (kg)'].unique()) + ["All"]
selected_weight = st.sidebar.selectbox("Select Weight (or 'All' for no filter)", weight_options)
if selected_weight == "All":
    selected_weight = None

# Main content
st.title("EcoSort - Top 10 Low Emission Products")
st.subheader("Your sustainable shopping choices")

# Sort and display
sorted_products = sort_products_by_emissions(data, selected_product_type, selected_weight)

if len(sorted_products) == 0:
    st.warning("No products found for the selected criteria.")
else:
    # Create cards for the top 10 products
    for _, row in sorted_products.iterrows():
        st.markdown(
            f"""
            <div style="padding: 1em; margin-bottom: 1em; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                <h4>{row['Industry']} - {row['Material Type']}</h4>
                <p><strong>Production Emissions:</strong> {row['Production Emissions']:.2f} kg CO2e</p>
                <p><strong>Logistics Emissions:</strong> {row['Logistics Emissions']:.2f} kg CO2e</p>
                <p><strong>Total Emissions:</strong> {row['Total Emissions']:.2f} kg CO2e</p>
            </div>
            """, unsafe_allow_html=True
        )
