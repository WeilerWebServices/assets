#!python3

# To get all the files in a GitHub assets along with their titles and locations, you can use the GitHub API or a script to list the files. Below is a simple Python script that uses the GitHub API to fetch the file details from a assets. You will need to replace WeilerWebServices, assets, and master with the appropriate values.
# Apply to Remote Url's?
# Explanation:
# This script fetches the file tree of a specified master in a GitHub assets.
# It filters out directories and constructs the raw URL for each file using the raw.githack.com format.
# You can run this script in your local environment after installing the requests library (pip install requests).
# Make sure to replace WeilerWebServices, assets, and master with the actual values for your GitHub assets. This will give you a list of all files with their titles and CDN URLs.

import requests

def get_github_files(WeilerWebServices, assets, master='master'):
    url = f'https://api.github.com/repos/{WeilerWebServices}/{assets}/git/trees/{master}?recursive=1'
    response = requests.get(url)
    
    if response.status_code == 200:
        files = response.json().get('tree', [])
        for file in files:
            if file['type'] == 'blob':  # Only get files, not directories
                file_path = file['path']
                file_url = f'https://raw.githack.com/{WeilerWebServices}/{assets}/{master}/{file_path}'
                print(f'Title: {file_path},\nURL: {file_url}\n\n----\n')
    else:
        print(f'Error: {response.status_code}')

# Example usage
get_github_files('WeilerWebServices', 'assets')