-- PostgreSQL schema for variant and annotation storage
CREATE TABLE variant (
    id SERIAL PRIMARY KEY,
    gene TEXT,
    transcript TEXT,
    protein_change TEXT,
    genome_build TEXT,
    tumor_type TEXT,
    tmb FLOAT,
    prior_therapy_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE annotation (
    id SERIAL PRIMARY KEY,
    variant_id INT REFERENCES variant(id),
    oncokb_level TEXT,
    cosmic_frequency FLOAT,
    clinical_impact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
