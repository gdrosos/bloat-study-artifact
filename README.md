# README for Research Artifact

## Introduction
This repository contains the research artifacts related to our paper.
The artifacts are organized into different directories, each serving a specific purpose in the research.

## Directory Structure

.
│
├── analysis/
│ ├── data/
│ │ ├── qualitative_results.json
│ │ ├── results_rq1b.csv
│ │ ├── results_rq1.csv
│ │ ├── results_rq2b.csv
│ │ └── results_rq2.csv
│ ├── rq1b.ipynb
│ ├── rq1.ipynb
│ ├── rq2b.ipynb
│ ├── rq2.ipynb
│ ├── rq3.ipynb
│ └── rq4.ipynb
│
└── data/
├── initial_dataset.csv
├── product_to_install_requires.json
├── projects2dependencies.json
├── rq2/
│ ├── project_vulnerabilities.json
│ └── vulnerability_version_constraints.csv
└── call_graphs/
└── p* (all stitched call graphs of projects starting with 'p')



## Directory Descriptions

### `analysis/`
This directory contains notebooks for visualizations and tables, along with data used for the results of our paper.

- `data/` contains:
  - `qualitative_results.json`: [Description]
  - `results_rq1b.csv`: [Description]
  - `results_rq1.csv`: [Description]
  - `results_rq2b.csv`: [Description]
  - `results_rq2.csv`: [Description]

- Notebooks (`rq1b.ipynb`, `rq1.ipynb`, `rq2b.ipynb`, `rq2.ipynb`, `rq3.ipynb`, `rq4.ipynb`) provide visualizations and tables based on the analysis.

### `data/`
This directory hosts various datasets and information utilized in our research.

- `initial_dataset.csv`: The initial dataset used as an entry point from the X paper.
- `product_to_install_requires.json`: Maps each GitHub project to a list of the declared direct dependencies (install requires).
- `projects2dependencies.json`: A JSON file mapping every GitHub project with a set of resolved transitive and direct dependencies (package:versions).

- `rq2/` directory contains:
  - `project_vulnerabilities.json`: Showcases all the vulnerable projects having vulnerable dependencies.
  - `vulnerability_version_constraints.csv`: Contains the vulnerability information fetched from GitHub.

- `call_graphs/`: Contains all the stitched call graphs of projects names starting with the letter 'p'.
