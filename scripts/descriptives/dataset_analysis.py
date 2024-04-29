import json
import argparse
import os



def parse_args():
    parser = argparse.ArgumentParser(description='Get decriptive stats for dataset (included in Table 1)')
    parser.add_argument('-json_pre', '--json_pre', required=True, help='Path to JSON file hosting the dataset pre data analysis')
    parser.add_argument('-json_post', '--json_post', required=True, help='Path to JSON file hosting the dataset post ata analysis')


    return parser.parse_args()

def load_json(path):
    file = open(path, 'r')
    data = json.load(file)
    return data

def analyze_dependency_data(data):
    total_keys = len(data)
    total_values = 0
    unique_values = set()
    
    for entry in data:
        for key, values in entry.items():
            total_values += len(values)
            unique_values.update(values)
    
    unique_values_count = len(unique_values)
    average_values_per_key = total_values / total_keys if total_keys else 0

    return {
        "Total GitHub Projects": total_keys,
        "Resolved Dependencies": total_values,
        "PyPI Releases": unique_values_count,
        "Average Dependencies (Per Project)": f"{average_values_per_key:.2f}"
    }

def print_table(data_collection, data_analysis):
    headers = ["Step", "Operation", "Total GitHub Projects", "Resolved Dependencies", "PyPI Releases", "Average Dependencies (Per Project)"]
    steps = ["Data Collection", "Data Analysis"]
    operations = ["Dependency Resolution", "Partial Call Graph Generation"]
    data_rows = [data_collection, data_analysis]

    # Calculate column widths for alignment
    column_widths = []
    for index, header in enumerate(headers[2:]):  # Skip 'Step' and 'Operation' for indexing data_rows
        max_length = max(len(header), *(len(str(row[header])) for row in data_rows))
        column_widths.append(max_length)

    # Include 'Step' and 'Operation' in column width calculation
    column_widths.insert(0, max(len(steps[0]), len(steps[1]), len(headers[0])))
    column_widths.insert(1, max(len(operations[0]), len(operations[1]), len(headers[1])))

    # Print header
    header_row = " | ".join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
    print(header_row)
    print("-" * 150)  # Adjust underlining

    # Print data rows
    for step, operation, row in zip(steps, operations, data_rows):
        row_data = [step.ljust(column_widths[0]), operation.ljust(column_widths[1])]
        row_data.extend(str(row[header]).ljust(column_widths[i + 2]) for i, header in enumerate(headers[2:]))
        print(" | ".join(row_data))

def main():
    print()
    args = parse_args()
    pre_dataset = load_json(args.json_pre)
    post_dataset = load_json(args.json_post)
    data_collection_results = analyze_dependency_data(pre_dataset)
    data_analysis_results = analyze_dependency_data(post_dataset)

    print_table(data_collection_results, data_analysis_results)
if __name__ == "__main__":
    main()
    