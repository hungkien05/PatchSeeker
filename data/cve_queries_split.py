import json
import os
from pathlib import Path

def split_cve_queries(input_file, output_dir="cve_query_files"):
    """Split the CVE queries into separate files by query_id (CVE-ID)."""
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Group entries by CVE-ID (query_id)
    cve_groups = {}
    for entry in data:
        cve_id = entry.get("query_id", "unknown")
        
        if cve_id not in cve_groups:
            cve_groups[cve_id] = []
        
        cve_groups[cve_id].append(entry)
    
    # Write each group to a separate file
    for cve_id, entries in cve_groups.items():
        output_file = output_path / f"{cve_id}.json"
        with open(output_file, 'w') as f:
            json.dump(entries, f, indent=4)
        
        print(f"Created {output_file} with {len(entries)} entries")
    
    print(f"Processed {len(data)} entries into {len(cve_groups)} files")

if __name__ == "__main__":
    split_cve_queries("/raid/data/hung/tuanna/tuanna/data_repllama/24_01_2026/cve_queries.json", "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/test_all/cve_queries_24_01_2026_split")