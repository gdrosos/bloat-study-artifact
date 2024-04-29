import os
import json
import csv
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Get reported vulnerabilities on PyPI releases')
    parser.add_argument('-gad_path', '--gad_path', required=True, help='Directory hosting github advisory db')
    parser.add_argument('-o', '--out', required=True, help='Output csv file with vulnerabilities of PyPI releases')

    return parser.parse_args()

def parse_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data     

def process_directory(directory_path, gad_path, output):
    total_vulnerabilities = 0
    package_set = set()
    with open(output, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Identifier', 'Package', 'VersionConstraint'])
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                found = False
                file_path = os.path.join(root, file_name)
                data = parse_json_file(file_path)
                # cve_aliases = [alias for alias in data['aliases'] if alias.startswith('CVE-')]
                affected_packages = data['affected']
                identifier = data["id"]
                if "withdrawn" in data:
                    continue
                for affected in affected_packages:
                    if affected['package']["ecosystem"] == "PyPI":
                        package_name = affected['package']['name']
                        package_set.add(package_name)
                        found=True
                        lower_limit = None
                        upper_limit = None
                        if 'ranges' in affected:
                            ranges = affected['ranges']
                            for range_info in ranges:
                                events = range_info['events']
                                introduced = None
                                fixed = None
                                last_affected = None
                                for event in events:
                                    if 'introduced' in event:
                                        introduced = event["introduced"]
                                    elif 'fixed' in event:
                                        fixed = event["fixed"]
                                    elif 'last_affected' in event:
                                        last_affected = event["last_affected"]
                                
                                lower_limit = ">= " + introduced
                                if fixed:
                                    upper_limit = "< "+ fixed
                                    # print(identifier, package_name, fixed)
                                elif last_affected:
                                    upper_limit = '<= ' + last_affected
                                else:
                                    if 'database_specific' in affected:
                                        upper_limit = affected["database_specific"]["last_known_affected_version_range"]
                                    else:
                                        upper_limit = None
                            
                            version_constraint = ",".join(filter(None, [lower_limit, upper_limit]))
                            writer.writerow([identifier, package_name, version_constraint])       
                        else:
                            versions = affected['versions']
                            for version in versions:
                                writer.writerow([identifier, package_name, f"== {version}"])
                if found:
                    total_vulnerabilities+=1
                
    # print("Total vulnerabilities:", total_vulnerabilities)
    # print("Total affected PyPI packages:", len(package_set))

def main():
    args = parse_args()
    directory_path = args.gad_path+'/advisory-database/advisories/github-reviewed'
    process_directory(directory_path, args.gad_path, args.out)


if __name__ == "__main__":
    main()
