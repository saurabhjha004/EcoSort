# EcoSort - Sustainable Shopping 🌿

**Deployed Application**: [EcoSort - Sustainable Shopping](https://eco-sort.streamlit.app/)

## 📖 Overview
**EcoSort** is a user-friendly platform that empowers consumers to shop sustainably by providing insights into the carbon emissions of various products. By highlighting low-emission products and offering intuitive filtering options, EcoSort makes sustainable shopping effortless and impactful.

## ✨ Features
- **Filter by Material Type**: Narrow your search by selecting specific product materials.
- **Weight-Based Filtering**: Refine results by selecting product weights for more precise recommendations.
- **Detailed Carbon Metrics**: View production, logistics, and total emissions for each product.
- **Color-Coded Results**: Easily identify low, average, and high-emission products with intuitive color indicators.
- **Average Emission Comparison**: Compare product emissions against the average for the selected category.

## 📊 Dataset
EcoSort uses a modified version of the [Supply Chain Greenhouse Gas Emission Factors (v1.3) by NAICS-6](https://catalog.data.gov/dataset/supply-chain-greenhouse-gas-emission-factors-v1-3-by-naics-6). The dataset has been adapted to meet the application's needs while maintaining data integrity.

## 🛠️ Technical Stack
- **Frontend**: [Streamlit](https://streamlit.io/) for a clean and interactive user interface.
- **Backend**: Python with Pandas for data handling and analysis.
- **Deployment**: Hosted on [Streamlit Cloud](https://streamlit.io/cloud).

Steps to Run Locally
Clone the repository:

bash
Copy code
git clone https://github.com/saurabhjha004/EcoSort
Navigate to the project directory:

bash
Copy code
cd eco-sort
Ensure the dataset (products.csv) is in the root directory.

Run the application using Streamlit:

bash
Copy code
streamlit run app.py
Open the application in your browser at http://localhost:8501/.

Project Structure
plaintext
Copy code
eco-sort/
├── app.py                 # Main application script
├── main.py                # Backend functions for emissions calculations
├── products.csv           # Dataset used for product emissions
├── requirements.txt       # List of required Python libraries
├── README.md              # Project documentation
Future Enhancements
Dynamic Data Integration: Automatically fetch product data from vendors in real time.
Advanced Carbon Models: Incorporate machine learning for more accurate emission predictions.
Personalized Recommendations: Suggest eco-friendly products based on user preferences.
Educational Resources: Provide tips and resources for adopting sustainable shopping habits.
License
This project is licensed under the MIT License.
