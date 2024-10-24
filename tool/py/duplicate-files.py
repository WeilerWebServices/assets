#!python3

import os
from collections import defaultdict

def find_duplicates(directory):
    text_dict = defaultdict(list)

    # Scan through files in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        text_dict[line.strip()].append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Print duplicates
    for text, files in text_dict.items():
        if len(files) > 1:
            print(f'Duplicate text: "{text}" found in: {files}')

# Usage
directory_to_scan = '/Users/air/github/Projects/assets/'
find_duplicates(directory_to_scan)
