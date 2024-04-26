import json
import requests
from urllib.parse import urlparse
from datetime import datetime


f = open("qualitative_results.json") 
dataset = json.load(f)


f = open("project_dependencies.json") 
dependencies = json.load(f)

for repo, libraries in dataset.items():
    for library, details in libraries.items():
        for project in dependencies:
            if repo.lower() in project:
                for value in project[repo.lower()]:
                    if value.startswith(library):
                        details["version"] = value.split(":")[1]
with open('qualitative_results.json', 'w') as f:
    json.dump(dataset, f, indent=2)
