import os
import joblib
import pandas as pd
import pytest

def test_model_predicts():
    # Check model file exists
    model_path = os.path.join('models', 'xgb_model.pkl')
    assert os.path.exists(model_path), f"Model file {model_path} not found. Run training script."
    model = joblib.load(model_path)
    # Load engineered features
    df = pd.read_csv(os.path.join('data', 'engineered_variants.csv'))
    # Example: use only feature columns for prediction
    # Use only numeric/categorical columns for prediction
    feature_cols = ['hotspot_flag', 'driver_gene_flag', 'tmb', 'tumor_type_encoded']
    X = df[feature_cols]
    # Ensure correct dtypes
    X = X.apply(pd.to_numeric, errors='coerce')
    assert X.notnull().all().all(), "Nulls in input features for prediction."
    preds = model.predict(X)
    assert len(preds) == len(df), "Prediction count does not match input rows."
