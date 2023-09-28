# Supplementary Material for "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis"

This repository contains supplementary material for the research paper submitted to FSE'2024 titled "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis".

## Directory Structure

### [project-data](./project-data/)
- `project_dependencies.json`: Maps each of the 1302 GitHub projects to 21787 resolved direct and transitive dependencies, accounting for 3,232 unique PyPI releases.
- `projects_vulnerabilities.json`: Lists the 599 projects depending on at least one vulnerable package, along with their vulnerable dependencies and the specific [GHSA ID](https://github.com/github/advisory-database#ghsa-ids) affecting each dependency.


### [callgraphs](./callgraphs)
- Contains a sample number of JSON files representing the stitched call graphs of Python GitHub projects.
Due to size restrictions,
we have included a subset,
specifically the call graphs of projects whose name starts with the letter 'p'
(150 in total).
The call graphs are structured as `{github_owner}/{repository_name}/cg.json`.

### [results](./results/)
- `rq1.csv`, `rq1b.csv`, `rq2.csv`, `rq2b.csv`:  Contain the quantitative analysis results for the  RQ1 & RQ2 research questions.

## Usage

These datasets and results are provided as supplementary material to validate and further explore the findings of our research on bloated dependnency code within the PyPI ecosystem.

## Data Availability

Upon acceptance of the paper,
we intend to make the data publicly available on zenodo
to facilitate future research and replication of our study.