#!/bin/bash

TOKEN=$1
DEST_DIR=$2
DEP_FILE_PRE=$3
DEP_FILE_POST=$4
case "$TOKEN" in
    data*)
        echo "Error: It appears that the GitHub Token has not been properly set as an environment variable."
        echo "Please ensure that you have properly set up your Github Access Token"
        exit 1
        ;;
esac
CURRENT_DIR=$(pwd)
echo Cloning PyCG repository...
git clone https://{$TOKEN}@github.com/gdrosos/PyCG.git
cd PyCG
pip3 install .
PATH="$HOME/.local/bin:$PATH"
cd ..
rm -rf PyCG
echo Starting Partial Call Graph Generation of Github Projects...
python scripts/partial_cg_generation/produce_project_partial_cg.py  --source  $DEST_DIR --json  $DEP_FILE_PRE
python  scripts/partial_cg_generation/merge_json.py  -d $DEST_DIR --json  $DEP_FILE_PRE -o intermediate.json --project
echo Starting Partial Call Graph Generation of Project Dependencies...
python scripts/partial_cg_generation/produce_dep_partial_cg.py --source $DEST_DIR --json intermediate.json
python  scripts/partial_cg_generation/merge_json.py  -d $DEST_DIR --json  intermediate.json -o $DEP_FILE_POST
rm intermediate.json
rm -rf tmp1
echo Finished Partial Call Graph Generation