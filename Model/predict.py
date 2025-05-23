import pickle
import numpy as np
import pandas as pd

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

# Sample input
sample = pd.DataFrame(
    [
        {
            "Monthly_Usage_kWh": 950.0,
            "Year": 2022,
            "Household_Size": 4.6,
            "Adoption_Year": 2017,
            "Cost_Savings_USD": 300.0,
            "Country": "Australia",
            "Energy_Source": "Solar",
            "Income_Level": "Middle",
            "Urban_Rural": "Urban",
            "Subsidy_Received": "Yes",
        }
    ]
)[
    columns
]  # ensure correct column order

with open("K_Prototypes.pkl", "rb") as f:
    model = pickle.load(f)

cluster_id = model.predict(sample.to_numpy(), categorical=categorical_indexes)[0]

user_label = cluster_labels[cluster_id]

print(f"Cluster {cluster_id}: {user_label}")
