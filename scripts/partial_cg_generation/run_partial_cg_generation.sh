#!/bin/bash

TOKEN=$1
DEST_DIR=$2
DEP_FILE_PRE=$3
DEP_FILE_POST=$4

CURRENT_DIR=$(pwd)
git clone https://{$TOKEN}@github.com/gdrosos/PyCG.git
cd PyCG
pip3 install .
PATH="$HOME/.local/bin:$PATH"
cd ..
rm -rf PyCG
python scripts/partial_cg_generation/produce_project_partial_cg.py  --source  $DEST_DIR --json  $DEP_FILE_PRE
python  scripts/partial_cg_generation/merge_json.py  -d $DEST_DIR --json  $DEP_FILE_PRE -o intermediate.json --project
python scripts/partial_cg_generation/produce_dep_partial_cg.py --source $DEST_DIR --json intermediate.json
python  scripts/partial_cg_generation/merge_json.py  -d $DEST_DIR --json  intermediate.json -o $DEP_FILE_POST
rm intermediate.json
rm -rf tmp1