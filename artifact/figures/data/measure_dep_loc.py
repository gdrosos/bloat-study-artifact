import json
import subprocess
import os
import tempfile  # Import the tempfile module for creating temporary directories

# Load the dataset
with open("qualitative_results.json", "r") as f:
    dataset = json.load(f)

# Function to install a package using pip without dependencies into a specified directory
def install_package_no_deps(package_name, version, target_dir):
    subprocess.run(["pip3", "install", "--no-deps", "--target", target_dir, f"{package_name}=={version}"], check=True)

# Function to count lines of code in Python files for a given directory
def count_loc(directory):
    loc = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    loc += sum(1 for _ in f)
    return loc

# Function to measure the size of a directory in bytes
def measure_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

total_loc = 0
total_size = 0
count = 0
for repo, libraries in dataset.items():
    for library, details in libraries.items():
        deps = details["Transitive Dependencies"]
        if len(deps)>0:
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    for coordinate in deps:
                        library, version = coordinate.split(":")
                        install_package_no_deps(library, version, temp_dir)
                        # Now temp_dir contains the installed package
                        loc = count_loc(temp_dir)
                        size = measure_size(temp_dir)
                        details["LoC"] = loc
                        details["Size"] = size
                        if details["PR Status"] == "Merged" and details["Root Cause"] != "Transitive dependency":
                            count+=1
                            total_loc+=loc
                            total_size+=size
                except Exception as e:
                    print(f"Error processing {library}: {e}")

        else:
            details["Dependency Size"] = 0

        # Create a temporary directory for the package installation

# Write the updated dataset back to the file
with open("updated_qualitative_results1.json", "w") as f:
    json.dump(dataset, f, indent=4)

print(count, total_loc, total_size)