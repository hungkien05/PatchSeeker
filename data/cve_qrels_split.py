import os
from pathlib import Path
from collections import defaultdict

def split_trec_file(input_file, output_dir="trec_files_by_cve"):
    """Split a TREC file into separate files by CVE-ID in the first column."""
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Group lines by CVE-ID
    cve_groups = defaultdict(list)
    line_count = 0
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                # Split by whitespace and get the CVE-ID (first column)
                parts = line.split()
                if len(parts) >= 1:
                    cve_id = parts[0]
                    cve_groups[cve_id].append(line)
                    line_count += 1
    
    # Write each group to a separate file
    for cve_id, lines in cve_groups.items():
        output_file = output_path / f"{cve_id}.trec"
        with open(output_file, 'w') as f:
            for line in lines:
                f.write(f"{line}\n")
        
        print(f"Created {output_file} with {len(lines)} lines")
    
    print(f"Processed {line_count} lines into {len(cve_groups)} files")

if __name__ == "__main__":
    # Replace "trec_file.txt" with your actual TREC file path
    split_trec_file("/raid/data/hung/tuanna/tuanna/data_repllama/24_01_2026/cve_qrels.trec", "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/test_all/cve_qrels_24_01_2026_split")