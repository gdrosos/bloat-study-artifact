# Supplementary Material for "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis"

This  document details the supplementary material for the research paper submitted to FSE'2024 titled "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis".

## Directory Structure

### [project-data](./project-data/)
- `project_dependencies.json`: Maps each of the 1302 GitHub projects to 21787 resolved direct and transitive dependencies, accounting for 3,232 unique PyPI releases.

### [callgraphs](./callgraphs)
- Contains a sample number of JSON files representing the stitched call graphs of Python GitHub projects.
Due to size restrictions,
we have included a subset,
specifically the call graphs of projects whose owner name starts with the letter 'p'
(150 in total).
The call graphs are structured as `{github_owner}/{repository_name}/cg.json`.

### [results](./results/)
- `rq1.csv`, `rq1b.csv`, `rq2.csv`, `rq2b.csv`:  Contain the quantitative analysis results to answer the  RQ1 & RQ2 research questions.
- `rq3.json`:  Contains the results of the qualitative analysis (RQ3) identifying  the root causes for the 50 selected bloated direct dependencies.


## Usage

These datasets and results are provided as supplementary material to validate and further explore the findings of our research on bloated dependency code within the PyPI ecosystem.

## Data Availability

Upon acceptance of the paper,
we intend to make the data publicly available on Zenodo
to facilitate future research and replication of our study.