import pandas as pd
import random

# Load the dataset
file_path = 'products.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Define emission factors for different transport modes (kg CO2e per km per kg)
emission_factors = {
    'air': 0.5,   # Air transport
    'water': 0.02, # Sea transport
    'land': 0.15  # Road transport
}

# Predefined distances in kilometers for simulation
random_distances = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]  # Example distances

# Function to calculate logistics emissions
def calculate_logistics_emissions(weight, mode):
    # Randomly select a distance
    distance_km = random.choice(random_distances)
    
    # Get the emission factor for the selected mode of transport
    factor = emission_factors.get(mode, 0.15)  # Default to 'land' if mode is missing
    
    # Calculate logistics emissions (kg of CO2e)
    logistics_emissions = distance_km * weight * factor / 1000  # Convert to kg of CO2e
    return logistics_emissions, distance_km

# Function to sort products based on total emissions
def sort_products_by_emissions(data, product_type):
    # Filter the data by the selected product type
    filtered_data = data[data['Material Type'] == product_type]
    
    # Calculate production emissions
    filtered_data['Production Emissions'] = filtered_data['Weight (kg)'] * filtered_data['Emission Factor per kg (CO2e)']
    
    # Calculate logistics emissions
    filtered_data['Logistics Emissions'] = filtered_data.apply(
        lambda row: calculate_logistics_emissions(row['Weight (kg)'], row['Transport Mode'])[0], axis=1
    )
    
    # Calculate total emissions
    filtered_data['Total Emissions'] = filtered_data['Production Emissions'] + filtered_data['Logistics Emissions']
    
    # Sort by total emissions
    sorted_data = filtered_data.sort_values(by='Total Emissions')
    return sorted_data

# Main script
if __name__ == '__main__':
    # Display available product types
    print("\nAvailable product types in the dataset:")
    product_types = data['Material Type'].unique()
    for i, product_type in enumerate(product_types, 1):
        print(f"{i}. {product_type}")
    
    # Ask the user to select a product type
    user_choice = input(f"\nSelect a product type (1-{len(product_types)}): ")
    try:
        selected_product_type = product_types[int(user_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice. Defaulting to the first product type.")
        selected_product_type = product_types[0]
    
    print(f"\nYou selected: {selected_product_type}")
    
    # Sort the products for the selected type
    sorted_products = sort_products_by_emissions(data, selected_product_type)
    
    # Display the top 10 least carbon-producing products
    print(f"\nTop 10 least carbon-producing products for {selected_product_type}:")
    print(sorted_products[['Industry', 'Material Type', 'Weight (kg)', 
                           'Production Emissions', 'Logistics Emissions', 
                           'Total Emissions']].head(10))
