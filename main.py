import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import random

# Load the dataset
file_path = r'C:\Users\Lenovo\Desktop\randomized_balanced_dataset.csv'  # Update with your dataset path
data = pd.read_csv(file_path)

# Sample vendor locations (latitude, longitude) for each product
vendor_locations = [
    (37.7749, -122.4194),  # San Francisco
    (34.0522, -118.2437),  # Los Angeles
    (40.7128, -74.0060),   # New York
    (51.5074, -0.1278),    # London
    (48.8566, 2.3522),     # Paris
    (35.6895, 139.6917),   # Tokyo
]

# Available modes of transportation
transport_modes = ['road', 'sea', 'air']

# Possible weights (kg)
weights = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

# Predefined distances in kilometers (no geopy needed)
random_distances = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]  # Random distances between vendor and customer

# Emission factors for different transport modes
emission_factors = {
    'air': 0.5,  # kg CO2e per km per kg
    'sea': 0.02,  # kg CO2e per km per kg
    'road': 0.15  # kg CO2e per km per kg
}

# Preprocess and train the model
def train_production_emissions_model(data):
    X = data[['Material Type', 'Weight (kg)']]
    y = data['Emission Factor per kg (CO2e)']
    
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(), ['Material Type'])],
        remainder='passthrough'
    )
    
    model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', RandomForestRegressor(random_state=42))])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    print(f"Model R^2 Score: {model.score(X_test, y_test):.2f}")
    
    return model

# Calculate logistics emissions based on vendor location, customer location, and mode of transport
def calculate_logistics_emissions(weight, mode):
    # Randomly select a distance from the list
    distance_km = random.choice(random_distances)
    
    # Get the emission factor for the selected transport mode
    factor = emission_factors.get(mode, 0.15)  # Default to 'road' if no mode is provided
    
    # Calculate logistics emissions
    logistics_emissions = distance_km * weight * factor / 1000  # Convert to kg of CO2e
    return logistics_emissions, distance_km

# Randomize vendor location, weight, and transport mode for each product
def randomize_vendor_weight_transport(data):
    random.seed(42)  # Set random seed for reproducibility
    data['Vendor Location'] = [random.choice(vendor_locations) for _ in range(len(data))]
    data['Weight (kg)'] = [random.choice(weights) for _ in range(len(data))]  # Randomize weights for each product
    data['Transport Mode'] = [random.choice(transport_modes) for _ in range(len(data))]
    return data

# Sort products by total emissions based on selected product type
def sort_products_by_emissions(data, model, customer_loc):
    sorted_data = data.copy()
    
    # Predict production emissions (scaled by weight) 
    sorted_data['Predicted Production Emissions'] = sorted_data['Weight (kg)'] * sorted_data['Emission Factor per kg (CO2e)']
    
    # Calculate logistics emissions
    sorted_data['Logistics Emissions'] = sorted_data.apply(
        lambda row: calculate_logistics_emissions(row['Weight (kg)'], row['Transport Mode'])[0],  # Only use emissions part
        axis=1
    )
    
    # Calculate total emissions
    sorted_data['Total Emissions'] = sorted_data['Predicted Production Emissions'] + sorted_data['Logistics Emissions']
    
    # Sort products by category and total emissions
    sorted_data = sorted_data.sort_values(by=['Material Type', 'Total Emissions'])
    
    return sorted_data

# Main execution for user selection
def run_for_selected_product_type(data, model, product_type, customer_loc):
    # Filter the data based on user-selected product type
    filtered_data = data[data['Material Type'] == product_type]
    
    # Randomize vendor location, weight, and transport mode
    filtered_data = randomize_vendor_weight_transport(filtered_data)
    
    # Run emissions sorting
    sorted_products = sort_products_by_emissions(
        filtered_data, model, customer_loc
    )
    
    # Display sorted products in the terminal
    print(f"\nTop 10 least carbon-producing products for {product_type}:")
    print(sorted_products[['Industry', 'Material Type', 'Weight (kg)', 'Predicted Production Emissions', 'Logistics Emissions', 'Total Emissions']].head(10))  # Display top 10 sorted products
    
    return sorted_products

# Example usage
if __name__ == '__main__':
    # Train the model
    model = train_production_emissions_model(data)
    
    # List available product categories
    categories = data['Material Type'].unique()
    print("\nAvailable categories to choose from:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    # Get user input for product type (user selects from the list)
    user_input = input(f"Select a category (enter number between 1 and {len(categories)}): ")
    try:
        selected_category = categories[int(user_input) - 1]
        print(f"You selected: {selected_category}")
    except (ValueError, IndexError):
        print("Invalid selection, defaulting to 'Electronics'.")
        selected_category = 'Electronics'  # Default selection
    
    # Customer location (for example, Los Angeles)
    customer_location = (34.0522, -118.2437)
    
    # Run for selected product type and show the top sorted products
    run_for_selected_product_type(data, model, selected_category, customer_location)
