import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


pd.set_option('display.float_format', '{:.2f}'.format)
sns.set(style="whitegrid")
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['axes.labelsize'] = 23
plt.rcParams['axes.titlesize'] = 23
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['figure.figsize'] = (6, 4)


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate Bloat Prevalence metrics')
    parser.add_argument("data", help="CSV with bloat metrics")
    parser.add_argument(
            "--output",
            default="figures/bloat_prevalence.pdf",
            help="Filename to save the bloat prevalence figure.")
    return parser.parse_args()

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    metrics_count = ['PBD', 'PBFD', 'PBMD']
    metrics_loc = ['PBD-LOC', 'PBFD-LOC', 'PBMD-LOC']
    rename_dict = {'PBMD': 'Method', 'PBD': 'Package', 'PBFD': 'File'}
    df_total = df[['NBD', 'NBFD', 'NBMD', 'NBD-LOC', 'NBFD-LOC', 'NBMD-LOC']]
    df_count = df[metrics_count].melt(var_name='metric', value_name='value')
    df_count['Type'] = 'Bloated entries'
    df_loc = df[metrics_loc].melt(var_name='metric', value_name='value')
    df_loc['metric'] = df_loc['metric'].str.replace('-LOC', '')
    df_loc['Type'] = 'Bloated LoC'

    df_melted = pd.concat([df_count, df_loc])
    df_melted['metric'] = df_melted['metric'].map(rename_dict)
    df_melted['Type'] = pd.Categorical(df_melted['Type'], categories=['Bloated LoC', 'Bloated entries'], ordered=True)
    return df_melted, df_total

def plot_data(df, output_path):
    flierprops = dict(marker='d', markerfacecolor='k', linestyle='none', markeredgecolor='k')

    ax = sns.boxplot(data=df, x="metric", y="value", hue="Type",
                     orient='v', linewidth=1.2, palette="colorblind", flierprops=flierprops,
                     showmeans=True, meanprops={"marker":"^","markerfacecolor":"red", "markeredgecolor":"red"})
    ax.legend(title="Entity type", frameon=True, fontsize=11, title_fontsize=11)
    plt.xlabel("")
    plt.ylabel("Percentage (%)", fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')

def main():
    args = get_args()
    df, total_stats = load_and_prepare_data(args.data)

    total_entries = total_stats.describe()
    print("Absolute value bloat metric stats:\n")
    total_stats = pd.concat([total_entries, pd.DataFrame(total_stats.sum(), columns=['Sum']).T])

    print(total_stats)





    # Rename columns for clarity
    grouped_stats = df.groupby(['metric', 'Type'], observed=True).describe()
    grouped_stats.index = grouped_stats.index.rename(names=['Granularity', 'Metric'])
    grouped_stats.columns = grouped_stats.columns.set_levels(['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'], level=1)
    grouped_stats.columns = grouped_stats.columns.droplevel(0)
    grouped_stats.rename(columns={'Type': 'Metric'}, inplace=True)
    print("\nPercentage value bloat metric stats (Fig 5.):\n")
    print(grouped_stats.to_string())
    plot_data(df, args.output)

if __name__ == "__main__":
    main()