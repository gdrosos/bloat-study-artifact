import csv
import os
import subprocess
from multiprocessing import Pool
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Clone a list of GitHub repositories.')
    parser.add_argument('-t', '--token', required=True, help='GitHub access token')
    parser.add_argument('-f', '--file', required=True, help='CSV file with list of repositories')
    parser.add_argument('-d', '--directory', required=True, help='Directory to store cloned repositories')
    return parser.parse_args()

def clone_repo(args, repo):
    print("Cloning:", repo)
    user, repo_name = repo.split('/')
    directory = os.path.join(args.directory, user, repo_name)

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Clone the repo with token authentication
    result = subprocess.run(
        f'git clone https://{args.token}@github.com/{repo}.git {directory}',
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Failed to clone {repo}: {result.stderr}"
    return None

def main():
    args = parse_args()

    # Read CSV and clone repos
    with open(args.file, 'r') as file:
        repos = [row[0] for row in csv.reader(file)]

    # Create a pool of workers
    with Pool() as pool:
        results = pool.starmap(clone_repo, [(args, repo) for repo in repos])
    failed_repos = [result for result in results if result is not None]
    print(f"Number of failed repository clones: {len(failed_repos)}")
    for failure in failed_repos:
        print(failure)

if __name__ == "__main__":
    main()
