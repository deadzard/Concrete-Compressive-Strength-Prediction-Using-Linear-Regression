"""
Extract key results from the genuine dataset analysis for verification.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import json

df = pd.read_csv('dataset/concrete_data.csv')

# Clean duplicates
df_clean = df.drop_duplicates(keep='first').reset_index(drop=True)

# Split
X = df_clean.drop(columns=['Concrete compressive strength'])
y = df_clean['Concrete compressive strength']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# New prediction
new_sample = pd.DataFrame({
    'Cement': [300.0], 'Blast Furnace Slag': [100.0], 'Fly Ash': [50.0],
    'Water': [180.0], 'Superplasticizer': [6.0], 'Coarse Aggregate': [1000.0],
    'Fine Aggregate': [750.0], 'Age': [28]
})
new_pred = model.predict(new_sample)[0]

results = {
    'original_shape': [int(x) for x in df.shape],
    'missing_values': int(df.isnull().sum().sum()),
    'duplicates': int(df.duplicated().sum()),
    'clean_shape': [int(x) for x in df_clean.shape],
    'train_count': int(X_train.shape[0]),
    'test_count': int(X_test.shape[0]),
    'mae': float(round(mae, 2)),
    'r2': float(round(r2, 4)),
    'intercept': float(round(model.intercept_, 4)),
    'coefficients': {str(feat): float(round(coef, 4)) for feat, coef in zip(X.columns, model.coef_)},
    'five_records': [],
    'new_prediction': float(round(new_pred, 2)),
    'desc_stats': {}
}

for i in range(5):
    results['five_records'].append({
        'record_num': i + 1,
        'actual': float(round(y_test.values[i], 2)),
        'predicted': float(round(y_pred[i], 2)),
        'abs_error': float(round(abs(y_test.values[i] - y_pred[i]), 2))
    })

for col in df_clean.columns:
    results['desc_stats'][col] = {
        'mean': float(round(df_clean[col].mean(), 2)),
        'std': float(round(df_clean[col].std(), 2)),
        'min': float(round(df_clean[col].min(), 2)),
        'max': float(round(df_clean[col].max(), 2))
    }

with open('report_data.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Results successfully extracted and verified to report_data.json:")
print(json.dumps(results, indent=2))
