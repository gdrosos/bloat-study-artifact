#!/bin/bash

TOKEN=$1
DEST_DIR=$2
DEP_FILE_PRE=$3
DEP_FILE_POST=$4


git clone https://{$TOKEN}@github.com/gdrosos/PyCG.git
cd PyCG
pip3 install .
cd ..
rm -rf PyCG
python3 scripts/partial_cg_generation/produce_project_partial_cg.py  --source  $DEST_DIR --json  $DEP_FILE_PRE
python3  scripts/partial_cg_generation/merge_json.py  -d $DEST_DIR --json  $DEP_FILE_PRE -o intermediate.json --project
python3 scripts/partial_cg_generation/produce_dep_partial_cg.py --source $DEST_DIR --json intermediate.json
python3  scripts/partial_cg_generation/merge_json.py  -d $DEST_DIR --json  intermediate.json -o $DEP_FILE_POST
rm intermediate.json