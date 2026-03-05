# ---
# Synthetic Data Creation Documentation
#
# The synthetic variant data in this script was created manually to mimic real-world cancer genomics datasets.
#
# Step-by-step: How manual selection was performed
#
# 1. **Identify key cancer genes:**
#    - Reviewed public cancer genomics resources (COSMIC, OncoKB, ClinVar) to find genes most frequently mutated in cancer (e.g., TP53, EGFR, BRAF).
# 2. **Select representative mutations:**
#    - Chose well-known hotspot mutations for each gene (e.g., TP53 p.R175H, BRAF p.V600E) based on their prevalence and clinical relevance.
# 3. **Assign canonical transcript IDs:**
#    - Used Ensembl and NCBI Gene to find the most widely accepted transcript for each gene, ensuring consistency with clinical reporting standards.
# 4. **Pair with tumor types:**
#    - Matched each gene/mutation to a tumor type where it is commonly observed, referencing published studies and clinical guidelines.
# 5. **Set plausible numeric values:**
#    - Assigned tumor mutational burden (tmb) and prior therapy counts to reflect realistic patient scenarios, based on typical ranges in the literature.
# 6. **Review for diversity and realism:**
#    - Ensured the dataset covers a range of genes, mutations, tumor types, and numeric values to simulate real-world variety.
# 7. **No real patient data used:**
#    - All records were constructed from scratch for safe development and testing, with no direct copying from any patient or database record.
#
# This process ensures the synthetic data is realistic, diverse, and safe for development, while being fully transparent and reproducible.
#
# - Gene names, transcript IDs, and protein changes were selected based on well-known cancer driver genes and hotspot mutations
#   (e.g., TP53 p.R175H, BRAF p.V600E) as cataloged in public resources such as COSMIC, OncoKB, and ClinVar.
# - Canonical transcript IDs were chosen to match the most commonly referenced transcripts for each gene.
# - Tumor types were paired with gene/mutation combinations according to their established clinical associations in the literature.
# - Numeric fields (e.g., tmb, prior_therapy_count) were assigned plausible values to simulate realistic patient scenarios.
# - No real patient data was used; all records were constructed for development and testing purposes only.
#
# Useful resources for reference:
#   COSMIC:   https://cancer.sanger.ac.uk/cosmic
#   OncoKB:   https://www.oncokb.org/
#   ClinVar:  https://www.ncbi.nlm.nih.gov/clinvar/
#   Ensembl:  https://www.ensembl.org/
#   NCBI Gene: https://www.ncbi.nlm.nih.gov/gene/
#   PubMed:   https://pubmed.ncbi.nlm.nih.gov/
#
# This approach allows safe, reproducible development and testing before integrating real-world data.
# ---
# Script to generate synthetic variant data for testing
import csv


header = ["gene", "transcript", "protein_change", "genome_build", "tumor_type", "tmb", "prior_therapy_count"]
data = [
    ["TP53", "NM_000546.5", "p.R175H", "GRCh38", "lung_adenocarcinoma", 12.5, 2],
    ["EGFR", "NM_005228.3", "p.L858R", "GRCh38", "lung_adenocarcinoma", 8.1, 1],
    ["KRAS", "NM_033360.4", "p.G12D", "GRCh38", "colorectal_cancer", 6.7, 0],
    ["ALK", "NM_004304.4", "p.F1174L", "GRCh38", "neuroblastoma", 15.2, 3],
    ["BRAF", "NM_004333.4", "p.V600E", "GRCh38", "melanoma", 18.9, 1],
    ["PIK3CA", "NM_006218.3", "p.E545K", "GRCh38", "breast_cancer", 9.3, 2],
    ["NRAS", "NM_002524.4", "p.Q61R", "GRCh38", "thyroid_cancer", 5.4, 0],
    ["IDH1", "NM_005896.3", "p.R132H", "GRCh38", "glioma", 3.2, 1],
    ["PTEN", "NM_000314.6", "p.R130Q", "GRCh38", "endometrial_cancer", 7.8, 2],
    ["CDKN2A", "NM_000077.4", "p.A148T", "GRCh38", "pancreatic_cancer", 11.0, 1],
    ["MET", "NM_000245.3", "p.D1228N", "GRCh38", "lung_adenocarcinoma", 13.5, 2],
    ["ERBB2", "NM_004448.3", "p.S310F", "GRCh38", "breast_cancer", 10.1, 0],
    ["FGFR3", "NM_000142.4", "p.S249C", "GRCh38", "bladder_cancer", 4.6, 1],
    ["KIT", "NM_000222.3", "p.D816V", "GRCh38", "gastrointestinal_stromal_tumor", 16.7, 3],
    ["RET", "NM_020975.6", "p.M918T", "GRCh38", "medullary_thyroid_cancer", 2.9, 0],
]

with open("../data/synthetic_variants.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
