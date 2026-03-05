import os
import pandas as pd
import pytest

def test_engineered_features_exist():
    # Check engineered_variants.csv exists
    path = os.path.join('data', 'engineered_variants.csv')
    assert os.path.exists(path), f"{path} not found. Run feature engineering script."
    df = pd.read_csv(path)
    # Example: check for expected feature columns
    expected_features = [
        'gene', 'transcript', 'protein_change', 'genome_build', 'tumor_type',
        'tmb', 'prior_therapy_count', 'hotspot_flag', 'driver_gene_flag',
        'tmb_bin', 'tumor_type_encoded'
    ]
    for col in expected_features:
        assert col in df.columns, f"Missing feature column: {col}"
    # Check for non-null values in numeric/categorical columns
    numeric_cols = ['tmb', 'prior_therapy_count', 'hotspot_flag', 'driver_gene_flag', 'tumor_type_encoded']
    for col in numeric_cols:
        assert df[col].notnull().all(), f"Null values found in column: {col}"
