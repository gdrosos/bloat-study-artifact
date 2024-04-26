import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tabulate import tabulate
from matplotlib.patches import Patch

sns.set(style="whitegrid")
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['figure.figsize'] = (10, 4)


def get_args():
    parser = argparse.ArgumentParser(description='Analyze PR status and effects on dependency reduction')
    parser.add_argument("data", help="Path to the JSON file containing PR data")
    parser.add_argument("--table3", help="Produce data from table 3", action='store_true')
    parser.add_argument("--output_fig_10", default=None, help="Filename for the output plot.")
    parser.add_argument("--output_fig_11", default=None, help="Filename for the output plot.")
    parser.add_argument("--output_fig_12", default=None, help="Filename for the output plot.")

    return parser.parse_args()


def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def process_data(projects, output, produce_table):
    causes = {}
    statuses = ["Merged", "Approved", "Pending", "Rejected"]
    loc = 0
    projects_per_status = {s: set() for s in statuses}  # Track unique projects per status
    for project, deps in projects.items():
        for dep, details in deps.items():
            if details["PR Status"]=="Merged":
                loc+= details["LoC"]
            cause = details["Root Cause"]
            status = details["PR Status"]
            if status in statuses:
                if cause not in causes:
                    causes[cause] = {s: 0 for s in statuses}
                causes[cause][status] += 1
                projects_per_status[status].add(project)
    labels = list(causes.keys())
    bottom = np.zeros(len(labels))
    if output:
        color_palette = plt.colormaps['RdYlGn']

        # Explicitly choose color points from the color map
        colors = [color_palette(i) for i in np.linspace(1, 0, 4)]
        # Adjusting the figure size based on the number of labels
        fig, ax = plt.subplots(figsize=(8, 4))

        for i, status in enumerate(statuses):
            counts = [causes[label][status] for label in labels]
            ax.barh(labels, counts, left=bottom, label=status, height=0.5, color=colors[i])  # Adjust bar thickness with height
            bottom += counts

        # Set xlabel with appropriate font size
        ax.set_xlabel('Bloated dependencies')

        # Create space to the right of the plot
        fig.subplots_adjust(right=0.7)

        # Adjust the yticks and xticks font sizes

        # Set the legend outside the plot on the right
        legend = ax.legend(loc='center right', prop={"size": 12})

        legend.set_title("PR Status", prop={"size": 14})
        ax.set_xlim(0, 16)  # Adjust x-axis limits

        plt.gca().invert_yaxis() 
        plt.savefig(output, bbox_extra_artists=(legend,), bbox_inches='tight')
        print_detailed_table(causes)
        print()
    if produce_table:
        print_table(projects_per_status, causes)
        print()
        print("Number of LoC removed:", loc)


def print_detailed_table(causes):
    rows = []
    for cause, statuses in causes.items():
        for status, count in statuses.items():
            rows.append([cause, status, count])
    
    # Sort rows for better readability, first by cause, then by status if you want
    rows.sort(key=lambda x: (x[0], x[1]))
    
    print(tabulate(rows, headers=['Root Cause', 'PR Status', 'Count'], tablefmt='grid'))


def print_table(projects_per_status, causes):
    statuses = ["Merged", "Approved", "Pending", "Rejected"]

    rows = []
    for status in statuses:
        num_prs = len(projects_per_status[status])
        num_deps_removed = sum(causes[cause][status] for cause in causes if status in causes[cause])
        rows.append([status, num_prs, num_deps_removed])
    
    total_prs = sum(len(projects_per_status[s]) for s in projects_per_status)
    total_deps_removed = sum(sum(causes[c][s] for c in causes) for s in statuses)
    rows.append(["Total", total_prs, total_deps_removed])
    
    print(tabulate(rows, headers=['PR Status', 'Number of PRs', 'Number of  BD removed'], tablefmt='grid'))

def plot_discussions(projects, outfile):
    colors_discussions = sns.color_palette("colorblind", 5)
    discussion_categories = ['No Discussion', 'Discussions Involving Changes', 'Discussions without Requiring Changes']
    discussion_counts = {}
    
    for project_name, deps in projects.items():
        for dep_name, details in deps.items():
            if "Discussion Status" in details:
                status = details["Discussion Status"]
                if status in discussion_counts:
                    discussion_counts[status] += 1
                else:
                    discussion_counts[status] = 1
                break
    discussion_counts = sorted(discussion_counts.values(), reverse=True)
    print("Merged PRs requiring no discussion:", discussion_counts[0])
    print("Merged PRs requiring discussions involving changes:", discussion_counts[1])
    print("Merged PRs requiring discussions without requiring changes:", discussion_counts[2])

    create_stacked_bar_chart(
        discussion_categories, 
        discussion_counts, 
        colors_discussions, 
        'Summary of Discussions on Merged Pull Requests', 
        outfile,
        "Discussion Summary"
    )
def plot_durations(projects, outfile):
    data = projects
    # Create lists to store merged_at dates
    same_date = set()
    within_week = set()
    within_month = set()

    remaining = set()

    # Convert string dates to datetime objects and categorize PRs
    for repo, pr_data in data.items():
        for pr, pr_info in pr_data.items():
            duration = pr_info.get('Duration', -111)
            if duration>=0:
                if duration <1:
                    same_date.add(repo)
                elif duration < 8:
                    within_week.add(repo)
                elif duration < 32:
                    within_month.add(repo)
                else:
                    remaining.add(repo)

    # Output the results
    print("Pull Requests Merged on the Same Date:", len(same_date))
    print("Pull Requests Merged Within Week:", len(within_week))
    print("Pull Requests Merged Within Month:", len(within_month))
    print("Pull Requests Merged more than Month:", len(remaining))
    duration_counts = [len(same_date), len(within_week), len(within_month),  len(remaining)]
    colors_durations = sns.color_palette("colorblind", 4)
    duration_categories = ['Same Day', '1 Day to 1 Week', '1 Week to 1 Month', 'Over 1 Month']
    create_stacked_bar_chart(
        duration_categories, 
        duration_counts, 
        colors_durations, 
        'Duration of Merged Pull Requests', 
        outfile,
        "Duration"
    )

def create_stacked_bar_chart(categories, counts, colors, title, filename, legend_title):
    # Calculate percentages and labels
    total = sum(counts)
    percentages = [count / total * 100 for count in counts]
    labels = [f'{count} \n({percent:.0f}%)' for percent, count in zip(percentages, counts)]
    
    # Create figure and bar chart
    fig, ax = plt.subplots(figsize=(10, 2))  # Figure size can be adjusted
    left = 0
    for idx, (count, label) in enumerate(zip(counts, labels)):
        # ax.barh(0, count+4, left=left, color=colors[idx], edgecolor='white')
        # ax.text(left + (count+2) / 2, 0, label, ha='center', va='center', fontsize=15, color='black',   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
        # left += count
        # Adjusting bar width by adding an offset
        bar_width = count + 4
        ax.barh(0, bar_width, left=left, color=colors[idx], edgecolor='white')
        
        # Check if there is enough space to draw the text without overlap
        if idx < len(counts) - 1 and (left + bar_width + counts[idx+1]/2) < (left + bar_width + counts[idx+1] + 2):
            # Not enough space for the next text, only draw if this is the larger segment
            ax.text(left +2+ count / 2, 0, label, ha='center', va='center', fontsize=15, color='black',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
        else:
            # Enough space, draw the text
            ax.text(left + 2+count / 2, 0, label, ha='center', va='center', fontsize=15, color='black',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
        
        left += bar_width 
    # Set title and remove axes
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.axis('off')

    # Create and set custom legend
    legend_handles = [Patch(facecolor=colors[i], label=categories[i]) for i in range(len(categories))]
    ax.legend(handles=legend_handles, bbox_to_anchor=(1, 1), fontsize=14, title=legend_title, title_fontsize=14)

    # Save the plot as a PDF
    plt.tight_layout()
    plt.savefig(filename, format="pdf", bbox_inches='tight')

def main():
    args = get_args()
    projects = load_data(args.data)
    process_data(projects, args.output_fig_10, args.table3)
    if args.output_fig_11:
        plot_durations(projects, args.output_fig_11)
    if args.output_fig_12:
        plot_discussions(projects, args.output_fig_12)
if __name__ == "__main__":
    main()
