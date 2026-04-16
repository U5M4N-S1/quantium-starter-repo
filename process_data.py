import pandas as pd
import os

# Folder containing the CSV files
data_folder = "data"

# List to hold each processed DataFrame
dataframes = []

# Loop through every CSV in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(data_folder, filename)
        df = pd.read_csv(filepath)

        # Keep only Pink Morsel rows
        df = df[df["product"] == "pink morsel"]

        # Combine quantity and price into a single "sales" field
        df["sales"] = df["quantity"] * df["price"]

        # Keep only the columns we care about
        df = df[["sales", "date", "region"]]

        dataframes.append(df)

# Combine all three into one DataFrame
combined = pd.concat(dataframes, ignore_index=True)

# Write the result to a new CSV
combined.to_csv("formatted_data.csv", index=False)

print(f"Done! Wrote {len(combined)} rows to formatted_data.csv")