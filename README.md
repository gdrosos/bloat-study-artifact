# Artifact for for "Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis"
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
- Contains metrics regarding the usage of inactive (used with bloated vulnerable method) and active vulnerable packages within each Python project (RQ2). Each row describes a project’s interaction with a vulnerable dependency,  and more precisely the extent of bloat and usage in both the files and methods of this dependency.

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

## Methodology

### Call Graph Stitching

### Reachability Analysis


#### Final Dataset Retrieval

**NOTE:** Ensure that you have at least 10GB of available disk space before running this step.

To obtain the stitched call graphs of the 1302 Python Applications, as well as the bloat metrics correspondng to each project,
you can fetch the data from zenodo. First run:

`wget -O stitched_cg_data.zip "https://zenodo.org/records/11077253/files/stitched_callgraphs.zip?download=1"`

To extract the data, run:

`unzip stitched_cg_data.zip `

this will create the directory `stitched_callgraphs`. This directory is structured into directories for each of the analyzed projects.
Each sub-directory is named using the pattern `repo_name/project_name/` and contains several JSON files detailing the stitched call graphs and various metrics analyses.

##### File Descriptions

- **`cg.json`**: Contains the stitched call graph for the project, integrating multiple call graphs from direct and transitive dependencies to form a comprehensive view of the project’s call architecture.

- **`bloat_metrics.json`**: Contains individual project-specific results from the reachability analysis, measuring various aspects of code bloat such as the number of bloated dependencies, files, and methods, along with their corresponding lines of code. Each record from these JSON files has been systematically aggregated into the [rq1a.csv](#rq1acsv), which is used in subsequent steps to produce Figure 5.


- **`bloat_metrics_direct_vs_transitive.json`**: Contains individual project-specific code bloat metrics comparing direct vs transitive dependencies from the reachability analysis. Each record from these JSON files has been systematically aggregated into the [rq1b.csv](#rq1bcsv), which is used in subsequent steps to produce Figure 7.

- **`security_metrics.json`**: Available only for projects with reachable vulnerable dependencies. It includes metrics on dependency bloat concerning vulnerable code. The data in this file are systematically aggregated and used to populate both the [rq2a.csv](#rq2acsv) and [rq2b.csv](#rq2bcsv) files, which facilitate the analysis and presentation of the results for RQ2.

###### Example Directory Structure

For a project named `datadogpy` under the `datadog` repository, the directory structure would be:
```
datadog/datadogpy/
├─ cg.json
├─ bloat_metrics.json
├─ bloat_metrics_direct_vs_transitive.json
└─ security_metrics.json (if applicable)
```




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
The acronym of each metric is described in detail [here](#rq1acsv).
Some of those total and average numbers are utilized in Section 3.1 of our paper
(e.g. {Total, average} number of bloated {dependencies, files, methods}, in the context of entries or LoC).

Moreover, to produce Figure 7, simply run:

```bash
python scripts/rq1_dep_comp.py data/results/rq1b.csv --output figures/bloat_prevalence_direct_vs_transitive.pdf
```

The above command produces the figure `figures/bloat_prevalence_direct_vs_transitive.pdf` (Figure 7)
and prints the following stats in the standard output:

```
Number of dependencies

Direct bloated      : 5.69%
Transitive bloated  : 52.99%
Direct used         : 22.71%
Transitive used     : 18.61%

Number of files

Direct bloated      : 44.86%
Transitive bloated  : 45.72%
Direct used         : 6.41%
Transitive used     : 3.02%

Number of functions

Direct bloated      : 47.87%
Transitive bloated  : 48.13%
Direct used         : 2.74%
Transitive used     : 1.26%

Size of dependencies (LoC)

Direct bloated      : 4.45%
Transitive bloated  : 24.36%
Direct used         : 47.76%
Transitive used     : 23.42%

Size of files (LoC)

Direct bloated      : 38.06%
Transitive bloated  : 40.94%
Direct used         : 14.15%
Transitive used     : 6.84%

Size of functions(LoC)

Direct bloated      : 49.55%
Transitive bloated  : 44.19%
Direct used         : 4.21%
Transitive used     : 2.05%
```

## RQ2: Security Impact (Section 3.2)

In the second research question,
we explore the relation between bloated dependency code and software
vulnerabilities.
To produce Figure 8 of our paper, simply run:

```bash
python scripts/rq2.py data/results/rq2a.csv --output figures/vulnerable_dep_usage_status.pdf 
```


The above command produces the figure `figures/vulnerable_dep_usage_status.pdf` (Figure 8)
and prints the following data in the standard output:

```
Vulnerable Dependency Activation Status:

dependency_type                Direct  Transitive  Total
activation_status                                       
Active                             20           6     26
Inactive (bloated dependency)      41         565    606
Inactive (bloated method)          84          38    122
Undefined                          26          36     62
Total                             171         645    816

Number of projects depending on at least one vulnerable release: 595
```

Moreover, to compute the distribution of bloat metrics per vulnerability exposure and produce Figure 6 of our paper,
simply run:
```bash
python scripts/rq2_bloat_metrics.py data/results/rq2b.csv --output figures/bloat_metric_per_exposure.pdf 
```

The above command produces the figure `figures/bloat_metric_per_exposure.pdf` (Figure 6)
and prints the following data in the standard output:


```
Distribution of bloat metrics per vulnerability exposure:
                          count  mean   std   min   25%   50%   75%   max
metric          Status                                                   
Bloated files   Active    26.00 63.47 16.36 38.89 55.46 64.44 77.25 87.50
                Inactive 123.00 80.22 12.53 33.33 68.82 82.98 88.89 98.61
Bloated methods Active    26.00 85.07 12.62 62.66 79.79 90.02 94.61 97.97
                Inactive 123.00 94.59  6.86 48.15 94.02 96.51 98.59 99.92
```

## RQ3: Root Causes (Section 3.3)

In this research question we manually classify
the root causes of 50 bloated dependencies
and report our results,
as depicted on Figure 9.

To produce Figure 9, simply run:

```bash
python scripts/rq3.py data/results/qualitative_results.json  --output figures/root_cause_distribution.pdf
```

The above command produces the figure `figures/root_cause_distribution.pdf` (Figure 9)
and prints the following data in the standard output:

```
Root Cause Distribution:
--------------------------------------------
Built-in or alternate library: 9/50 (18.00%)
Unused from the first time: 8/50 (16.00%)
Feature removal: 10/50 (20.00%)
Transitive dependency: 15/50 (30.00%)
Security constraint: 5/50 (10.00%)
Compatibility constraint: 3/50 (6.00%)
```

## RQ3: Developer Perception (Section 3.4)

In the last research question, we investigate developer's perception on dependency bloat.
To reproduce table 3, simply run:

```bash
python scripts/rq4.py data/results/qualitative_results.json --table3
```

The command will print the following table in the standard output:


```
+-------------+-----------------+-------------------------+
| PR Status   |   Number of PRs |   Number of  BD removed |
+=============+=================+=========================+
| Merged      |              30 |                      35 |
+-------------+-----------------+-------------------------+
| Approved    |               1 |                       1 |
+-------------+-----------------+-------------------------+
| Pending     |               4 |                       5 |
+-------------+-----------------+-------------------------+
| Rejected    |               1 |                       1 |
+-------------+-----------------+-------------------------+
| Total       |              36 |                      42 |
+-------------+-----------------+-------------------------+

Number of LoC removed: 393837
```

In addition, the above command will measure and output the number of LoC removed, which
is reported on Section 3.4.

Moreover, to reproduce Figure 10, run:


```bash
python scripts/rq4.py data/results/qualitative_results.json --output_fig_10 figures/pr_per_root_cause.pdf
```

The above command produces the figure `figures/pr_per_root_cause.pdf` (Figure 10)
and prints the following table in the standard output:

```
+-------------------------------+-------------+---------+
| Root Cause                    | PR Status   |   Count |
+===============================+=============+=========+
| Built-in or alternate library | Approved    |       0 |
+-------------------------------+-------------+---------+
| Built-in or alternate library | Merged      |       9 |
+-------------------------------+-------------+---------+
| Built-in or alternate library | Pending     |       0 |
+-------------------------------+-------------+---------+
| Built-in or alternate library | Rejected    |       0 |
+-------------------------------+-------------+---------+
| Feature removal               | Approved    |       0 |
+-------------------------------+-------------+---------+
| Feature removal               | Merged      |       9 |
+-------------------------------+-------------+---------+
| Feature removal               | Pending     |       1 |
+-------------------------------+-------------+---------+
| Feature removal               | Rejected    |       0 |
+-------------------------------+-------------+---------+
| Transitive dependency         | Approved    |       1 |
+-------------------------------+-------------+---------+
| Transitive dependency         | Merged      |      11 |
+-------------------------------+-------------+---------+
| Transitive dependency         | Pending     |       3 |
+-------------------------------+-------------+---------+
| Transitive dependency         | Rejected    |       0 |
+-------------------------------+-------------+---------+
| Unused from the first time    | Approved    |       0 |
+-------------------------------+-------------+---------+
| Unused from the first time    | Merged      |       6 |
+-------------------------------+-------------+---------+
| Unused from the first time    | Pending     |       1 |
+-------------------------------+-------------+---------+
| Unused from the first time    | Rejected    |       1 |
+-------------------------------+-------------+---------+
```

In the same manner, to reproduce Figure 11, run:


```bash
python scripts/rq4.py data/results/qualitative_results.json --output_fig_11 figures/pr_durations.pdf
```

The above command produces the figure `figures/pr_durations.pdf` (Figure 11)
and prints the following data in the standard output:

```
Pull Requests Merged on the Same Date: 5
Pull Requests Merged Within Week: 6
Pull Requests Merged Within Month: 9
Pull Requests Merged more than Month: 10
```

Finally, to reproduce Figure 12, run:

```bash
python scripts/rq4.py data/results/qualitative_results.json --output_fig_12 figures/pr_discussions.pdf
```

The above command produces the figure `figures/pr_discussions.pdf` (Figure 12)
and prints the following data in the standard output:

```
Merged PRs requiring no discussion: 21
Merged PRs requiring discussions involving changes: 6
Merged PRs requiring discussions without requiring changes: 3
```