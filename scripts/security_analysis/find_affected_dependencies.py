import csv
from packaging.requirements import Requirement
from packaging.version import parse
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Get reported vulnerabilities on PyPI releases')
    parser.add_argument('-json', '--json', required=True, help='Path to JSON file hosting the dependencies')
    parser.add_argument('-cves', '--cves', required=True, help='CSV file with collected vulnerabilities')
    parser.add_argument('-o', '--out', required=True, help='Output csv file with affected dependencies')

    return parser.parse_args()

def match_vulnerabilities_to_dependencies(vulnerabilities, dependencies):
    unique_vulnerabilities_set = set()
    for vulnerability in vulnerabilities:
        if vulnerability.package in dependencies:
            requirement = Requirement(vulnerability.package + " " + vulnerability.version_constraint)
            specifier_set = requirement.specifier
            for version in dependencies[vulnerability.package]:
                if specifier_set.contains(parse(version)):
                    dependencies[vulnerability.package][version]["count"]+=1
                    dependencies[vulnerability.package][version]["vulnerability_ids"].append(vulnerability.id)
                    unique_vulnerabilities_set.add(vulnerability.id)
        # elif vulnerability.package.lower() in dependencies:
        #     requirement = Requirement(vulnerability.package.lower()+ " "+vulnerability.version_constraint)
        #     specifier_set = requirement.specifier
        #     for version in dependencies[vulnerability.package.lower()]:
        #         if specifier_set.contains(parse(version)):
        #             dependencies[vulnerability.package.lower()][version]+=1
        #             count+=1
    # print("Number of unique vulnerabilities affecting our dataset:", len(unique_vulnerabilities_set))

    return dependencies

class VulnerabilityConstraint:
    def __init__(self, id, package, version_constraint):
        self.id = id    = id
        self.package = package
        self.version_constraint = version_constraint

    def __repr__(self):
        return f'{self.id} {self.package} {self.version_constraint}'

def load_vulnerabilities(path):
    vulnerabilities = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            id, package, version_constraint = row
            vulnerabilities.append(VulnerabilityConstraint(id, package, version_constraint))
    return vulnerabilities

def load_dependencies(path):
    file = open(path, 'r')
    data = json.load(file)
    dependency_to_vulnerabilities = {}
    for project in data:
        for dep in list(project.values())[0]:
            package, version = dep.split(':')
            if package not in dependency_to_vulnerabilities:
                dependency_to_vulnerabilities[package] = {}
            dependency_to_vulnerabilities[package][version] = {"count": 0, "vulnerability_ids": []}
    return dependency_to_vulnerabilities



def main():
    args = parse_args()
    vulnerabilities = load_vulnerabilities(args.cves)
    dependencies = load_dependencies(args.json)
    final_dataset = match_vulnerabilities_to_dependencies(vulnerabilities, dependencies)
    package_version_count_with_vulnerabilities = 0
    total = 0

    output_data = {}

    for package, versions in final_dataset.items():
        for version, data in versions.items():
            if data["count"] > 0:

                total+=data['count']
                package_version_count_with_vulnerabilities += 1

                key = f"{package}:{version}"
                output_data[key] = data["vulnerability_ids"]

    # print(f"Number of package versions with at least one vulnerability: {package_version_count_with_vulnerabilities}")
    # print(f"Total number of vulnerabilities: {total}")

    with open(args.out, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)


if __name__ == "__main__":
    main()
