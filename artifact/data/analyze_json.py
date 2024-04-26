import json
import requests
from urllib.parse import urlparse
from datetime import datetime


f = open("qualitative_results.json") 
data = json.load(f)

def calculate_duration(created_at, merged_at):
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    merged_at_dt = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")
    # Calculate the difference in days
    duration_days = (merged_at_dt - created_at_dt).days
    # Adjusting to start counting from 1
    return duration_days

# Function to extract owner, repo, and PR number from PR URL
def extract_pr_details(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    owner = path_parts[0]
    repo = path_parts[1]
    pr_number = path_parts[-1]
    return owner, repo, pr_number


# Function to fetch PR creation and merge dates, and comment count
def fetch_pr_details(owner, repo, pr_number, token):
    headers = {'Authorization': f'token {token}'}
    pr_api_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}'
    comments_api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments'

    # Fetch PR details
    pr_response = requests.get(pr_api_url, headers=headers).json()
    creation_date = pr_response.get('created_at')
    merge_date = pr_response.get('merged_at')
    user_login = pr_response.get('user', {}).get('login')
    # Fetch comments and filter out those made by the PR author
    comments_response = requests.get(comments_api_url, headers=headers).json()
    external_comments_count = sum(1 for comment in comments_response if comment['user']['login'] != user_login)

    return creation_date, merge_date, external_comments_count

# Your GitHub access token
token = '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'

# Iterate over the JSON data to process each PR
for repo, libraries in data.items():
    for library, details in libraries.items():
        if details['PR Status'] == 'Merged':
            pr_url = details['PR URL']
            owner, repo, pr_number = extract_pr_details(pr_url)
            creation_date, merge_date, comments_count = fetch_pr_details(owner, repo, pr_number, token)
            
            # Here you can calculate the duration and update your data structure
            # For example:
            duration = calculate_duration(creation_date, merge_date)
            details['Duration'] = duration
            details['Created At'] = creation_date
            details['Merged At'] = merge_date

with open('qualitative_results.json', 'w') as f:
    json.dump(data, f, indent=2)
