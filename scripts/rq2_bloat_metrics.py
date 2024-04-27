import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)
sns.set(style="whitegrid")
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 17
plt.rcParams['figure.titlesize'] = 17
plt.rcParams['figure.figsize'] = (6, 4)

def get_args():
    parser = argparse.ArgumentParser(
        description='Generate plot of distribution of bloat metrics per vulnerability exposure.')
    parser.add_argument("data", help="CSV with bloat metrics of dependencies with active or inactive invokation status")
    parser.add_argument(
            "--output",
            default="figures/bloat_metric_per_exposure.pdf",
            help="Filename to save the boxplots representing the distribution of bloat metrics per vulnerability exposure (Figure 6).")
    return parser.parse_args()

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    return df

def plot_metrics_per_exposure(df, output):
    metrics_count = ['percentage_bloated_files', 'percentage_bloated_functions']

    # Define a rename dictionary for nicer axis labels
    rename_dict = {
        'percentage_bloated_functions': 'Bloated methods',
            'percentage_bloated_files': 'Bloated files',


    }

    # Melt the DataFrame
    df_melted = df[metrics_count + ['Status']].melt(id_vars='Status', var_name='metric', value_name='value')

    # Map the metric names to more readable ones
    df_melted['metric'] = df_melted['metric'].map(rename_dict)

    df_melted['value'] = df_melted['value'] * 100  
    hue_order = ['Active', 'Inactive']
    flierprops = dict(marker='d', markerfacecolor='k', linestyle='none', markeredgecolor='k')
    # Plot
    ax = sns.boxplot(data=df_melted, x="metric", y="value", hue="Status", 
                    orient='v', linewidth=1.2, palette="colorblind", flierprops=flierprops,
                    showmeans=True,
                    meanprops={"marker":"^","markerfacecolor":"red", "markeredgecolor":"red"},
                    hue_order=hue_order)


    handles, labels = ax.get_legend_handles_labels()

    # Modify the label text where necessary
    for i, label in enumerate(labels):
        if label == 'Inactive':
            labels[i] = 'Inactive (bloated method)'

    ax.legend(handles, labels, title="Exposure Status", frameon=True, prop={"size": 12})
    plt.ylim([0, 100])
    plt.xlabel("")
    plt.ylabel("Percentage (%)")
    plt.tight_layout()
    plt.savefig(output, bbox_inches='tight',)

def print_distributions(df):
    metrics_count = ['percentage_bloated_files', 'percentage_bloated_functions']

    # Define a rename dictionary for nicer axis labels
    rename_dict = {
        'percentage_bloated_functions': 'Bloated methods',
        'percentage_bloated_files': 'Bloated files',
    }

    # Melt the DataFrame
    df_melted = df[metrics_count + ['Status']].melt(id_vars='Status', var_name='metric', value_name='value')

    # Map the metric names to more readable ones
    df_melted['metric'] = df_melted['metric'].map(rename_dict)

    # Multiply by 100 to get percentage
    df_melted['value'] = df_melted['value'] * 100  

    # Group by metric and status, and print distribution
    print("Distribution of bloat metrics per vulnerability exposure:")
    pivot_table = df_melted.groupby(['metric', 'Status'])['value'].describe()
    print(pivot_table)
    
def main():
    args = get_args()
    df = load_and_prepare_data(args.data)
    print_distributions(df)
    plot_metrics_per_exposure(df, args.output)

if __name__ == "__main__":
    main()
