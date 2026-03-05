"""
Feature engineering for variant data.
- Loads synthetic_variants.csv
- Adds engineered features (hotspot, driver gene, tmb_bin, tumor_type_encoded, etc.)
- Saves engineered features to data/engineered_variants.csv
"""
import pandas as pd
import os

HOTSPOT_MUTATIONS = {"TP53": ["p.R175H"], "BRAF": ["p.V600E"]}
DRIVER_GENES = {"TP53", "BRAF", "EGFR", "KRAS", "ALK", "PIK3CA", "NRAS", "IDH1", "PTEN", "CDKN2A", "MET", "ERBB2", "FGFR3", "KIT", "RET"}


def engineer_features(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    # Hotspot flag
    df["hotspot_flag"] = df.apply(lambda row: int(row["protein_change"] in HOTSPOT_MUTATIONS.get(row["gene"], [])), axis=1)
    # Driver gene flag
    df["driver_gene_flag"] = df["gene"].apply(lambda g: int(g in DRIVER_GENES))
    # TMB binning
    df["tmb_bin"] = pd.cut(df["tmb"], bins=[-1, 5, 10, 100], labels=["low", "medium", "high"])
    # Tumor type encoding
    tumor_types = {t: i for i, t in enumerate(df["tumor_type"].unique())}
    df["tumor_type_encoded"] = df["tumor_type"].map(tumor_types)
    # Save
    df.to_csv(output_csv, index=False)
    print(f"Engineered features saved to {output_csv}")

if __name__ == "__main__":
    input_csv = os.path.join(os.path.dirname(__file__), "../../data/synthetic_variants.csv")
    output_csv = os.path.join(os.path.dirname(__file__), "../../data/engineered_variants.csv")
    engineer_features(input_csv, output_csv)
