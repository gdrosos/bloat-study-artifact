# Supplementary Material for "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis"
This is the artifact for the paper accepted to FSE'24 titled:
"Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis.

## Directory Structure

### [project-data](./project-data/)
- `project_dependencies.json`: Json file mapping each of the 1302 GitHub projects to its set of resolved dependencies, accounting for 3,232 unique PyPI releases.

### [callgraphs](./callgraphs)
- Contains a sample number of JSON files representing the stitched call graphs of Python GitHub projects.
Due to size restrictions,
we have included a subset,
specifically the call graphs of projects whose owner name starts with the letter 'p'
(150 in total).
The call graphs are structured as `{github_owner}/{repository_name}/cg.json`.

### [results](./results/)
#### rq1a.csv: 
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

#### `rq1b.csv`: 
- For each Python project, it includes the different usage statuses of its direct and transitive dependencies, showcasing metrics related to bloat and usage in various granularities (RQ1).

  - Columns:
    - `project`: Github Owner-Repository Name.
    
    #### Direct Dependencies:
    - `direct_dependencies_bloated_count`: Number of bloated direct dependencies.
    - `direct_dependencies_bloated_loc`: Lines of code in bloated direct dependencies.
    - `direct_dependency_files_bloated_count`: Number of bloated files in direct dependencies.
    - `direct_dependency_files_bloated_loc`: Lines of code in the bloated files of direct dependencies.
    - `direct_dependency_methods_bloated_count`: Number of bloated methods in direct dependencies.
    - `direct_dependency_methods_bloated_loc`: Lines of code in the bloated methods of direct dependencies.
    - `direct_dependencies_used_count`: Number of used direct dependencies.
    - `direct_dependencies_used_loc`: Lines of code in used direct dependencies.
    - `direct_dependency_files_used_count`: Number of used files in direct dependencies.
    - `direct_dependency_files_used_loc`: Lines of code in the used files of direct dependencies.
    - `direct_dependency_methods_used_count`: Number of used methods in direct dependencies.
    - `direct_dependency_methods_used_loc`: Lines of code in the used methods of direct dependencies.
        
    #### Transitive Dependencies:
    - `transitive_dependencies_bloated_count`: Number of bloated transitive dependencies.
    - `transitive_dependencies_bloated_loc`: Lines of code in bloated transitive dependencies.
    - `transitive_dependency_files_bloated_count`: Number of bloated files in transitive dependencies.
    - `transitive_dependency_files_bloated_loc`: Lines of code in the bloated files of transitive dependencies.
    - `transitive_dependency_methods_bloated_count`: Number of bloated methods in transitive dependencies.
    - `transitive_dependency_methods_bloated_loc`: Lines of code in the bloated methods of transitive dependencies.
    - `transitive_dependencies_used_count`: Number of used transitive dependencies.
    - `transitive_dependencies_used_loc`: Lines of code in used transitive dependencies.
    - `transitive_dependency_files_used_count`: Number of used files in transitive dependencies.
    - `transitive_dependency_files_used_loc`: Lines of code in the used files of transitive dependencies.
    - `transitive_dependency_methods_used_count`: Number of used methods in transitive dependencies.
    - `transitive_dependency_methods_used_loc`: Lines of code in the used methods of transitive dependencies.

#### `rq2a.csv`: 
- Contains the quantitative results for the second research question (RQ2), including all Python projects having vulnerable dependencies. Each row specifies a dependency from a project to a vulnerable dependency.
  - Columns:
    - `project`: Github Owner-Repository Name, representing the Python project.
    - `package_name`: Specifies the name of the PyPI package identified as a vulnerable dependency.
    - `dependency_type`: Distinguishes whether the vulnerable package is a direct or transitive dependency of the project.
    - `activation_status`: Indicates the invokation status of the dependency, specifying whether it is a bloated dependency, active, inactive, or undefined.

#### `rq2b.csv`: 
- Contains metrics regarding the usage of inactive (used with bloated vulnerable method) and active vulnerable packages witihn each Python project (RQ2). Each row describes a project’s interaction with a vulnerable dependency,  and more precicely the extent of bloat and usage in both the  files and methods of this dependency.

  - Columns:
    - `project`: Github Owner-Repository Name, signifying the particular Python project being analyzed.
    - `package_name`: Specifies the name of the PyPI package identified as a vulnerable dependency.
    - `activation_status`: Indicates the invokation status of the dependency, specifying whether it is active or inactive.
    - `bloated_files`: Quantifies the number of bloated files present in the vulnerable dependency.
    - `used_files`: Enumerates the number of files from the vulnerable dependency that are actually utilized in the project.
    - `bloated_methods`: Enumerates the number of bloated methods present in the vulnerable dependency.
    - `used_methods`: Measures the number of methods from the vulnerable dependency that are actually utilized in the project.
    - `percentage_bloated_methods`: Calculates the percentage of bloated methods within the methods of the vulnerable dependency.
    - `percentage_bloated_files`: Computes the percentage of bloated files within the files of the vulnerable dependency.


#### `rq3.json`: 
- Contains the results of the qualitative analysis (RQ3) identifying  the root causes for the 50 selected bloated dependencies.


## Usage

These datasets and results are provided as supplementary material to validate and further explore the findings of our research on bloated dependency code within the PyPI ecosystem.

# Step-by-Step Instructions

In the following section, we provide instructions
for reproducing the results
presented in the paper using the data coming from the `data/` directory.

## RQ1: Bloat Prevalence (Section 3.1)

In the first research question,
we compute the prevalence of dependency bloat across different granularities.

To produce the results of Figure 5, simply run:

```bash
python scripts/rq1.py data/results/rq1a.csv --output figures/bloat_prevalence.pdf
```

The above command produces the figure `figures/bloat_prevalence.pdf` (Figure 5)
and prints the following tables in the standard output:

```
Absolute value bloat metric stats:

           NBD      NBFD        NBMD      NBD-LOC     NBFD-LOC     NBMD-LOC
count  1302.00   1302.00     1302.00      1302.00      1302.00      1302.00
mean     10.14    688.73    10618.03     98097.10    243156.10    185052.14
std      14.43    880.18    13086.86    175217.62    328677.30    245717.72
min       0.00      0.00        0.00         0.00         0.00         0.00
25%       2.00     95.00     1550.00      4748.00     32785.25     24963.50
50%       5.00    339.00     5619.50     24024.00    120311.50     95047.00
75%      13.00    983.00    14832.50    123269.25    329135.00    248139.00
max     139.00   8390.00    99702.00   1452702.00   2567201.00   1872912.00
Sum   13206.00 896731.00 13824676.00 127722424.00 316589243.00 240937888.00

Percentage value bloat metric stats (Fig. 5):

                              Count  Mean   Std  Min   25%   50%   75%    Max
Granularity Metric                                                           
File        Bloated LoC     1302.00 78.49 17.92 0.00 70.69 81.52 90.83 100.00
            Bloated entries 1302.00 87.36 12.97 0.00 83.55 90.08 95.01 100.00
Method      Bloated LoC     1302.00 93.52  7.83 0.00 91.48 95.07 98.33 100.00
            Bloated entries 1302.00 95.41  6.07 0.00 94.21 96.80 98.71 100.00
Package     Bloated LoC     1302.00 34.39 32.28 0.00  5.93 24.78 52.93 100.00
            Bloated entries 1302.00 51.67 27.70 0.00 33.33 50.00 69.23 100.00
```


**Note**: The first table presents descriptive statistics regarding the absolute values of the bloat metrics.
The acronym of each metric is described in detail [here](#rq1a.csv).
Some of those total and average numbers are utilized in Section 3.1 of our paper
(e.g. {Total, average} number of bloated {dependencies, files, methods}, in the context of entries or LoC).