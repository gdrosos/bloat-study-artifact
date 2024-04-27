import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_args():
    parser = argparse.ArgumentParser(
        description='Generate Vulnerable Dependency Activation Status plot')
    parser.add_argument("data", help="CSV with vulnerable dependency activation status data")
    parser.add_argument(
            "--output",
            default="figures/vulnerable_dep_status.pdf ",
            help="Filename to save the vulnerable dependency activation status plot (Figure 8).")
    return parser.parse_args()

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    return df

def plot_dependency_activation_status(df, output):
    sns.set(style="whitegrid")
    plt.rcParams['font.monospace'] = 'Inconsolata Medium'
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['xtick.labelsize'] = 13
    plt.rcParams['ytick.labelsize'] = 13
    plt.rcParams['legend.fontsize'] = 18
    plt.rcParams['figure.titlesize'] = 24
    plt.rcParams['figure.figsize'] = (8, 4)

    label_mapping = {
        'Active': 'Active',
        'Undefined': 'Undefined',
        'Bloated': 'Inactive (bloated dependency)',
        'Inactive': 'Inactive (bloated method)',
    }

    # Count the occurrences of each activation_status and separate them by status
    grouped_df = df.groupby(['activation_status', 'dependency_type']).size().reset_index(name='counts')

    # Get unique activation_status values
    activation_statuses = df['activation_status'].unique()

    # Sort activation_statuses by total counts
    sorted_activation_statuses = grouped_df.groupby('activation_status')['counts'].sum().sort_values(ascending=False).index.tolist()

    # Use a grayscale color palette
    statuses = df['dependency_type'].unique()
    palette = sns.color_palette("colorblind", len(statuses))
    color_dict = dict(zip(statuses, palette))

    fig, ax = plt.subplots()

    # Create bars for each activation_status and color them by status
    bottoms = {activation_status: 0 for activation_status in sorted_activation_statuses}
    for activation_status in sorted_activation_statuses:  
        rows = grouped_df[grouped_df['activation_status'] == activation_status]
        for index, row in rows.iterrows():
            ax.barh(label_mapping[row['activation_status']], row['counts'], color=color_dict[row['dependency_type']], 
                    left=bottoms[row['activation_status']], edgecolor=None, label=row['dependency_type'])
            bottoms[row['activation_status']] += row['counts']

        # Annotating total at the end of the bar
        total = bottoms[activation_status]
        ax.annotate(f'{total}/'+f'{df["project"].count()}', 
                    xy=(total + 70, label_mapping[activation_status]), 
                    ha='center', va='center',
                    color='black')

    # Create a legend for each status
    handles = [plt.Rectangle((0,0),1,1, color=color_dict[label]) for label in statuses]
    ax.legend(handles, statuses, title='Status', fontsize=11, title_fontsize=11, loc='lower right')

    ax.set_xlabel('Dependencies to vulnerable releases', fontsize=23)
    ax.set_xlim(0, 750 + 100)  # Adjusted xlim to accommodate the annotations

    plt.gca().invert_yaxis()

    plt.savefig(output, bbox_inches='tight')
    print("Vulnerable Dependency Activation Status:\n")
    table = grouped_df.pivot_table(index='activation_status', columns='dependency_type', values='counts', fill_value=0).round().astype(int)
    table.rename(index=label_mapping, columns=label_mapping, inplace=True)

    # Calculate sums for rows and columns
    table['Total'] = table.sum(axis=1)
    table.loc['Total'] = table.sum()

    # Print the pivot table with sums
    print(table)
    print()
    print("Number of projects depending on at least one vulnerable release:",df["project"].value_counts().count())

def main():
    args = get_args()
    df = load_and_prepare_data(args.data)
    plot_dependency_activation_status(df, args.output)

if __name__ == "__main__":
    main()
