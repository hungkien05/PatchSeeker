import pandas as pd
import json
import os
from pathlib import Path
from tqdm import tqdm
import ijson

def build_docid_hashmap(csv_files):
    """Build a hashmap of docid to cct5_msg_token from all CSV files."""
    docid_to_cct5 = {}
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file,encoding='latin-1')
            for _, row in df.iterrows():
                if row['len_text'] <=5 :
                    docid = row['commit_id']
                    cct5_msg_token = row['cct5_msg_token']
                    docid_to_cct5[docid] = cct5_msg_token
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    return docid_to_cct5

def process_json_file(json_file_path, docid_to_cct5, matched_entries, matched_docids):
    """Process a JSON file, update text for matching docids, collect matched CVE entries, and log matched docids."""
    try:
        match_count = 0  # Initialize counter for matched passages
        n = 0
        with open(json_file_path, 'r', encoding='latin-1') as f:
            # Use ijson to stream JSON objects
            parser = ijson.items(f, 'item')
            for cve_entry in parser:
                # Create a copy to avoid modifying the original data unnecessarily
                updated_entry = cve_entry.copy()
                updated = False
                
                # Check positive_passages
                if 'positive_passages' in updated_entry:
                    for passage in updated_entry['positive_passages']:
                        if passage['docid'] in docid_to_cct5:
                            passage['text'] = f"{passage['text']} {docid_to_cct5[passage['docid']]}"
                            updated = True
                            match_count += 1  # Increment counter for each match
                            matched_docids.append(passage['docid'])  # Log matched docid
                
                # Check negative_passages
                if 'negative_passages' in updated_entry:
                    for passage in updated_entry['negative_passages']:
                        if passage['docid'] in docid_to_cct5:
                            passage['text'] = f"{passage['text']} {docid_to_cct5[passage['docid']]}"
                            updated = True
                            match_count += 1  # Increment counter for each match
                            matched_docids.append(passage['docid'])  # Log matched docid
                
                # If any passage was updated, add the entire CVE entry to matched_entries
                # if updated:
                n +=1
                matched_entries.append(updated_entry)
                    
        print(f"Finished processing {json_file_path} with {match_count} matched passages")
        return True, match_count,n  # Return success status and match count
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {json_file_path}: {e}")
        return False, 0  # Return 0 matches on error
    except IOError as e:
        print(f"Error accessing file {json_file_path}: {e}")
        return False, 0  # Return 0 matches on error

def save_matched_entries(matched_entries, output_json_path):
    """Save matched CVE entries to a new JSON file."""
    try:
        with open(output_json_path, 'w', encoding='latin-1') as f:
            json.dump(matched_entries, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(matched_entries)} matched CVE entries to {output_json_path}")
    except IOError as e:
        print(f"Error writing to {output_json_path}: {e}")

def save_matched_docids(matched_docids, output_docids_path):
    """Save matched docids to a text file."""
    try:
        with open(output_docids_path, 'w', encoding='latin-1') as f:
            for docid in matched_docids:
                f.write(f"{docid}\n")
        print(f"Saved {len(matched_docids)} matched docids to {output_docids_path}")
    except IOError as e:
        print(f"Error writing to {output_docids_path}: {e}")

def main():
    # Define paths and input
    csv_files = [f"/raid/data/hung/tuanna/tuanna/data_repllama/test_cct5_0806/test_0806_concat_{name}_final.csv" for name in ['cpp', 'cs', 'js', 'java', 'python']]
    json_files = [
        "/raid/data/hung/tuanna/tuanna/data_repllama/test_cct5_0806/mf_71_cleaned.json"
    ]
    output_json_path = "/raid/data/hung/tuanna/tuanna/data_repllama/test_cct5_0806/matched_cve_entries_71cve.json"
    output_docids_path = "/raid/data/hung/tuanna/tuanna/data_repllama/test_cct5_0806/matched_docids_71cve.txt"

    # Build hashmap from CSV files
    print("Building docid hashmap from CSV files...")
    docid_to_cct5 = build_docid_hashmap(csv_files)
    print(f"Hashmap built with {len(docid_to_cct5)} docid entries.")

    # Process each JSON file and collect matched CVE entries and docids
    matched_entries = []
    matched_docids = []  # List to store matched docids
    total_match_count = 0  # Initialize total match counter
    for json_file in tqdm(json_files, desc="Processing JSON files"):
        if os.path.exists(json_file):
            success, match_count ,n = process_json_file(json_file, docid_to_cct5, matched_entries, matched_docids)
            if success:
                total_match_count += match_count  # Aggregate match count
        else:
            print(f"JSON file {json_file} does not exist.")

    # Print total number of matched passages
    print(f"Total number of matched passages: {total_match_count}")
    print(f"Total number of CVE: {n}")


    # Save matched entries to a new JSON file
    if matched_entries:
        save_matched_entries(matched_entries, output_json_path)
    else:
        print("No matched CVE entries found.")

    # Save matched docids to a text file
    if matched_docids:
        save_matched_docids(matched_docids, output_docids_path)
    else:
        print("No matched docids found.")

if __name__ == "__main__":
    main()