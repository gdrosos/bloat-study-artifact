import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)
sns.set(style="whitegrid")
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['axes.labelsize'] = 23
plt.rcParams['axes.titlesize'] = 23
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['figure.figsize'] = (8, 4)

title_mapping = {
    'direct_deps_bloated_count': 'Number of dependencies',
    'direct_deps_bloated_loc': 'Size of dependencies (LoC)',
    'direct_files_bloated_count': 'Number of files',
    'direct_files_bloated_loc': 'Size of files (LoC)',
    'direct_functions_bloated_count': 'Number of functions',
    'direct_functions_bloated_loc': 'Size of functions(LoC)'
}

column_mapping = {
    'product': 'product',
    'bloated_deps_count_1': 'direct_deps_bloated_count',
    'bloated_deps_loc_1': 'direct_deps_bloated_loc',
    'bloated_files_count_1': 'direct_files_bloated_count',
    'bloated_files_loc_1': 'direct_files_bloated_loc',
    'bloated_functions_count_1': 'direct_functions_bloated_count',
    'bloated_functions_loc_1': 'direct_functions_bloated_loc',
    'used_direct_deps_count_1': 'direct_deps_used_count',
    'used_direct_deps_loc_1': 'direct_deps_used_loc',
    'used_direct_files_count_1': 'direct_files_used_count',
    'used_direct_files_loc_1': 'direct_files_used_loc',
    'used_direct_functions_count_1': 'direct_functions_used_count',
    'used_direct_functions_loc_1': 'direct_functions_used_loc',
    'transitive_bloated_dependencies_count': 'transitive_deps_bloated_count',
    'transitive_bloated_dependencies_loc': 'transitive_deps_bloated_loc',
    'transitive_bloated_files_count': 'transitive_files_bloated_count',
    'transitive_bloated_files_loc': 'transitive_files_bloated_loc',
    'transitive_bloated_functions_count': 'transitive_functions_bloated_count',
    'transitive_bloated_functions_loc': 'transitive_functions_bloated_loc',
    'transitive_used_dependencies_count': 'transitive_deps_used_count',
    'transitive_used_dependencies_loc': 'transitive_deps_used_loc',
    'transitive_used_files_count': 'transitive_files_used_count',
    'transitive_used_files_loc': 'transitive_files_used_loc',
    'transitive_used_functions_count': 'transitive_functions_used_count',
    'transitive_used_functions_loc': 'transitive_functions_used_loc',
}


def get_args():
    parser = argparse.ArgumentParser(
        description='Compare bloat prevalence metrics between direct and transitive dependencies')
    parser.add_argument("data", help="CSV with bloat metrics")
    parser.add_argument(
            "--output",
            default="figures/bloat_prevalence_direct_vs_transitive.pdf",
            help="Filename to save the bloat prevalence comparison figure.")
    return parser.parse_args()

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns=column_mapping)
    df = df[list(column_mapping.values())]
    return df



def plot_data(df, output):
    fig, axes = plt.subplots(2, 3, figsize=(9, 6))
    ax_iter = iter(axes.flatten())

    # New metrics mapping reordered for the desired sequence
    metrics_mapping = {
        'direct_deps_bloated_count': ['transitive_deps_bloated_count', 'direct_deps_used_count', 'transitive_deps_used_count'],
        'direct_files_bloated_count': ['transitive_files_bloated_count', 'direct_files_used_count', 'transitive_files_used_count'],
        'direct_functions_bloated_count': ['transitive_functions_bloated_count', 'direct_functions_used_count', 'transitive_functions_used_count'],
        'direct_deps_bloated_loc': ['transitive_deps_bloated_loc', 'direct_deps_used_loc', 'transitive_deps_used_loc'],
        'direct_files_bloated_loc': ['transitive_files_bloated_loc', 'direct_files_used_loc', 'transitive_files_used_loc'],
        'direct_functions_bloated_loc': ['transitive_functions_bloated_loc', 'direct_functions_used_loc', 'transitive_functions_used_loc'],
    }

    labels = ['Direct bloated', 'Transitive bloated', 'Direct used', 'Transitive used']
    percentages = {}
    for direct_metric, other_metrics in metrics_mapping.items():
        ax = next(ax_iter)

        # Calculate values for all 4 categories
        direct_bloated_value = df[direct_metric].sum()
        transitive_bloated_value = df[other_metrics[0]].sum()
        direct_used_value = df[other_metrics[1]].sum()
        transitive_used_value = df[other_metrics[2]].sum()

        values = [direct_bloated_value, transitive_bloated_value, direct_used_value, transitive_used_value]
        total = sum(values)
        percentages[title_mapping[direct_metric]] = [value / total * 100 for value in values]
        wedges, texts, autotexts = ax.pie(values, autopct='%1.1f%%', startangle=90, pctdistance=1.1,
                                          colors=sns.color_palette("colorblind", 4))

        # Set white edge color for each wedge
        for wedge in wedges:
            wedge.set_edgecolor('white')
        for i in range(len(autotexts) - 1):
            x1, y1 = autotexts[i].get_position()
            x2, y2 = autotexts[i + 1].get_position()
            if abs(y2 - y1) < 0.1:  # Check if y-coordinates are close
                if y1 < y2:
                    y1_new = y1 - 0.05
                    y2_new = y2 + 0.05
                else:
                    y1_new = y1 + 0.05
                    y2_new = y2 - 0.05
                autotexts[i].set(y=y1_new)
                autotexts[i + 1].set(y=y2_new)

        # Adjust font size for labels and autopct
        for text in texts + autotexts:
            text.set(size=10)

        ax.set_title(title_mapping[direct_metric], fontsize=15)

    for metric, perc_list in percentages.items():
        print()
        print(metric)
        print()
        for label, perc in zip(labels, perc_list):
            print("{:<20}: {:.2f}%".format(label, perc))

    fig.legend(wedges, labels, title="Dependency usage", loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=len(labels))

    plt.tight_layout()
    plt.savefig(output, format="pdf", bbox_inches='tight')

def main():
    args = get_args()
    df = load_and_prepare_data(args.data)


    plot_data(df, args.output)

if __name__ == "__main__":
    main()