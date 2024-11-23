#!/usr/bin/env python3

import os

def add_text_to_filename(directory, text_to_add):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            base, ext = os.path.splitext(filename)
            new_filename = f"{text_to_add}_{base}{ext}"
            new_file_path = os.path.join(directory, new_filename)
            os.rename(file_path, new_file_path)

if __name__ == "__main__":
    directory = "/Users/air/github/Projects/assets/big"  # Replace with your actual directory
    text_to_add = "big-"  # Replace with the text you want to add
    add_text_to_filename(directory, text_to_add)

