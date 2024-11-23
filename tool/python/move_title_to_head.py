import os
import re

def move_title_to_head(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Check if <title> is outside <head>
    if '<title>' in content and '</head>' in content:
        head_end_index = content.index('</head>')
        title_match = re.search(r'<title>.*?</title>', content, re.DOTALL)
        
        if title_match:
            title_tag = title_match.group(0)
            content = content.replace(title_tag, '')  # Remove the title tag from its current position
            content = content[:head_end_index] + title_tag + content[head_end_index:]  # Insert the title tag before </head>

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated: {file_path}")
        else:
            print(f"No <title> tag found in {file_path}")
    else:
        print(f"No <title> tag or </head> tag found in {file_path}")

def process_html_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                move_title_to_head(file_path)

# Replace 'your_directory_path' with the path to your HTML files
process_html_files('your_directory_path')