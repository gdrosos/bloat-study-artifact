#!/bin/bash

# Assign command line arguments to variables
GITHUB_TOKEN=$1
DEST_DIR=$2
SUBSET=$3
case "$GITHUB_TOKEN" in
    data*)
        echo "Error: It appears that the GitHub Token has not been properly set as an environment variable."
        echo "Please ensure that you have properly set up your Github Access Token"
        exit 1
        ;;
esac
if [ "$SUBSET" = "subset" ]; then
    echo "Processing sample dataset..."
    python scripts/dependency_resolution/clone_repos.py -t $GITHUB_TOKEN  -f $DEST_DIR/sample_projects.csv -d $DEST_DIR/sources/apps
    python scripts/dependency_resolution/dependency_resolver.py -f $DEST_DIR/sample_projects.csv -d $DEST_DIR/sources/apps
    python scripts/dependency_resolution/merge_json.py -d $DEST_DIR -o $DEST_DIR/project_dependencies_subset.json
else
    echo "Processing full dataset..."
    wget -O dataset.zip https://zenodo.org/records/5645517/files/dataset-package.zip?download=1
    unzip dataset.zip 
    awk -F"," 'NR > 1 {print $1}' dataset-package/python-projects-dataset.csv  > $DEST_DIR/python_projects.csv
    python scripts/dependency_resolution/clone_repos.py -t $GITHUB_TOKEN  -f $DEST_DIR/python_projects.csv -d $DEST_DIR/sources/apps
    python scripts/dependency_resolution/dependency_resolver.py -f $DEST_DIR/python_projects.csv -d $DEST_DIR/sources/apps
    python scripts/dependency_resolution/merge_json.py -d $DEST_DIR -o $DEST_DIR/project_dependencies.json
fi
echo "Dependency resolution completed."
