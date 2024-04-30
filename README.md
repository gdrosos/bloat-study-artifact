# Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis
This is the artifact for the paper accepted to FSE'24 titled:
"Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis".

# Table of Contents
- [Bloat beneath Python’s Scales: A Fine-Grained Inter-Project Dependency Analysis](#bloat-beneath-pythons-scales-a-fine-grained-inter-project-dependency-analysis)
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
- [Getting Started](#getting-started)
- [Full Call Graph Dataset Retrieval (Optional)](#full-call-graph-dataset-retrieval-optional)
- [Step-by-Step Instructions](#step-by-step-instructions)
  - [Descriptive Tables (Sections 2.2 \& 2.3)](#descriptive-tables-sections-22--23)
  - [Results](#results)
    - [RQ1: Bloat Prevalence (Section 3.1)](#rq1-bloat-prevalence-section-31)
    - [RQ2: Security Impact (Section 3.2)](#rq2-security-impact-section-32)
    - [RQ3: Root Causes (Section 3.3)](#rq3-root-causes-section-33)
    - [RQ4: Developer Perception (Section 3.4)](#rq4-developer-perception-section-34)
  - [Methodology](#methodology)
    - [Project Selection and Dependency Resolution (Section 2.2)](#project-selection-and-dependency-resolution-section-22)
      - [Dependency Resolution of Full Dataset (Optional)](#dependency-resolution-of-full-dataset-optional)
      - [Dependency Resolution of a Subset Dataset](#dependency-resolution-of-a-subset-dataset)
    - [Partial Call Graph Construction (Section 2.3.1)](#partial-call-graph-construction-section-231)
      - [Partial Call Graph Generation of Full Dataset (Optional)](#partial-call-graph-generation-of-full-dataset-optional)
      - [Partial Call Graph Generation of Subset Dataset](#partial-call-graph-generation-of-subset-dataset)
    - [Stitching of Call Graphs \& Reachability Analysis (Sections 2.3.2 \& 2.3.3)](#stitching-of-call-graphs--reachability-analysis-sections-232--233)
      - [Stitching \& Reachability Analysis of Full Dataset (Optional)](#stitching--reachability-analysis-of-full-dataset-optional)
      - [Stitching \& Reachability Analysis of Subset Dataset](#stitching--reachability-analysis-of-subset-dataset)
    - [Analyzing Reachability Results: RQ2:Relation between software bloat and software vulnerabilities (2nd paragraph of Section 2.4):](#analyzing-reachability-results-rq2relation-between-software-bloat-and-software-vulnerabilities-2nd-paragraph-of-section-24)


# Dataset Description
The dataset of the artifact exists in the `data/` directory and has the following structure:
```
├── data
│   ├── results
│   │   ├── rq1a.csv
│   │   ├── rq1b.csv
│   │   ├── rq2a.csv
│   │   └── rq2b.csv
│   │   ├── qualitative_results.json
│   ├── project_dependencies_post_data_collection.json
│   ├── project_dependencies_final.json
│   ├── security
│   │   ├── project_vulnerabilities.json
│   │   ├── pypi_vulnerabilities.csv
│   │   ├── vulnerability2function.json
│   │   └── vulnerable_dependencies.json
│   └── subset
│       ├── sample_projects.csv
```
In the remaining part of this section, we describe the contents of each file:

- `results/`: This directory stores the bre-baked dataset of the automated and manual analysis performed in order to produce the results (numbers, figures, tables) reported on the results section of our paper (Sections 3.1-3.4)
  - `rq1a.csv`: Contains the quantitative analysis results for the first research question (RQ1), focusing especially on the prevalence of bloat at different granularities in the Python projects.
    - Columns:
      - `project`: GitHub Owner-Repository Name.
      - `NBD`: Number of Bloated Dependencies – Represents the number of bloated dependencies identified in the project.
      - `NBFD`: Number of Bloated Files in Dependencies – Measures the count of bloated files identified within the dependencies of the project.
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
      - `unique_unresolved_count`: The number of unique unresolved external calls during the Stitching process.
      - `unique_resolved_count`: The number of unique resolved external calls during the Stitching process.
      - `unresolved_count`: The total number of unresolved external calls during the Stitching process.
      - `resolved_count`: The total number of resolved external calls during the Stitching process.

- `rq1b.csv`: For each Python project, this file includes the different usage statuses of its direct and transitive dependencies, showcasing metrics related to bloat and usage in various granularities (RQ1).
  - Columns:
    - `product`: GitHub Owner-Repository Name.
    - `bloated_deps_count_1`: Number of bloated direct dependencies.
    - `bloated_deps_loc_1`: Lines of code in bloated direct dependencies.
    - `bloated_files_count_1`: Number of bloated files in direct dependencies.
    - `bloated_files_loc_1`: Lines of code in the bloated files of direct dependencies.
    - `bloated_functions_count_1`: Number of bloated functions in direct dependencies.
    - `bloated_functions_loc_1`: Total number of lines of code in the bloated functions of direct dependencies.
    - `used_direct_deps_count_1`: Number of used direct dependencies.
    - `used_direct_deps_count_1`: Lines of code in used direct dependencies.
    - `used_direct_files_count_1`: Number of used files in direct dependencies.
    - `used_direct_files_loc_1`: Lines of code in the used files of direct dependencies.
    - `used_direct_functions_count_1`: Number of used functions in direct dependencies.
    - `used_direct_functions_loc_1`: Lines of code in the used functions of direct dependencies.
    - `transitive_bloated_dependencies_count`: Number of bloated transitive dependencies.
    - `transitive_bloated_dependencies_loc`: Lines of code in bloated transitive dependencies.
    - `transitive_bloated_files_count`: Number of bloated files in transitive dependencies.
    - `transitive_bloated_files_loc`: Lines of code in the bloated files of transitive dependencies.
    - `transitive_bloated_functions_count`: Number of bloated functions in transitive dependencies.
    - `transitive_bloated_functions_loc`: Lines of code in the bloated functions of transitive dependencies.
    - `transitive_used_dependencies_count`: Number of used transitive dependencies.
    - `transitive_used_dependencies_loc`: Lines of code in used transitive dependencies.
    - `transitive_used_files_count`: Number of used files in transitive dependencies.
    - `transitive_used_files_loc`: Lines of code in the used files of transitive dependencies.
    - `transitive_used_functions_count`: Number of used functions in transitive dependencies.
    - `transitive_used_functions_loc`: Lines of code in the used functions of transitive dependencies.
  

- `rq2a.csv`: Contains the quantitative results for the second research question (RQ2), including all Python projects having vulnerable dependencies. Each row specifies a dependency from a project to a vulnerable dependency.
  - Columns:
    - `project`: GitHub Owner-Repository Name, representing the Python project.
    - `package_name`: Specifies the name of the PyPI package identified as a vulnerable dependency.
    - `dependency_type`: Distinguishes whether the vulnerable package is a direct or transitive dependency of the project.
    - `activation_status`: Indicates the invocation status of the dependency, specifying whether it is a bloated dependency, active, inactive, or undefined.

- `rq2b.csv`: Contains metrics regarding the usage of inactive (used while the vulnerable method is bloated) and active vulnerable packages within each Python project (RQ2). Each row describes a project’s interaction with a vulnerable dependency and more precisely the extent of bloat and usage in both the files and methods of this dependency.
  - Columns:
    - `project`: GitHub Owner-Repository Name, signifying the particular Python project being analyzed.
    - `package_name`: Specifies the name of the PyPI package identified as a vulnerable dependency.
    - `activation_status`: Indicates the invocation status of the dependency, specifying whether it is active or inactive.
    - `bloated_files`: Quantifies the number of bloated files present in the vulnerable dependency.
    - `used_files`: Enumerates the number of files from the vulnerable dependency that are actually utilized in the project.
    - `bloated_methods`: Enumerates the number of bloated methods present in the vulnerable dependency.
    - `used_methods`: Measures the number of methods from the vulnerable dependency that are actually utilized in the project.
    - `percentage_bloated_methods`: Calculates the percentage of bloated methods within the methods of the vulnerable dependency.
    - `percentage_bloated_files`: Computes the percentage of bloated files within the files of the vulnerable dependency.

- `qualitative_results.json`: This file contains the results of qualitative analysis conducted for research questions 3 and 4 (RQ3-RQ4) for the 50 selected bloated dependencies. Each record in the file represents a specific project with one or more dependencies that were analyzed. The key of each record is the project name, and its value is a set of JSON objects, where each object represents a dependency in the project. Each dependency object contains the following metadata:
  - `Root Cause`: Describes the root cause of the bloated dependency, as devised from our Root Cause Analysis (RQ3)
  - `PR Status`: Indicates the status of the associated pull request (PR), whether it's merged, open or closed. (Applicable only for dependencies for which we opened PRs)
  - `PR URL`: Provides the URL of the pull request related to the dependency.
  - `Duration`: Represents the duration of the pull request in days.
  - `Created At`: Specifies the date and time when the pull request related to the dependency was opened.
  - `Merged At`: (Optional) Specifies the date and time when the pull request related to the dependency was merged.
  - `Version`: Represents the version of the dependency being removed.
  - `LoC`: Stands for Lines of Code, indicating the number of lines of code of the dependency.
  - `Size`: Specifies the size of the dependency in bytes
  - `Discussion Status`: Indicates the status of any discussions or conversations related to the dependency.

Below is an example of a project entity in the JSON structure:

```json
  "ewels/MultiQC": {
      "simplejson": {
          "Root Cause": "Built-in or alternate library",
          "PR Status": "Merged",
          "PR URL": "https://github.com/ewels/MultiQC/pull/1973",
          "Duration": 4,
          "Created At": "2023-08-11T00:27:57Z",
          "Merged At": "2023-08-15T21:15:16Z",
          "Version": "3.19.1",
          "LoC": 4500,
          "Size": 515330,
          "Discussion Status": "No Discussion"
      }
  }
```
- `project_dependencies_post_data_collection.json`: This JSON file describes the status of our dataset after the Data Collection phase. Each key represents a GitHub project, and the values represent a list with the PyPI releases of the resolved dependencies. (Its descriptive statistics are described on the third line of Table 1).
```json
[
    {
      "rdiff-backup/rdiff-backup": [
        "PyYAML:6.0"
      ]
    },
    {
      "jopohl/urh": [
        "psutil:5.9.5",
        "numpy:1.25.0",
        "PyQt5-sip:12.12.1",
        "PyQt5:5.15.9",
        "Cython:0.29.36",
        "PyQt5-Qt5:5.15.2"
      ]
    }
  // More projects...
]
```
- `project_dependencies_final.json`: This JSON file describes the status of our dataset after the Data Analysis phase. It is a subset of the `project_dependencies_post_data_collection.json` file and its descriptive statistics are described on the third line of Table 1 of the paper.
- `security/`: This directory stores the data generated when running our methodology for answering RQ2 (detailed in the second paragraph of Section 2.4 of our paper)
  - `pypi_vulnerabilities.csv`:  This file contains the set of PyPI vulnerabilities extracted from the GitHub Advisory Database.
  - Columns:
    - `Identifier`: GitHub Owner-Repository Name, signifying the particular Python project being analyzed.
    - `Package`: Specifies the name of the affected PyPI package
    - `VersionConstraint`: Describes the package versions affected by this vulnerability, in the format of comma-separated version constraints (e.g. ">= 4.0,< 4.0.7")
  - `vulnerable_dependencies.json`: This JSON file serves as a record of vulnerable releases acting as dependencies in our dataset. Each record consists of a key representing a PyPI release and a list of affected Common Vulnerabilities and Exposures (CVEs). For example:
    ```json
        {
        "grpcio:1.50.0": [
            "GHSA-6628-q6j9-w8vg",
            "GHSA-cfgp-2977-2fmm",
            "GHSA-9hxf-ppjv-w6rq"
        ],
        // Other records...
      }
    ```
  - `project_vulnerabilities.json`:  This JSON file serves as a mapping of software projects to their vulnerable dependencies. Each key represents a unique project, identified by its name. Each project key represents a unique project identified by its name. Associated with each project key is a list of objects, where each object corresponds to a vulnerable dependency identified by its package name and version. The values are arrays listing the CVEs that impact that specific version of the dependency. An example JSON record is the following:
    ```json
    {
      "widdowquinn/pyani": [
        {
          "Pillow:10.0.0": [
            "GHSA-3f63-hfp8-52jq",
            "GHSA-j7hp-h8jx-5ppr"
          ]
        },
        {
          "fonttools:4.40.0": [
            "GHSA-6673-4983-2vx5"
          ]
        }
      ],
    // More projects...
    }
    ```
  - `vulnerability2function.json`: This JSON file contains a manual mapping of each vulnerability encountered in the dataset with the corresponding vulnerable functions. The keys represent the CVE identifiers, and the values are arrays containing the paths to the vulnerable functions within the codebase. For example:
    ```json
      {
          "GHSA-jh3w-4vvf-mjgr": [
              "//Django/django.core.validators/EmailValidator.__init__()",
              "//Django/django.core.validators/EmailValidator",
              "//Django/django.core.validators/URLValidator.__init__()",
              "//Django/django.core.validators/URLValidator"
          ],
          // Other mappings...
      }
    ```
- `subset/`: This directory stores the data generated when running our methodology for a subset of our dataset
  - `sample_projects.csv`: A simple CSV file listing the project names included in the subset of our dataset
  

# Getting Started

Before getting started, ensure that your machine meets the specifications outlined in the [Requirements](REQUIREMENTS.md) file.
Additionally, please refer to the [Installation Guide](INSTALL.md) for detailed instructions on setting up the necessary environment to run our experiments.


# Full Call Graph Dataset Retrieval (Optional)

**NOTE:** Ensure that you have at least 15GB of available disk space before running this step.

If you want to obtain the partial and stitched call graphs of the 1302 Python Applications along with their dependencies, as well as the bloat metrics corresponding to each project,
you can fetch the data from Zenodo. First run:

`wget -O callgraph_data.zip "https://zenodo.org/records/11088204/files/callgraph_data.zip?download=1"`

To extract the data, run:

`unzip callgraph_data.zip -d data/`

The above command will create inside the `data/` directory the `partial_callgraphs` and `stitched_callgraphs` directory. The directories will have the following structure:
```
├── partial_callgraphs
│   ├── apps
│   │   ├── aio-libs
│   │   │   ├── aiomonitor
│   │   │   │   └── cg.json
│   │   │   └── janus
│   │   │       └── cg.json
│   │   ├── cherrypy
│   │   │   └── cheroot
│   │   │       └── cg.json
│   │   ├── ...
│   ├── a
│   │   ├── aioconsole
│   │   │   └── 0.7.0
│   │   │       └── cg.json
│   │   │   └── 0.7.1
│   │   │       └── cg.json
│   │   ├── aiohttp
│   │   │   └── 3.9.5
│   │   │       └── cg.json
│   ├── r
│   │   ├── razorpay
│   │   │   └── 1.4.2
│   │   │       └── cg.json
│   │   ├── ...
├── stitched_callgraphs
    ├── 4catalyzer
    │   └── flask-resty
    │       ├── bloat_metrics.json
    │       └── cg.json
    ├── aamalev
    |   └── aiohttp_apiset
    │       ├── bloat_metrics.json
    │       └── cg.json
    │       ├── security_metrics.json
    └── ...
```
Specifically, the first directory, namely `partial call graphs`, stores in JSON representation the partial call graph of each Github project, as well as the partial call graph of each PyPI release which acts as a dependency in a project.
The project partial call graphs are stored in the following path:
`partial_callgraphs/apps/{project_owner}/{project_repo}/cg.json`.

Similarly, the partial call graph for each unique PyPI dependency (package_name:version) is stored in the following path:
 `partial_callgraphs/{first_letter_of_package_name}/{package_name}/{package_version}/cg.json`

An example Partial Call Graph JSON representation is the following:
```json
{
    "product":"yarl",
    "forge":"PyPI",
    "generator":"PyCG",
    "depset":[
       
    ],
    "version":"1.9.4",
    "timestamp":"0",
    "modules":{
       "internal":{
          "/yarl._url/":{
             "sourceFile":"yarl/_url.py",
             "namespaces":{
                "0":{
                   "namespace":"/yarl._url/",
                   "metadata":{
                      "first":1,
                      "last":1200
                   }
                },
                "1":{
                   "namespace":"/yarl._url/rewrite_module()",
                   "metadata":{
                      "first":19,
                      "last":21
                   }
                },
                //More internal methods
            }
          }
       },
       "external":{
          "urllib":{
             "sourceFile":"",
             "namespaces":{
                "125":{
                   "namespace":"//urllib//urllib.parse.urlsplit",
                   "metadata":{
                      
                   }
                },
                "126":{
                   "namespace":"//urllib//urllib.parse.SplitResult",
                   "metadata":{
                      
                   }
                }
             }
            }
          }
       }
    },
    "graph":{
       "internalCalls":[
          [
             "0",
             "1",
             {
                
             }
          ],
          [
             "7",
             "2",
             {
                
             }
          ],
        // More edges
       ],
    },
    "nodes":179,
    "metadata":{
       "loc":1181,
       "time_elapsed":-1,
       "max_rss":-1,
       "num_files":4
    },
    "sourcePath":"data/sources/y/yarl/1.9.4"
 }
```
The second directory, namely `stitched_callgraphs`, is structured into directories for each of the analyzed projects.
Each sub-directory is named using the pattern `repo_name/project_name/` and contains (at most) three JSON files, specifically:

- **`cg.json`**: Contains the stitched call graph for the project, integrating the partial call graphs of the project with the ones of its direct and transitive dependencies.

- **`bloat_metrics.json`**: Contains individual project-specific bloat metrics from the reachability analysis, measuring various aspects of code bloat such as the number of bloated dependencies, files, and methods, along with their corresponding lines of code. The data from this file are aggregated and used to generate `rq1a.csv` and `rq1b.csv` (see [Dataset Description](#dataset-description) for detailed description). These CSV files subsequently provide the numerical data for figures and tables in the results of RQ1 (see [RQ1: Bloat Prevalence (Section 3.1)](#rq1-bloat-prevalence-section-31)).


- **`security_metrics.json`**: Available only for projects with reachable vulnerable dependencies. It includes metrics on dependency bloat concerning vulnerable code. By aggregating the data included in those files, we craft the `data/results/rq2a.cv` and `data/results/rq2b.cv` (see [Dataset Description](#dataset-description) for detailed description) which are used to answer RQ2 and produce the corresponding figures (see [RQ2: Security Impact (Section 3.2)](#rq2--security-impact--section-32-))
  
An example stitched call graph JSON representation is the following:

```json
{
  "nodes": {
    "0": {
      "URI": "//click/click.exceptions/ClickException.format_message()",
      "metadata": {
        "LoC": 2
      }
    },
    "1": {
      "URI": "/click/click.parser/Option.__init__()",
      "metadata": {
        "LoC": 32
      }
    },
    "2": {
      "URI": "//SQLAlchemy/sqlalchemy.sql.schema/MetaData.reflect()",
      "metadata": {
        "LoC": 177
      }
    },
    // More nodes...
  },
  "edges": [
    [
      0,
      1
    ],
    [
      1,
      2
    ],
  // More edges...
  ]
}
```

# Step-by-Step Instructions

In the following sections, we provide instructions
for reproducing the descriptive tables and figures
presented in the paper using the "pre-baked" data coming from the `data/` directory.
Then we provide detailed instructions to re-run our methodology for producing those results

## Descriptive Tables (Sections 2.2 & 2.3)

To produce the descriptive statistics regarding our dataset after the Data Collection as well as after the Data Analysis steps (as described on Table 1), simply run:

```bash
python scripts/descriptives/dataset_analysis.py  \
  -json_pre data/project_dependencies_post_data_collection.json \
  -json_post data/project_dependencies_final.json 
```
The following script will print the following table (Part of Table 1):
```
Step            | Operation                     | Total GitHub Projects | Resolved Dependencies | PyPI Releases | Average Dependencies (Per Project)
------------------------------------------------------------------------------------------------------------------------------------------------------
Data Collection | Dependency Resolution         | 1644                  | 34864                 | 5617          | 21.21                             
Data Analysis   | Partial Call Graph Generation | 1302                  | 21785                 | 3232          | 16.73   
```
**Note**: Due to a minor transcription error in the descriptive statistics previously reported in the major revision version of our paper, there are very small discrepancies in some numbers.
The numbers shown above are correct, and we will incorporate these slight adjustments in the camera-ready version of the paper.


Moreover, to produce Table 2 describing the statistics on the resolved and unresolved external calls during our stitching process, simply run:

```bash
python scripts/descriptives/evaluation.py  -csv data/results/rq1a.csv 
```
This script will produce the following table:

```
External Calls  Aggregate count Proportion of total (%)   Average (per project) Median (per project)
Resolved        7799929         96.8                      5990.7               144.5               
Unresolved      260249          3.2                       199.9                11.5      
```


## Results

### RQ1: Bloat Prevalence (Section 3.1)

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
python scripts/rq1_dep_comp.py data/results/rq1b.csv \
  --output figures/bloat_prevalence_direct_vs_transitive.pdf
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

### RQ2: Security Impact (Section 3.2)

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
python scripts/rq2_bloat_metrics.py data/results/rq2b.csv \
--output figures/bloat_metric_per_exposure.pdf 
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

### RQ3: Root Causes (Section 3.3)

In this research question, we manually classify
the root causes of 50 bloated dependencies
and report our results,
as depicted in Figure 9.

To produce Figure 9, simply run:

```bash
python scripts/rq3.py data/results/qualitative_results.json \
 --output figures/root_cause_distribution.pdf
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

### RQ4: Developer Perception (Section 3.4)

In the last research question, we investigate developer's perception of dependency bloat.
To reproduce Table 3, simply run:

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
is reported in Section 3.4.

Moreover, to reproduce Figure 10, run:


```bash
python scripts/rq4.py data/results/qualitative_results.json \
 --output_fig_10 figures/pr_per_root_cause.pdf
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
python scripts/rq4.py data/results/qualitative_results.json \
--output_fig_11 figures/pr_durations.pdf
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
python scripts/rq4.py data/results/qualitative_results.json \
 --output_fig_12 figures/pr_discussions.pdf
```

The above command produces the figure `figures/pr_discussions.pdf` (Figure 12)
and prints the following data in the standard output:

```
Merged PRs requiring no discussion: 21
Merged PRs requiring discussions involving changes: 6
Merged PRs requiring discussions without requiring changes: 3
```

## Methodology
 Before proceeding with the methodology, it's important to note that for each step of our process
 (dependency resolution, partial call graph generation, and stitching), we offer two options:
 The first option involves running the steps on the full dataset, which replicates the exact operations performed in the paper.
 However, this comprehensive process may take up to 5 weeks to complete.
 For convenience, we provide the option to perform the methodology steps for a subset of 50 projects, which should take less than 30 minutes to finish.


**NOTE #1** Ensure that you have at least 150GB of available disk space if you decide to run the methodology steps of the full dataset.

**NOTE #2:**: Some numbers generated from the methodology section may differ slightly from those reported in the paper or our datasets. This variance is due to changes in source code or dependency relations of certain projects or dependencies since our analysis was conducted.


###  Project Selection and Dependency Resolution (Section 2.2)
This section outlines the process of resolving project dependencies as detailed in Section 2.2 of our accompanying paper.

#### Dependency Resolution of Full Dataset (Optional)
To perform the dependency resolution process of the full dataset, simply execute (estimated running time: 2-3 days):
```bash
sh scripts/dependency_resolution/run_dep_resolution.sh $GH_TOKEN data
```
This script performs the following steps:

- Downloads the initial [dataset](https://zenodo.org/records/5645517) from Zenodo that includes the set of Python projects used in our study.
- Clones each project repository into the specified target directory (in directory `sources/apps` inside the specified `data/` directory).
- Resolves dependencies for each project using pip and saves the results in a resolved_dependencies.json file within each project's directory.
- Aggregates all the individual `resolved_dependencies.json` files from each project into a single file named `project_dependencies_post_data_collection.json`. The structure of this file is detailed in Section [Dataset Description](#dataset-description).



#### Dependency Resolution of a Subset Dataset

For a quicker resolution process, we give the option to resolve dependencies for a subset of the dataset.
This process handles only 50 projects and is significantly faster. To execute this, run:
```bash
sh scripts/dependency_resolution/run_dep_resolution.sh $GH_TOKEN data/subset subset
```
This execution will download the source code of 50 projects (listed in the `data/subset/sample_projects.txt` file)
and generate a `project_dependencies_subset.json` file in the `data/subset` directory containing the resolved dependencies for the subset of projects.

### Partial Call Graph Construction (Section 2.3.1)

In this step, we use PyCG to build the partial call graph of each project,
as well as for each of its dependencies.

#### Partial Call Graph Generation of Full Dataset (Optional)
Optionally, you can reproduce the partial call graph generation process of the full dataset.
**Important Note:** This process is expected to take **3-4 weeks** to complete.
Before beginning this process, ensure that you have access to the `data/project_dependencies_post_data_collection.json` file, which contains the resolved dependencies after the Data Collection. This file is included in the repository but can also be generated using the process described in the [dependency resolution process of the full dataset](#dependency-resolution-of-full-dataset-optional) section.
Additionally, the source code for each project must be available locally. This can be accomplished by running the previous dependency resolution steps (see Section [Dependency Resolution of Full Dataset (Optional)](#dependency-resolution-of-full-dataset-optional)).
To initiate the partial call graph generation, execute the following command:
```bash
sh scripts/partial_cg_generation/run_partial_cg_generation.sh $GH_TOKEN \
 data data/project_dependencies_post_data_collection.json data/project_dependencies_final.json 
```
This script will install PyCG and use it to produce the partial call graphs of the source code of each project.
It will also retrieve the dependency set of all projects and build the partial call graph of each dependency.
The partial call graph for each project is stored in JSON format at the destination:
`data/partial_callgraphs/apps/{project_owner}/{project_repo}/cg.json`.

Similarly, the call graph for each unique PyPI dependency (package_name:version) is stored in the file:
 `data/partial_callgraphs/{first_letter_of_package_name}/{package_name}/{package_version}/cg.json`

Moreover, the source code of each release will also be stored in the following directory:
  `data/sources/{first_letter_of_package_name}/{package_name}/{package_version}/`.

 Finally, the script will produce a JSON file named `data/project_dependencies_final.json` which contains the final dataset of projects and dependencies. This file is the final dataset used in the Data Analysis Phase.(Its descriptives are described in the Data Analysis rows of Table 1). The structure of this file is detailed in Section [Dataset Description](#dataset-description).


#### Partial Call Graph Generation of Subset Dataset
For a quicker alternative, you can run the partial call graph construction process for a subset of 50 projects along with their set of dependencies, comprising of 88 unique PyPI releases.
Ensure you have completed the [dependency resolution process of the subset dataset](#dependency-resolution-of-a-subset-dataset) step before proceeding with this step.
To initiate this process, execute the following command  (estimated running time: ~10 minutes):
```bash
sh scripts/partial_cg_generation/run_partial_cg_generation.sh $GH_TOKEN \
data/subset data/subset/project_dependencies_subset.json \
data/subset/project_dependencies_final_subset.json 
```
This script performs the same operations as outlined in the full dataset section but on a smaller scale. It will:

* Produce the partial call graphs for each project and its dependencies.
* Store the produced partial call graphs, as well as the source code of each dependency within the `data/subset/` directory, maintaining the same directory structure with the one described on the previous sub-section.
* Finally, it will generate a file named `data/subset/project_dependencies_final_subset.json`, containing the final dataset of projects and dependencies after performing this step.

### Stitching of Call Graphs & Reachability Analysis (Sections 2.3.2 & 2.3.3)
In our implementation, for efficiency, we perform the stitching and the reachability analysis in one step.

#### Stitching & Reachability Analysis of Full Dataset (Optional)

Before beginning this process, ensure that you have access to the `data/project_dependencies_final.json` file, which contains the resolved dependencies after the Partial Call Graph Generation phase.
This file is already included in the repository but can also be generated using the process described in the [Partial Call Graph Generation of Full Dataset (Optional)](#partial-call-graph-generation-of-full-dataset-optional) section.
Moreover, in order to replicate the stitching as well as the reachability analysis of the whole dataset used in our study,
you need to have produced the partial call graphs of each project and each dependency, either through performing the steps described on  [Partial Call Graph Generation of Full Dataset (Optional)](#partial-call-graph-generation-of-full-dataset-optional) section or through using the "pre-baked" stitched callgraph dataset obtained through Zenodo (see Section [Full Call Graph Dataset Retrieval (Optional)](#full-call-graph-dataset-retrieval-optional)).

**Important Note:** This process is expected to take **1-2 weeks** to complete.

To initiate the stitched call graph generation (and reachability analysis), execute the following command:

```bash
python scripts/stitched_cg_generation/stitch.py \
  --source data/full/partial_callgraphs --json data/project_dependencies_final.json
```

This script collects for each project the partial call graph of its source code as well as its dependencies and incrementally merges them to form the stitched graph.
Moreover, it performs a reachability analysis (Section 2.3.3) on the stitched graph to compute the bloat metrics necessary to answer the first research question (described in the first paragraph of Section 2.4 of our paper)
For each project, it produces two JSON files. Specifically:

- `data/stitched_callgraphs/{project_owner}/{project_repo}/cg.json`: Contains the stitched call graph of the project, integrating multiple call graphs from direct and transitive dependencies to form a comprehensive view of the project’s call architecture.

- `data/stitched_callgraphs/{project_owner}/{project_repo}/bloat_metrics.json`: Contains individual project-specific results from the reachability analysis, measuring various aspects of code bloat such as the number of bloated dependencies, files, and methods, along with their corresponding lines of code. Each record from these JSON files is used to produce [rq1a.csv](#rq1acsv), and [rq1b.csv](#rq1bcsv) which are used in the result section to produce the tables and figures of RQ1.

#### Stitching & Reachability Analysis of Subset Dataset

Again, for convenience, we give the option to perform the stitching as well as the reachability analysis for the 50 sample projects used in the dependency resolution and partial call graph generation.
The only requirement to run this analysis is to have performed the steps outlined in sections [dependency resolution process of the subset dataset](#dependency-resolution-of-a-subset-dataset) and [Partial Call Graph Generation of Subset Dataset](#partial-call-graph-generation-of-subset-dataset). Having performed those steps, simply run:


```bash
python scripts/stitched_cg_generation/stitch.py --source data/subset/partial_callgraphs \
  --json data/subset/project_dependencies_final_subset.json
```

This script performs the same operations as outlined in the full dataset section but on a smaller scale, and it will store the results in the directory `data/subset/`, maintaining the same directory structure.


### Analyzing Reachability Results: RQ2:Relation between software bloat and software vulnerabilities (2nd paragraph of Section 2.4):

**NOTE:** Ensure that you have at least 3GB of available disk space before running this step.

In this sub-section, we describe how you can run our methodology from scratch for producing the security metrics used to answer RQ2. The steps are described in the second paragraph of Section 2.4.
We split this process in 2 steps. The first includes using the GitHub advisory database to retrieve PyPI vulnerabilities and investigate whether they affect our dataset. This step does not have any prerequisites.
To perform this operation, simply run:
```bash
 sh scripts/security_analysis/run_security_analysis.sh  $GH_TOKEN  \
  data/security data/project_dependencies_final.json
``` 
The script performs the following steps:
* It will first download the repository of the advisory database which contains the known PyPI vulnerabilities (this might take up to 30 minutes depending on your network connection)
* It will parse the repository to identify vulnerabilities affecting PyPI releases
* It will then find all the vulnerable releases affecting our dataset, and it will produce a file `data/security/project_vulnerabilities.json` which has the following format:

```json
{
  "widdowquinn/pyani": [
    {
      "Pillow:10.0.0": [
        "GHSA-3f63-hfp8-52jq",
        "GHSA-j7hp-h8jx-5ppr"
      ]
    },
    {
      "fonttools:4.40.0": [
        "GHSA-6673-4983-2vx5"
      ]
    }
  ],
  "pelican-plugins/image-process": [
    {
      "Pillow:10.0.0": [
        "GHSA-3f63-hfp8-52jq",
        "GHSA-j7hp-h8jx-5ppr"
      ]
    },
    {
      "jinja2:3.1.2": [
        "GHSA-h5c8-rqwp-cp95"
      ]
    }
  ],
// More projects...
}
```
The JSON file depicted above serves as a mapping of software projects to their vulnerable dependencies. Each key represents a unique project, identified by its name. Associated with each project key is a list of objects, where each object corresponds to a particular dependency identified by its package name and version (e.g., Pillow:10.0.0). The values are arrays listing the Common Vulnerabilities and Exposures (CVEs) IDs that impact that specific version of the dependency. This structure enables quick identification of vulnerabilities associated with dependencies in our project dataset.

Then, you can also run the reachability analysis on the stitched call graphs to produce the security metrics used to answer RQ2. To do this you need the already existing file `data/security/vulnerability2function.json` which contains the manually created mapping of each vulnerability encountered in our dataset with the actual vulnerable function (See second paragraph of Section 2.4 of our paper). Moreover, you need to have produced the stitched call graphs of each project to perform this step.  You can do this either by using the "pre-baked" stitched call graph dataset existing on Zenodo (for details see [Full Call Graph Dataset Retrieval (Optional)](#full-call-graph-dataset-retrieval-optional)) or by performing the steps described in the [Stitching & Reachability Analysis of Full Dataset (Optional)](#stitching--reachability-analysis-of-full-dataset-optional) section. You can run the security reachability analysis by running:


```bash
python scripts/stitched_cg_generation/security_reachability_analysis.py \
  --host data/stitched_callgraphs \
  --project_vulns  data/security/project_vulnerabilities.json \
  --vuln2func data/security/vulnerability2function.json
```
```
$: python scripts/stitched_cg_generation/security_reachability_analysis.py -h
usage: security_reachability_analysis.py [-h] -host HOST -project_vulns PROJECT_VULNS -vuln2func VULN2FUNC

Extract security bloat metrics for RQ2 through the reachability analysis

options:
  -h, --help            show this help message and exit
  -host HOST, --host HOST
                        Path to the directory hosting the stitched call graphs
  -project_vulns PROJECT_VULNS, --project_vulns PROJECT_VULNS
                        Json file hosting project vulnerabilities
  -vuln2func VULN2FUNC, --vuln2func VULN2FUNC
                        Json file hosting the manual mapping of vulnerabilities to vulnerable functions
```

For each project of our dataset having at least one vulnerable dependency, the script will produce in the same directory where the stitched call graph exists (e.g. `data/stitched_callgraphs`) a file named:
`security_metrics.json` (see [Full Call Graph Dataset Retrieval (Optional)](#full-call-graph-dataset-retrieval-optional) for file description)
