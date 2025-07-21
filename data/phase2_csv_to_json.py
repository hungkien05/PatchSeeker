import pandas as pd
import json

# Input and output file paths
csv_file = "/home/huuhungn/tuanna/rankllama_eval/tevatron/src/rankllama/patchfinder_phase2/top_100_fusion/top_100_fusion.csv"
jsonl_file = "/home/huuhungn/tuanna/rankllama_eval/tevatron/src/rankllama/patchfinder_phase2/top_100_fusion/top_100_fusion.jsonl"

# Read the CSV file
df = pd.read_csv(csv_file)

# Initialize a set to track unique docids
doc_ids = set()

# Open the output JSONL file
with open(jsonl_file, 'w', encoding='utf-8') as f:
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Create a JSON object for the row
        json_obj = {
            "docid": f"{row['commit_id']}{row['cve']}",
            "text": row['msg_token'],
            "query_id": row['cve'],
            "query": row['desc_token'],
            "label": row['label'],
            "score": row['similarity']
        }
        # Check if the docid is already seen
        if json_obj["docid"] not in doc_ids:
            # Add docid to the set
            doc_ids.add(json_obj["docid"])
            # Write the JSON object as a line
            f.write(json.dumps(json_obj, ensure_ascii=False) + '\n')

print(f"Conversion complete. JSONL file saved to: {jsonl_file}")