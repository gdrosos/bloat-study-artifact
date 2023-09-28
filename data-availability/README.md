# Supplementary Material for "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis"

This repository contains supplementary material for the research paper submitted to FSE'2024 titled "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis".

## Directory Structure

### [dependency_data/](./dependency_data/)
- `direct_dependencies.json`: A JSON file mapping each GitHub project to its direct dependency declarations.
- `resolved_dependencies.json`: Maps each of the 1302 GitHub projects to 21787 resolved direct and transitive dependencies, accounting for 3,232 unique PyPI releases.

### [callgraphs](./callgraphs)
- Contains a sample number of JSON files representing the stitched call graphs of Python GitHub projects.
Due to size restrictions,
we have included a subset,
specifically the call graphs of projects whose name starts with the letter 'p'
(150 in total).
The call graphs are structured as `{github_owner}/{repository_name}/cg.json`.

### [results](./results/)
- `qualitative_analysis.json`: Contains the results of our qualitative analysis for RQ3 and RQ4, providing for each GitHub project and specific direct dependency the manually assigned cause category, the link to the pull request, and the status of the pull request.
- `results_rq1.csv`, `results_rq1b.csv`, `results_rq2.csv`, `results_rq2b.csv`:  Contain the quantitative analysis results for the corresponding research questions.

### [vulnerability_data/](./vulnerability_data/)
- `projects_vulnerabilities.json`: Lists the 599 projects depending on at least one vulnerable package, along with their vulnerable dependencies and the specific [GHSA ID](https://github.com/github/advisory-database#ghsa-ids) affecting each dependency.

## Usage

These datasets and results are provided as supplementary material to validate and further explore the findings of our research on bloated dependnency code within the PyPI ecosystem.

## Data Availability

Upon acceptance of the paper,
we intend to make the data publicly available on zenodo
to facilitate future research and replication of our study.