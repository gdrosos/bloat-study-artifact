import json
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Merge JSON files into a single JSON list.')
    parser.add_argument('-d', '--directory', required=True, help='Directory to search for JSON files')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file name')
    return parser.parse_args()

def merge_json_files(directory, output_file):
    all_data = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a JSON file
            if file == 'resolved_dependencies.json':
                full_path = os.path.join(root, file)
                with open(full_path, 'r') as f:
                    data = json.load(f)
                    all_data.append(data)

    # Write all data to a single JSON file
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=2)

def main():
    args = parse_args()
    merge_json_files(args.directory, args.output)

if __name__ == "__main__":
    main()