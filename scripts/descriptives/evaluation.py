import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Produce statistics on the resolved and unresolved external calls during the stitching process (Table 2)')
    parser.add_argument('-csv', '--csv', required=True, help='CSV with stitching metrics')
    return parser.parse_args()


def main():
    args = parse_args()
    df = pd.read_csv(args.csv)
    total_unique_unresolved = df["unique_unresolved_count"].sum()
    total_unique_resolved = df["unique_resolved_count"].sum()
    total_calls = total_unique_resolved + total_unique_unresolved
    resolved_proportion = total_unique_resolved / total_calls
    unresolved_proportion = total_unique_unresolved / total_calls
    resolved_average = total_unique_resolved / df["product"].count()
    unresolved_average = total_unique_unresolved / df["product"].count()
    resolved_median = df["unique_resolved_count"].median()
    unresolved_median = df["unique_unresolved_count"].median()
    print()
    # Headers
    headers = ["External Calls", "Aggregate count", "Proportion of total (%)", "Average (per project)", "Median (per project)"]
    print("{:<15} {:<15} {:<25} {:<20} {:<20}".format(*headers))

    # Data rows
    print("{:<15} {:<15} {:<25.1f} {:<20.1f} {:<20.1f}".format("Resolved", total_unique_resolved, resolved_proportion * 100, resolved_average, resolved_median))
    print("{:<15} {:<15} {:<25.1f} {:<20.1f} {:<20.1f}".format("Unresolved", total_unique_unresolved, unresolved_proportion * 100, unresolved_average, unresolved_median))

if __name__ == "__main__":
    main()
