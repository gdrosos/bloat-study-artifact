# Installation Guide
This file  includes instructions and documentation for setting up the necessary environment in order run our code.
Note that the following instructions may not work on any machine, as they have only been tested on Ubuntu and Debian, however we recommend using Docker (see [Requirements](REQUIREMENTS.md#)).
If you encounter any issues, please contact us.

## Getting Started

Before we begin, make sure that your machine  meets the specifications listed in the  [Requirements file](REQUIREMENTS.md).

First, obtain the artifact by cloning the repository and navigating to the artifact's root directory:

```bash
   git clone https://github.com/gdrosos/bloat-study-artifact ~/bloat-study-artifact
   cd ~/bloat-study-artifact
```
To replicate the environment needed to run our analyses and scripts, you can choose between setting up a virtual environment directly on Ubuntu/Debian or using Docker, which is recommended.
## Option1: Ubuntu/Debian Installation

You need to install some packages through  `apt`  to run the
experiments of this artifact.
First, install git, python, pip, wget, unzip and python3-venv:

```bash
sudo apt update
sudo apt install git python3 python3-pip  wget unzip python3-venv
```
**Important Note**
For convenience, throughout the documentation and scripts, we use the standard python command instead of python3. To ensure compatibility, please create a symbolic link to point python to python3 by running the following command:
```bash
ln -s /usr/bin/python3 /usr/bin/python
```

You also need to install some Python packages.
In a Python `virtualenv` run the following:
```bash
python -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
```

### Option2: Docker Image Installation (Recommended)

Use this option if you prefer a containerized environment or are not using an Ubuntu/Debian operating system.
We provide a `Dockerfile` to build an image that contains:

* The necessary `apt` packages (e.g., `git`, `python3`, `pip`, `sudo`) for running the
  our experiments.
* The necessary Python packages (declared in the `requirements.txt` file).
* A user named `user` with `sudo` privileges.

To build the Docker image named `bloat-study-artifact` from source,
run the following command (estimated running time: ~7 minutes):

```bash
docker build -t bloat-study-artifact .
```
Then, you can run  the docker container by executing the following command:

```bash
docker run -it --rm \
    -v $(pwd)/scripts:/home/user/scripts \
    -v $(pwd)/data:/home/user/data \
    -v $(pwd)/figures:/home/user/figures \
    bloat-study-artifact /bin/bash
```
After executing the command, you will be able to enter the home directory
(i.e., `/home/user`). This directory contains:
1) the scripts for reproducing the results of the paper (see `scripts/`),
2)  the data of our bloat study (see `data/`),
3) a dedicated directory for storing the generated figures (see `figures/`),


This setup uses volume mounting (-v) to ensure that scripts, data, and figures directories are persisted outside of the container for ease of access and modification on your local machine (e.g. they will not be lost upon the container's exit).

# Important Note
In order to run some parts of our methodology, you will need a Github access token (see [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)).
Once you obtain it,
please assign it to a shell variable named `GH_TOKEN`.

```bash
export GH_TOKEN=<your Github access token>
```

