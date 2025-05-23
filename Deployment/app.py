import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import nbformat
from nbconvert import HTMLExporter
from functools import lru_cache


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

categorical_indexes = [0, 1, 5, 6, 8]  


cluster_labels = {
    0: "Heavy Users in Underserved Areas",
    1: "High Impact Rural Households",
    2: "Minimal Users with Strong Means",
    3: "Urban Subsidized Adopters",
    4: "Budget-Conscious Urban Beneficiaries",
    5: "Efficient Urban Savers",
    6: "High Consumers with Low Returns",
    7: "Frugal Households with High Gains",
    8: "Urban Energy Spenders",
    9: "Wealthy Subsidized Consumers",
}

# col names
columns = [
    "Country",
    "Energy_Source",
    "Monthly_Usage_kWh",
    "Year",
    "Household_Size",
    "Income_Level",
    "Urban_Rural",
    "Adoption_Year",
    "Subsidy_Received",
    "Cost_Savings_USD",
]

# map income lvl 
income_levels = {
    "0": "Low",
    "1": "Middle",
    "2": "High"
}


def load_model():
    
    model_path = os.path.join(BASE_DIR, 'Model', 'K_Prototypes.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)

#load mol startup
model = load_model()

# Routes
@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/analyzer')
def analyzer():
    
    return render_template('index.html')

@app.route('/notebook-view')
def notebook_view():
    
    notebook_html = get_notebook_html()
    return render_template('notebook.html', notebook_html=notebook_html)

@lru_cache(maxsize=1)
def get_notebook_html():
    """model html - cached """
    notebook_path = os.path.join(BASE_DIR, 'Model', 'model.ipynb')
    
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)
    
    # Convert to HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    (body, resources) = html_exporter.from_notebook_node(notebook_content)
    
    return body

@app.route('/download-model')
def download_model():
    """Download the model """
    model_path = os.path.join(BASE_DIR, 'Model', 'K_Prototypes.pkl')
    return send_file(model_path, 
                     mimetype='application/octet-stream',
                     download_name='energy_cluster_model.pkl',
                     as_attachment=True)

@app.route('/analyze', methods=['POST'])
def analyze():
    
    try:
        # Get data from form
        input_data, input_array = extract_form_data(request.form)
        
        # determine cluster 
        cluster_id = model.predict(input_array, categorical=categorical_indexes)[0]
        user_label = cluster_labels[cluster_id]
        
        return jsonify({
            'success': True,
            'cluster_id': int(cluster_id),
            'user_label': user_label,
        })
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'success': False
        })


def extract_form_data(form_data):
    # ex data and create data frame
    # Get input 
    country = form_data.get('country', 'Australia')
    energy_source = form_data.get('energy_source', 'Solar')
    monthly_usage = float(form_data.get('monthly_usage', 950.0))
    year = int(form_data.get('year', 2022))
    household_size = float(form_data.get('household_size', 4.6))
    income_level = income_levels[form_data.get('income_level', '1')]
    urban_rural = 'Urban' if form_data.get('urban') == 'true' else 'Rural'
    adoption_year = int(form_data.get('adoption_year', 2017))
    subsidy_received = 'Yes' if form_data.get('subsidy') == 'true' else 'No'
    cost_savings = float(form_data.get('cost_savings', 300.0))
    
    # Create struct data for model input 
    sample_data = {
        "Country": country,
        "Energy_Source": energy_source,
        "Monthly_Usage_kWh": monthly_usage,
        "Year": year,
        "Household_Size": household_size,
        "Income_Level": income_level,
        "Urban_Rural": urban_rural,
        "Adoption_Year": adoption_year,
        "Subsidy_Received": subsidy_received,
        "Cost_Savings_USD": cost_savings
    }
    
    input_df = pd.DataFrame([sample_data])[columns]  
    
    return input_df, input_df.to_numpy()

if __name__ == '__main__':
    app.run(debug=True) 
    