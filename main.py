import pandas as pd
import random

# Load dataset
def load_data(file_path='products.csv'):
    # Ensure consistent random values for reproducibility
    random.seed(42)
    return pd.read_csv(file_path)

# Emission factors for transport modes (in kg CO2e per km per kg)
emission_factors = {
    'air': 0.5,   # Air transport is highly polluting
    'water': 0.02, # Water transport is more eco-friendly
    'land': 0.15  # Land transport is moderate
}

# List of random distances to simulate logistics scenarios
random_distances = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

# Calculate emissions for logistics based on weight and transport mode
def calculate_logistics_emissions(weight, mode):
    # Pick a random distance from predefined options
    distance_km = random.choice(random_distances)
    # Get emission factor for the selected transport mode
    factor = emission_factors.get(mode, 0.15)  # Default to land transport if unknown
    # Calculate and return logistics emissions
    return distance_km * weight * factor / 1000

# Filter and sort products by total emissions
def sort_products_by_emissions(data, product_type, selected_weight=None):
    # Filter by product type
    filtered_data = data[data['Material Type'] == product_type]
    if selected_weight is not None:
        # Further filter by weight if a specific weight is selected
        filtered_data = filtered_data[filtered_data['Weight (kg)'] == selected_weight]

    # Calculate emissions for production and logistics
    filtered_data['Production Emissions'] = (
        filtered_data['Weight (kg)'] * filtered_data['Emission Factor per kg (CO2e)']
    )
    filtered_data['Logistics Emissions'] = filtered_data.apply(
        lambda row: calculate_logistics_emissions(row['Weight (kg)'], row['Transport Mode']), axis=1
    )
    # Compute total emissions
    filtered_data['Total Emissions'] = (
        filtered_data['Production Emissions'] + filtered_data['Logistics Emissions']
    )
    # Return top 20 products with the lowest total emissions
    return filtered_data.sort_values(by='Total Emissions').head(20)

# Calculate average total emissions for the filtered data
def calculate_average_emissions(data, product_type, selected_weight=None):
    # Filter data by product type
    filtered_data = data[data['Material Type'] == product_type]
    if selected_weight is not None:
        # Apply additional weight filtering
        filtered_data = filtered_data[filtered_data['Weight (kg)'] == selected_weight]

    # Handle case where no data matches the filter
    if filtered_data.empty:
        return 0  # Default average for empty datasets

    # Calculate total emissions
    filtered_data['Production Emissions'] = (
        filtered_data['Weight (kg)'] * filtered_data['Emission Factor per kg (CO2e)']
    )
    filtered_data['Logistics Emissions'] = filtered_data.apply(
        lambda row: calculate_logistics_emissions(row['Weight (kg)'], row['Transport Mode']), axis=1
    )
    filtered_data['Total Emissions'] = (
        filtered_data['Production Emissions'] + filtered_data['Logistics Emissions']
    )
    # Compute and return the average
    return filtered_data['Total Emissions'].mean()
