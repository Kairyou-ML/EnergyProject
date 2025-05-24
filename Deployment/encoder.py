from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle
import os


def encode_df(df: pd.DataFrame):
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scaler_path = os.path.join(base_dir, "EDA & Preprocessing", "scaler.pkl")
    
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    # Normalize numerical data
    num_cols = [
        "Monthly_Usage_kWh",
        "Household_Size",
        "Cost_Savings_USD",
        "Adoption_Year",
        "Year",
    ]
    df_scaled = df.copy()

    df_scaled[num_cols] = scaler.transform(df[num_cols])

    # Encode ordinal data into binary
    df_scaled["Income_Level"] = df["Income_Level"].map(
        {"Low": 0, "Middle": 1, "High": 2}
    )
    df_scaled["Urban_Rural"] = df["Urban_Rural"].map({"Urban": 1, "Rural": 0})
    df_scaled["Subsidy_Received"] = df["Subsidy_Received"].map({"Yes": 1, "No": 0})

    return df_scaled
