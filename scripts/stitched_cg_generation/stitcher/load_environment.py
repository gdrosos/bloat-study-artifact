import os
import sys
import subprocess
import importlib
import inspect
import argparse


# Function to create an isolated Python environment
def create_isolated_env(env_name, python_version='python3'):
    subprocess.run([python_version, '-m', 'venv', env_name])

def get_env_name(package_name, package_version):
    """
    Generates a unique environment name based on the package name and version.
    This ensures a separate environment for each package-version combination.
    """
    # Sanitize package name and version to be filesystem-friendly
    safe_package_name = package_name.replace(".", "_").replace("-", "_")
    safe_package_version = package_version.replace(".", "_").replace("-", "_")
    script_path = os.path.abspath(__file__)

    # Get the directory of the current script
    script_dir = os.path.dirname(script_path)
    return f"{script_dir}/virtual_environments/{safe_package_name}_{safe_package_version}_env"

# Function to install a specific package and its dependencies into the isolated environment
def install_package(env_name, package_name, package_version):
    pip_command = f"{env_name}/bin/pip3 install {package_name}=={package_version}"
    subprocess.run(pip_command, shell=True)

def dynamic_import(input_string, package_name, package_version):
    env_name = get_env_name(package_name, package_version)
    if not os.path.exists(env_name):
        create_isolated_env(env_name)
        install_package(env_name, package_name, package_version)
    python_exec = os.path.join(env_name, 'bin', 'python3') 
    
    # Construct the command to call dynamic_import.py
    script_path = os.path.abspath(__file__)

    # Get the directory of the current script
    script_dir = os.path.dirname(script_path)

    dynamic_import_script = script_dir+'/dynamic_import.py'
    command = [python_exec, dynamic_import_script, input_string]
    
    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)
    responses = result.stdout.split("\n")
    return responses

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamically import a module, install a package in an isolated environment, and resolve file path and import namespace.")
    parser.add_argument("input_string", help="The input string to be processed (format: module.object)")
    parser.add_argument("package_name", help="The name of the package to install")
    parser.add_argument("package_version", help="The version of the package to install")

    args = parser.parse_args()

    # Adjusted to use dynamic_import which ensures one-time setup
    print(dynamic_import(args.input_string, args.package_name, args.package_version))
