import os
import re

def process_directory(directory_path):
    # Get all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        remove_duplicates(file_path)
        # print(f"Processed: {file_path}")

def remove_duplicates(file_path):
    # Read all lines from the file
    if not file_path.endswith('.trec'):
        return
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Create a dictionary to track unique entries
    unique_lines = {}
    
    for line in lines:
        # Split the line by whitespace
        parts = line.strip().split()
        
        # Skip lines that don't have enough columns
        if len(parts) < 6:  # Assuming we need at least 7 columns (considering we're looking at last column)
            continue
        
        # Create a key using the first 3 columns and last column
        # This ignores the 4th, 5th, and 6th columns
        key = ' '.join(parts[:3] + [parts[-1]])
        # print(f"Key: {key}")
        # Keep the first occurrence of each unique combination
        if key not in unique_lines:
            unique_lines[key] = line
            
    
    # Write the unique lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(unique_lines.values())

# Usage example
if __name__ == "__main__":
    import sys
    directory_path = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/beir_embedding_cve_test_ckpt4/CCT5_old/rank_cve"
    
    process_directory(directory_path)
    print("Done! Duplicate lines have been removed from all files.")