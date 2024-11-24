import pandas as pd
import random

# Load the dataset
def load_data(file_path='products.csv'):
    return pd.read_csv(file_path)

# Define emission factors for different transport modes (kg CO2e per km per kg)
emission_factors = {
    'air': 0.5,
    'water': 0.02,
    'land': 0.15
}

# Predefined distances in kilometers for simulation
random_distances = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

# Function to calculate logistics emissions
def calculate_logistics_emissions(weight, mode):
    distance_km = random.choice(random_distances)
    factor = emission_factors.get(mode, 0.15)
    logistics_emissions = distance_km * weight * factor / 1000
    return logistics_emissions

# Function to sort products based on total emissions
def sort_products_by_emissions(data, product_type, selected_weight=None):
    filtered_data = data[data['Material Type'] == product_type]
    if selected_weight is not None:
        filtered_data = filtered_data[filtered_data['Weight (kg)'] == selected_weight]

    filtered_data['Production Emissions'] = filtered_data['Weight (kg)'] * filtered_data['Emission Factor per kg (CO2e)']
    filtered_data['Logistics Emissions'] = filtered_data.apply(
        lambda row: calculate_logistics_emissions(row['Weight (kg)'], row['Transport Mode']), axis=1
    )
    filtered_data['Total Emissions'] = filtered_data['Production Emissions'] + filtered_data['Logistics Emissions']
    sorted_data = filtered_data.sort_values(by='Total Emissions')
    return sorted_data[['Industry', 'Material Type', 'Production Emissions', 'Logistics Emissions', 'Total Emissions']].head(10)
