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
#### `rq1a.csv`: 
- Contains the quantitative analysis results for the first research question (RQ1), focusing especially on the prevalence of bloat at different granularities in the Python projects.
  - Columns:
    - `project`: Github Owner-Repository Name.
    - `NBD`: Number of Bloated Dependencies – Represents the number of bloated dependencies identified in the project.
    - `NBFD`: Number of Bloated Files in Dependencies – Signifies the count of bloated files identified within the dependencies of the project.
    - `NBMD`: Number of Bloated Methods in Dependencies – Indicates the count of bloated methods found within the dependencies of the project.
    - `NBD-LOC`: Number of Bloated Dependencies in LOC - Denotes the lines of code (LOC) in the bloated dependencies.
    - `NBFD-LOC`: Number of Bloated Files in Dependencies in LOC - Represents the lines of code (LOC) in the bloated files of the dependencies.
    - `NBMD-LOC`: Number of Bloated Methods in Dependencies in LOC - Represents the number of lines of code (LOC) in the bloated methods of the dependencies.
    - `PBD`: Percentage of Bloated Dependencies – Represents the proportion of dependencies that are identified as bloated in the project.
    - `PBFD`: Percentage of Bloated Files in Dependencies – Represents the proportion of files within the dependencies that are identified as bloated.
    - `PBMD`: Percentage of Bloated Methods in Dependencies – Represents the proportion of methods within the dependencies of the project that are identified as bloated.
    - `PBD-LOC`: Percentage of Bloated Dependencies in LOC - Represents the percentage of lines of code (LOC) in dependencies that are bloated
    - `PBFD-LOC`: Percentage of Bloated Files in Dependencies in LOC - Represents the percentage of lines of code (LOC) in dependency files that are bloated.
    - `PBMD-LOC`: Percentage of Bloated Methods in Dependencies in LOC - Represents the percentage of lines of code (LOC) in dependency methods that are bloated.
-  `rq1b.csv`, `rq2a.csv`, `rq2b.csv`:  Contain the quantitative analysis results to answer the  RQ1 & RQ2 research questions.
#### `rq3.json`:  Contains the results of the qualitative analysis (RQ3) identifying  the root causes for the 50 selected bloated direct dependencies.


## Usage

These datasets and results are provided as supplementary material to validate and further explore the findings of our research on bloated dependency code within the PyPI ecosystem.

## Data Availability

Upon acceptance of the paper,
we intend to make the data publicly available on Zenodo
to facilitate future research and replication of our study.