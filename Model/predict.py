import pickle
import numpy as np
import pandas as pd
from utils import encode_df

categorical_indexes = [0, 1]

cluster_labels = {
    0: "Modest Solar Starters",
    1: "High-Usage Biomass Households",
    2: "Urban Wind-Funded Families",
    3: "Resilient Rural Solar Pioneers",
    4: "Underperforming Hydro Households",
    5: "Independent Urban Wind Users",
    6: "Subsidized Hydro Families",
    7: "Rural Geothermal Pioneers",
    8: "Urban Wind Maximizers",
    9: "Strategic Biomass Users",
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
)[columns]

with open("K_Prototypes.pkl", "rb") as f:
    model = pickle.load(f)

cluster_id = model.predict(
    encode_df(sample).to_numpy(), categorical=categorical_indexes
)[0]

user_label = cluster_labels[cluster_id]

print(f"Cluster {cluster_id}: {user_label}")
