# Script to generate synthetic variant data for testing
import csv

header = ["gene", "transcript", "protein_change", "genome_build", "tumor_type", "tmb", "prior_therapy_count"]
data = [
    ["TP53", "NM_000546.5", "p.R175H", "GRCh38", "lung_adenocarcinoma", 12.5, 2],
    ["EGFR", "NM_005228.3", "p.L858R", "GRCh38", "lung_adenocarcinoma", 8.1, 1],
]

with open("../data/synthetic_variants.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
