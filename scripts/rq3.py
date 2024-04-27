import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import seaborn as sns
import argparse


sns.set(style="whitegrid")
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['axes.labelsize'] = 23
plt.rcParams['axes.titlesize'] = 23
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['figure.figsize'] = (8, 4)


def get_args():
    parser = argparse.ArgumentParser(
        description='Produce the distribution of root causes in selected 50 bloated direct dependencies')
    parser.add_argument("data", help="JSON file with the manual classification of root causes")
    parser.add_argument(
            "--output",
            default="figures/vulnerable_dep_status.pdf ",
            help="Filename to save the plot with the distribution of root causes (Figure 9).")
    return parser.parse_args()



def plot_root_cause_distribution(filepath, output):

    with open(filepath, "r") as f:
        projects = json.loads(f.read())
    root_cause_count = defaultdict(int)
    for project, dependencies in projects.items():
        for library, data in dependencies.items():
            root_cause_count[data["Root Cause"]] += 1
    labels = list(root_cause_count.keys())
    counts = list(root_cause_count.values())
    total = sum(counts)
    percentages = [count / total * 100 for count in counts]

    # Print distribution
    print("Root Cause Distribution:")
    print("--------------------------------------------")
    for label, count, percent in zip(labels, counts, percentages):
        print(f"{label}: {count}/{total} ({percent:.2f}%)")
    fig, ax = plt.subplots()
    bars = ax.barh(labels, counts, color=sns.color_palette("colorblind")[0])

    # Annotations
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}/{total}', 
                    xy=(width + 1.3, bar.get_y() + bar.get_height() / 2),
                    ha='center', va='center',
                    color='black')


    ax.set_xlim(0, max(counts) + 3)
    ax.set_xlabel('Selected dependencies')
    plt.gca().invert_yaxis()
    plt.savefig(output, bbox_inches='tight')

def main():
    args = get_args()
    plot_root_cause_distribution(args.data, args.output)

if __name__ == "__main__":
    main()
