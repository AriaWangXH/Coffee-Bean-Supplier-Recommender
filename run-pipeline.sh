#!/usr/bin/env bash

# Generate features
python3 src/generate_features.py --input=data/external/merged_data_cleaned.csv --config=config/config.yaml --output=data/data_clean.csv

# Train model
python3 src/train_model.py --input=data/data_clean.csv --config=config/config.yaml --output=ddata/clusters.csv

# Evaluate model
python3 src/evaluate_model.py --input=data/clusters.csv --config=config/config.yaml --output=figures/model_evaluation/cluster_counts.csv