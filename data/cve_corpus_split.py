import json
import os
import re
from pathlib import Path

def extract_cve_id(docid):
    """Extract the CVE-ID from the end of the docid field."""
    match = re.search(r'(CVE-\d{4}-\d+)$', docid)
    if match:
        return match.group(1)
    return "unknown"


def filter_commit_messages(msg):
    """Filter commit messages to remove unwanted characters."""
    # Remove newlines and extra spaces
    msg = msg.replace("\n", " ")
    msg = msg.replace("()", " ")
    
    #remove hex numbers
    msg = re.sub(r'\b0x[0-9a-fA-F]+\b', '', msg)
    # Remove # format hex numbers
    msg = re.sub(r'#[0-9a-fA-F]+\b', '', msg)
    # Remove h suffix format hex numbers
    msg = re.sub(r'\b[0-9a-fA-F]+h\b', '', msg)
    msg = re.sub(r'\b[0-9a-fA-F]*[a-fA-F]+[0-9a-fA-F]*\b', '', msg)
    
    # Remove standalone hex sequences that contain at least one hex letter
    msg = re.sub(r'\b[0-9a-fA-F]*[a-fA-F]+[0-9a-fA-F]*\b', '', msg)
    # Remove Unicode escape sequences like \u003, \u0123, etc.
    msg = re.sub(r'\\u[0-9a-fA-F]{1,6}', '', msg)
    # Remove other Unicode escape sequences like \U00000123
    msg = re.sub(r'\\U[0-9a-fA-F]{1,8}', '', msg)
    # Remove other common escape sequences
    msg = re.sub(r'\\x[0-9a-fA-F]{2}', '', msg)  # \x12 format
    # Optional: Remove non-ASCII characters (uncomment if needed)
    msg = re.sub(r'[^\x00-\x7F]+', '', msg)
    
    # Clean up multiple spaces that might result from the replacements
    msg = re.sub(r'\s+', ' ', msg)
    return msg.strip()

def split_cve_corpus(input_file, output_dir="cve_files"):
    """Split the CVE corpus into separate files by CVE-ID."""
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Group entries by CVE-ID
    cve_groups = {}
    for entry in data:
        docid = entry.get("docid", "")
        cve_id = extract_cve_id(docid)
        # if cve_id not in failed_cve_ids:
        #     continue
        if cve_id not in cve_groups:
            cve_groups[cve_id] = []
        entry["text"] = filter_commit_messages(entry["text"])  # Replace newlines with spaces
        cve_groups[cve_id].append(entry)
    
    # Write each group to a separate file
    for cve_id, entries in cve_groups.items():
        output_file = output_path / f"{cve_id}.json"
        with open(output_file, 'w') as f:
            json.dump(entries, f, indent=4)
        
        print(f"Created {output_file} with {len(entries)} entries")
    
    print(f"Processed {len(data)} entries into {len(cve_groups)} files")

if __name__ == "__main__":
    split_cve_corpus("/raid/data/hung/tuanna/tuanna/data_repllama/24_01_2026/cve_corpus.json", "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/test_all/cve_corpus_24_01_2026_split")
    # print(filter_commit_messages("do fffff9abcfb dcm \\u003 i do work func() \n i work"))