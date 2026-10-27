import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Concrete Strength Prediction Dashboard",
    page_icon="🏗️",
    layout="centered"
)

# Custom clean design CSS with light background and subtle green accents
st.markdown("""
<style>
    /* Clean background & typography */
    .main {
        background-color: #FAFAFA;
    }
    h1 {
        color: #1E3A2F;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #4A5568;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    /* Simple green accent buttons */
    div.stButton > button:first-child {
        background-color: #2E7D32;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    div.stButton > button:first-child:hover {
        background-color: #1B5E20;
        color: white;
    }
    /* Reset button */
    div.stButton > button[kind="secondary"] {
        background-color: #F1F5F2;
        color: #2E7D32;
        border: 1px solid #C8E6C9;
    }
    /* Metric cards styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #555555;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.35rem;
        color: #1E3A2F;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. Load Data and Train Linear Regression Model ---
@st.cache_resource
def load_and_train_model():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "concrete_data.csv")
    if not os.path.exists(data_path):
        st.error(f"Dataset file not found at {data_path}. Please run download_dataset.py first.")
        st.stop()
        
    df = pd.read_csv(data_path)
    # Cleaning identical to the project methodology: remove duplicate records
    df_clean = df.drop_duplicates(keep='first').reset_index(drop=True)
    
    # Feature names and target strictly matching training
    X = df_clean.drop(columns=['Concrete compressive strength'])
    y = df_clean['Concrete compressive strength']
    
    # 80:20 split with fixed random_state=42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Fit Linear Regression on training data only
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate model on test set
    y_pred_test = model.predict(X_test)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)
    
    # First 5 test records for visualization comparison
    test_samples_df = pd.DataFrame({
        'Sample': [f"Test {i+1}" for i in range(5)],
        'Actual Strength (MPa)': np.round(y_test.values[:5], 2),
        'Predicted Strength (MPa)': np.round(y_pred_test[:5], 2)
    })
    
    return model, list(X.columns), test_mae, test_r2, test_samples_df

model, feature_names, test_mae, test_r2, test_samples_df = load_and_train_model()

# --- 1. Page Title & Subtitle ---
st.title("Concrete Strength Prediction Dashboard")
st.markdown('<p class="subtitle">Estimate concrete compressive strength using Linear Regression.</p>', unsafe_allow_html=True)

# Default example values as requested
DEFAULT_VALUES = {
    'Cement': 300.0,
    'Blast Furnace Slag': 100.0,
    'Fly Ash': 50.0,
    'Water': 180.0,
    'Superplasticizer': 6.0,
    'Coarse Aggregate': 1000.0,
    'Fine Aggregate': 750.0,
    'Age': 28
}

# Initialise session state for inputs if not present
for key, val in DEFAULT_VALUES.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Reset helper
def reset_to_example():
    for k, v in DEFAULT_VALUES.items():
        st.session_state[k] = v
    if 'prediction_result' in st.session_state:
        del st.session_state['prediction_result']

# --- 2. Simple Input Section ---
st.subheader("Mix Ingredients and Age")

col1, col2 = st.columns(2)

with col1:
    cement = st.number_input(
        "Cement (kg/m³)",
        min_value=0.0, max_value=800.0,
        value=float(st.session_state['Cement']),
        step=5.0, key='Cement'
    )
    slag = st.number_input(
        "Blast Furnace Slag (kg/m³)",
        min_value=0.0, max_value=500.0,
        value=float(st.session_state['Blast Furnace Slag']),
        step=5.0, key='Blast Furnace Slag'
    )
    fly_ash = st.number_input(
        "Fly Ash (kg/m³)",
        min_value=0.0, max_value=400.0,
        value=float(st.session_state['Fly Ash']),
        step=5.0, key='Fly Ash'
    )
    water = st.number_input(
        "Water (kg/m³)",
        min_value=0.0, max_value=400.0,
        value=float(st.session_state['Water']),
        step=2.0, key='Water'
    )

with col2:
    superplasticizer = st.number_input(
        "Superplasticizer (kg/m³)",
        min_value=0.0, max_value=50.0,
        value=float(st.session_state['Superplasticizer']),
        step=0.5, key='Superplasticizer'
    )
    coarse_agg = st.number_input(
        "Coarse Aggregate (kg/m³)",
        min_value=0.0, max_value=1500.0,
        value=float(st.session_state['Coarse Aggregate']),
        step=10.0, key='Coarse Aggregate'
    )
    fine_agg = st.number_input(
        "Fine Aggregate (kg/m³)",
        min_value=0.0, max_value=1200.0,
        value=float(st.session_state['Fine Aggregate']),
        step=10.0, key='Fine Aggregate'
    )
    age = st.number_input(
        "Age (days)",
        min_value=1, max_value=365,
        value=int(st.session_state['Age']),
        step=1, key='Age'
    )

btn_col1, btn_col2, _ = st.columns([1.2, 1.4, 2.5])

with btn_col1:
    predict_clicked = st.button("Predict Strength", type="primary")

with btn_col2:
    st.button("Reset to Example", on_click=reset_to_example)

# Handle prediction
if predict_clicked:
    # Prepare input DataFrame with exact matching feature names and order
    input_data = pd.DataFrame([{
        'Cement': cement,
        'Blast Furnace Slag': slag,
        'Fly Ash': fly_ash,
        'Water': water,
        'Superplasticizer': superplasticizer,
        'Coarse Aggregate': coarse_agg,
        'Fine Aggregate': fine_agg,
        'Age': age
    }])
    
    try:
        prediction_val = float(model.predict(input_data)[0])
        st.session_state['prediction_result'] = prediction_val
    except Exception as e:
        st.error(f"Error computing prediction: {e}")

# --- 3. Output Section & 4. Small Dashboard Summary ---
if 'prediction_result' in st.session_state:
    pred_val = st.session_state['prediction_result']
    
    st.markdown("---")
    st.subheader("Prediction Summary")
    
    # 4. Three compact metric cards
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(
            label="Predicted Strength",
            value=f"{pred_val:.2f} MPa"
        )
    with m_col2:
        st.metric(
            label="Model MAE (Test Set)",
            value=f"{test_mae:.2f} MPa"
        )
    with m_col3:
        st.metric(
            label="Model R² Score (Test Set)",
            value=f"{test_r2:.4f}"
        )
    
    # Strength Category determination (illustrative)
    # Low: < 20 MPa, Moderate: 20 - 40 MPa, High: > 40 MPa
    if pred_val < 20.0:
        cat_name = "Low"
        cat_badge = "🟡"
    elif pred_val <= 40.0:
        cat_name = "Moderate"
        cat_badge = "🟢"
    else:
        cat_name = "High"
        cat_badge = "🔵"
        
    st.markdown(
        f"**Strength category:** {cat_badge} **{cat_name}** *(illustrative category, not a structural safety classification)*"
    )
    st.caption("This is the model's estimated strength based on the values entered.")

# --- 5. Simple Visualisation ---
st.markdown("---")
st.subheader("Model Performance on Test Samples")
st.caption("Comparison of actual test measurements vs. linear regression predictions for 5 test-set batches.")

# Format comparison chart data
chart_df = test_samples_df.set_index('Sample')
st.bar_chart(chart_df, color=["#1E88E5", "#2E7D32"])

# --- Educational Disclaimer ---
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** This dashboard is an educational predictive tool developed for an AI/ML coursework "
    "demonstration. The predictions are mathematical estimates derived from Linear Regression on the UCI "
    "Concrete Compressive Strength dataset and do not substitute for certified civil engineering testing "
    "or structural safety assessments."
)
