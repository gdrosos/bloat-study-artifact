#!/bin/bash

TOKEN=$1
SEC_PATH=$2
JSON=$3

git clone https://{$TOKEN}@github.com/github/advisory-database.git $SEC_PATH/advisory-database
python3 scripts/security_analysis/get_github_vulnerabilities.py  --gad_path $SEC_PATH -o  $SEC_PATH/pypi_vulnerabilities.csv  
python3 scripts/security_analysis/find_affected_dependencies.py  -json $JSON -cves  $SEC_PATH/pypi_vulnerabilities.csv   -o  $SEC_PATH/vulnerable_dependencies.json 
python3 scripts/security_analysis/calculate_stats.py -json $JSON -cves   $SEC_PATH/vulnerable_dependencies.json   -o  $SEC_PATH/project_vulnerabilities.json


