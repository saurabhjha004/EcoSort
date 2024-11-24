import streamlit as st
import pandas as pd
from main import load_data, sort_products_by_emissions, calculate_average_emissions

# Configure the app's settings
st.set_page_config(
    page_title="EcoSort - Sustainable Shopping",
    page_icon="🌿",
    layout="wide"
)

# Load product data
data = load_data()

# Display welcome message
st.title("🌿 Welcome to EcoSort!")
st.subheader("Your Guide to Sustainable Shopping")
st.markdown("""
EcoSort helps you find environmentally-friendly products by highlighting items with the lowest carbon emissions. 
Make informed choices and contribute to a greener planet!
""")

# Sidebar filters
st.sidebar.header("Filter Options")
# Dropdown for selecting product type
product_types = data['Material Type'].unique()
selected_product_type = st.sidebar.selectbox("Select Product Type", product_types)

# Dropdown for selecting weight (or no weight filter)
weight_options = ["All"] + sorted(data['Weight (kg)'].unique())
selected_weight = st.sidebar.selectbox("Select Weight (or 'All' for no filter)", weight_options)
if selected_weight == "All":
    selected_weight = None

# Show results when the button is clicked
if st.sidebar.button("Show Top Products"):
    # Display selected filters
    st.markdown(f"### Results for: {selected_product_type}")
    if selected_weight:
        st.markdown(f"**Weight:** {selected_weight} kg")

    # Filter and sort products
    sorted_products = sort_products_by_emissions(data, selected_product_type, selected_weight)

    # Handle case when no products match the criteria
    if len(sorted_products) == 0:
        st.warning("No products found for the selected criteria.")
    else:
        # Compute the average total emissions for filtered products
        average_emissions = calculate_average_emissions(data, selected_product_type, selected_weight)

        # Display average emissions
        st.markdown(f"### Average Emissions: {average_emissions:.2f} kg CO2")

        # Show products with color-coded differences
        st.markdown("### Top 20 Low Emission Products")
        for index, row in sorted_products.iterrows():
            # Calculate difference from the average emissions
            emission_difference = row['Total Emissions'] - average_emissions

            # Set box color based on the difference
            if emission_difference < 0:
                box_color = "#d4edda"  # Green for below average
            elif emission_difference == 0:
                box_color = "#fff3cd"  # Yellow for average
            else:
                box_color = "#f8d7da"  # Red for above average

            # Display product details in a styled box
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #ccc; 
                    border-radius: 8px; 
                    background-color: {box_color}; 
                    padding: 15px; 
                    margin-bottom: 15px;
                ">
                    <h4>{row['Industry']} - {row['Material Type']}</h4>
                    <p><strong>Production Emissions:</strong> {row['Production Emissions']:.2f} kg CO2e</p>
                    <p><strong>Logistics Emissions:</strong> {row['Logistics Emissions']:.2f} kg CO2e</p>
                    <p><strong>Total Emissions:</strong> {row['Total Emissions']:.2f} kg CO2e</p>
                    <p><strong>Difference from Average:</strong> {emission_difference:+.2f} kg CO2</p>
                </div>
                """,
                unsafe_allow_html=True
            )
