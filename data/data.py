import pandas as pd
import json

file_path = "/mnt/moon-data/hung/wp1b_data_new/implicit_2025_ground_truth.csv"


# Read the CSV with the detected encoding
df = pd.read_csv(file_path, encoding='latin-1')

data_dict = {}
docid = set()  # Use a set instead of a list for faster lookups

for _, row in df.iterrows():
    cve = row["cve"]
    if cve not in data_dict:
        data_dict[cve] = {
            "query_id": cve,
            "query": row["desc_token"],
            "positive_passages": [],
            "negative_passages": []
        }
    need = ""
    commit_id = row["commit_id"]
    commit = commit_id + cve
    if commit in docid:  # Now this check is O(1) on average
        continue
    else:
        docid.add(commit)  # Adding to a set is O(1) on average
        if row["label"] == 1:
            need = "true"
            data_dict[cve]["positive_passages"].append({
                "docid": commit,
                "is_selected": need,
                "text": row["msg_token"],
                "title": " "
            })
        else:
            need = "false"
            data_dict[cve]["negative_passages"].append({
                "docid": commit,
                "is_selected": need,
                "text": row["msg_token"],
                "title": " "
            })

output_file = "/raid/data/hung/tuanna/tuanna/data_repllama/implicit_2025_ground_truth.json"

with open(output_file, "w") as f:
    json.dump(list(data_dict.values()), f, indent=4)