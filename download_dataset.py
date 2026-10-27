"""
Download the Concrete Compressive Strength dataset from UCI ML Repository.
Dataset ID: 165
Source: https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength
"""

import os
import pandas as pd
from ucimlrepo import fetch_ucirepo

# Fetch the dataset
print("Fetching Concrete Compressive Strength dataset from UCI ML Repository...")
dataset = fetch_ucirepo(id=165)

# Print metadata
print(f"\nDataset Name: {dataset.metadata.name}")
print(f"Number of Instances: {dataset.metadata.num_instances}")

# Extract features and target
X = dataset.data.features
y = dataset.data.targets

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"\nFeature columns: {list(X.columns)}")
print(f"Target columns: {list(y.columns)}")

# Combine into a single DataFrame for saving
df = pd.concat([X, y], axis=1)
print(f"\nCombined DataFrame shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nData types:")
print(df.dtypes)
print(f"\nMissing values:")
print(df.isnull().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# Save dataset
dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
os.makedirs(dataset_dir, exist_ok=True)

csv_path = os.path.join(dataset_dir, "concrete_data.csv")
df.to_csv(csv_path, index=False)
print(f"\nSaved CSV to: {csv_path}")
print(f"File size: {os.path.getsize(csv_path)} bytes")
print(f"\nDataset successfully downloaded and saved!")
