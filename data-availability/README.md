# Supplementary Material for "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis"

This repository contains supplementary material for our research paper, "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis".

## Directory Structure

### [call_graph_samples/](./call_graph_samples/)
- Contains sample call graphs of Python projects.

### [analysis_results/](./analysis_results/)
- `qualitative_analysis.json`: Contains the qualitative analysis results.
- `results_rq1.csv`, `results_rq1b.csv`, `results_rq2.csv`, `results_rq2b.csv`: Contain the quantitative analysis results for corresponding research questions.

### [dependency_data/](./dependency_data/)
- `direct_dependencies.json`: Maps each GitHub project to its list of direct dependencies.
- `resolved_dependencies.json`: Maps each GitHub project to a set of resolved direct and transitive dependencies.

### [vulnerability_data/](./vulnerability_data/)
- `projects_vulnerabilities.json`: Contains information on project vulnerabilities with dependencies as keys and vulnerabilities CVEs as values.

## Usage

These datasets and results are provided as supplementary material to validate and further explore the findings of our research on bloated dependnency code within the PyPI ecosystem.

## Data Availability

Upon acceptance of the paper,
we intend to make the data publicly available on zenodo
to facilitate future research and replication of our study.