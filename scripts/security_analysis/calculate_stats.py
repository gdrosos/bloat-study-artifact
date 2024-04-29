import json
import csv
import pprint
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Find vulberabilties affecting projects')
    parser.add_argument('-json', '--json', required=True, help='Path to JSON file hosting the dependencies')
    parser.add_argument('-cves', '--cves', required=True, help='Json fil hostign the vulnerable dependencies')
    parser.add_argument('-o', '--out', required=True, help='Output csv file with projects with vulnerable dependencies')

    return parser.parse_args()
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def main():
    args = parse_args()
    dataset = load_json(args.json)
    dep2vuln = load_json(args.cves)

    projects2vulnerabilities_cnt = {}
    vulnerable_projects = set()
    projects2vulnerabilities = {}
    for item in dataset:
        values= list(item.values())
        keys = list(item.keys())

        for dependency in values[0]:
            if dependency in dep2vuln:
                    if keys[0] not in projects2vulnerabilities_cnt:
                        projects2vulnerabilities_cnt[keys[0]] = 0   
                        projects2vulnerabilities[keys[0]] = []

                    vulnerable_projects.add(keys[0])
                    projects2vulnerabilities_cnt[keys[0]]+= len(dep2vuln[dependency])
                    projects2vulnerabilities[keys[0]].append({dependency: dep2vuln[dependency]})

    # print("Number of total projects: ", len(dataset))
    # print("Number of vulnerable projects: ", len(vulnerable_projects))

    # save projects2vulnerabilities dictionary
    with open(args.out, 'w') as fp:
        json.dump(projects2vulnerabilities, fp, indent=2)


if __name__ == "__main__":
    main()
