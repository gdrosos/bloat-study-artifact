#!/bin/bash

# Assign command line arguments to variables
GITHUB_TOKEN=$1
DEST_DIR=$2
SUBSET=$3

if [ "$SUBSET" = "subset" ]; then
    echo "Processing sample dataset..."
    python3 clone_repos.py -t $GITHUB_TOKEN  -f ../../data/sample_projects.csv -d $DEST_DIR
    python3.9 dependency_resolver.py -f ../../data/sample_projects.csv -d $DEST_DIR
    python3.9 merge_json.py -d $DEST_DIR -o project_dependencies_subset.json
else
    echo "Processing full dataset..."
    wget -O dataset.zip https://zenodo.org/records/5645517/files/dataset-package.zip?download=1
    unzip dataset.zip 
    awk -F"," 'NR > 1 {print $1}' dataset-package/python-projects-dataset.csv  > python_projects.csv
    python3 clone_repos.py -t $GITHUB_TOKEN  -f python_projects.csv -d $DEST_DIR
    python3.9 dependency_resolver.py -f python_projects.csv -d $DEST_DIR
    python3.9 merge_json.py -d $DEST_DIR -o project_dependencies.json
fi
echo "Dependency resolution completed."
