
# Requirements

To install and utilize the artifact, the following requirements must be met:
- **Docker**: 
  - We recommend using Docker to ensure a consistent and reproducible environment across all platforms. The provided `Dockerfile` will help you set up the necessary environment. This artifact has been tested with Docker version 24.

- **Operating System**:
  - If Docker is not an option, the artifact has been tested and confirmed to work on Unix-like operating systems, specifically Ubuntu and Debian.

- **Version Control**: 
  - Git must be installed.

- **Programming Language**: 
  - Python 3.8 or higher along with PIP.
- **Network Connection**: 
  - A stable internet connection is essential as some steps in the methodology require substantial downloading.

- **Memory**: 
  - At least 2 GB of free main memory.

- **Disk Space (Optional)**: 
  - A minimum of 150GB of disk space if you plan to rerun the experiments from scratch or download the full dataset from Zenodo.

- **Processing Power (Optional)**: 
  - While not a strict requirement, having at least 3-4 CPU cores is recommended for optimal performance, as some artifact operations are multi-core optimized.

- **GitHub Access Token**: 
  - A GitHub access token is needed for cloning certain public repositories as part of the methodology. Instructions for creating a token are available [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
