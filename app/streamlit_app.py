import streamlit as st
import requests

st.title("Variant Actionability Scoring (API-integrated)")

API_URL = "http://localhost:8000/api/variant/score"
API_KEY = "changeme"

def get_score(payload):
    headers = {"Content-Type": "application/json", "X-API-Key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, response.text


def show_dashboard():
    st.header("Model Monitoring & Audit Trail Dashboard")
    st.markdown("View recent API calls and model usage statistics.")
    n = st.number_input("Show last N log entries", min_value=10, max_value=1000, value=100)
    try:
        headers = {"X-API-Key": API_KEY}
        resp = requests.get("http://localhost:8000/api/variant/logs", params={"n": n}, headers=headers)
        if resp.status_code == 200:
            logs = resp.json().get("logs", [])
            if logs:
                for line in logs:
                    st.text(line.strip())
            else:
                st.info("No logs found.")
        else:
            st.error(f"Failed to fetch logs: {resp.text}")
    except Exception as ex:
        st.error(f"Error fetching logs: {ex}")

def main():
    st.header("Single Variant Scoring")
    with st.form("single_variant_form"):
        gene = st.text_input("Gene", "TP53")
        transcript = st.text_input("Transcript", "NM_000546.5")
        protein_change = st.text_input("Protein Change", "p.R175H")
        genome_build = st.text_input("Genome Build", "GRCh38")
        tumor_type = st.selectbox("Tumor Type", [
            "lung_adenocarcinoma", "colorectal_cancer", "neuroblastoma", "melanoma", "breast_cancer", "thyroid_cancer", "glioma", "endometrial_cancer", "pancreatic_cancer", "bladder_cancer", "gastrointestinal_stromal_tumor", "medullary_thyroid_cancer"
        ], index=0)
        tmb = st.number_input("Tumor Mutational Burden (TMB)", min_value=0.0, value=12.5)
        prior_therapy_count = st.number_input("Prior Therapy Count", min_value=0, value=2)
        submit = st.form_submit_button("Score Variant")
    if submit:
        payload = {
            "gene": gene,
            "transcript": transcript,
            "protein_change": protein_change,
            "genome_build": genome_build,
            "tumor_type": tumor_type,
            "tmb": tmb,
            "prior_therapy_count": prior_therapy_count
        }
        result, error = get_score(payload)
        if result:
            st.success("Scoring Complete!")
            st.write("**Actionability Score:**", result["actionability_score"])
            st.write("**Resistance Probability:**", result["resistance_probability"])
            st.write("**Model Version:**", result["model_version"])
            st.subheader("Annotation")
            st.json(result["annotation"])
            st.subheader("Top Features (SHAP)")
            st.table(result["top_features"])
        else:
            st.error(f"API Error: {error}")

    st.header("Batch Variant Scoring (CSV Upload)")
    st.markdown("Upload a CSV with columns: gene, transcript, protein_change, genome_build, tumor_type, tmb, prior_therapy_count")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        import pandas as pd
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = ["gene", "transcript", "protein_change", "genome_build", "tumor_type", "tmb", "prior_therapy_count"]
            if not all(col in df.columns for col in required_cols):
                st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            else:
                results = []
                errors = []
                with st.spinner("Scoring variants..."):
                    for idx, row in df.iterrows():
                        payload = {col: row[col] for col in required_cols}
                        result, error = get_score(payload)
                        if result:
                            results.append({**payload, **result})
                        else:
                            errors.append({"row": idx, "error": error})
                if results:
                    st.success(f"Scored {len(results)} variants.")
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df)
                    st.download_button("Download Results as CSV", results_df.to_csv(index=False), file_name="variant_scores.csv")
                if errors:
                    st.warning(f"{len(errors)} variants failed to score.")
                    for e in errors:
                        st.text(f"Row {e['row']}: {e['error']}")
        except Exception as ex:
            st.error(f"Error reading CSV: {ex}")

if __name__ == "__main__":
    page = st.sidebar.selectbox("Navigation", ["Scoring", "Dashboard"])
    if page == "Scoring":
        main()
    else:
        show_dashboard()
