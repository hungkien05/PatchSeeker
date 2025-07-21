import pandas as pd
import json
import chardet
import os
import glob
from multiprocessing import Pool, Manager
import time

from lib import setup_logger

count_finish = 0
logger = setup_logger("data_parallel_test.log")
def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        detected_encoding = result['encoding']
    return detected_encoding

def process_file(file_path, shared_data_dict, shared_docid):
    """Process a single CSV file and update the shared data structures."""
    logger.info(f"Processing {file_path}...")
    start_time = time.time()
    
    # Detect the encoding
    # detected_encoding = detect_encoding(file_path)
    # logger.info(f"Detected encoding for {os.path.basename(file_path)}: {detected_encoding}")
    
    # Read the CSV with the detected encoding
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
    except pd.errors.EmptyDataError:
        logger.error(f"Error: {os.path.basename(file_path)} has no columns to parse. File might be empty or not a valid CSV.")
        return 0
    except Exception as e:
        logger.error(f"Error reading {os.path.basename(file_path)}: {e}")
        return 0
    local_updates = {}
    local_docid = set()
    
    for _, row in df.iterrows():
        cve = row["cve"]
        if cve not in local_updates:
            local_updates[cve] = {
                "query_id": cve,
                "query": row["desc_token"],
                "positive_passages": [],
                "negative_passages": []
            }
        
        commit_id = row["commit_id"]
        commit = commit_id + cve
        
        # Check if this commit is already processed
        if commit in shared_docid or commit in local_docid:
            continue
        
        local_docid.add(commit)
        
        if row["label"] == 1:
            need = "true"
            local_updates[cve]["positive_passages"].append({
                "docid": commit,
                "is_selected": need,
                "text": row["msg_token"],
                "title": " "
            })
        else:
            need = "false"
            local_updates[cve]["negative_passages"].append({
                "docid": commit,
                "is_selected": need,
                "text": row["msg_token"],
                "title": " "
            })
    
    # Update shared data structures with a lock (handled by Manager)
    for cve, data in local_updates.items():
        if cve not in shared_data_dict:
            shared_data_dict[cve] = data
        else:
            shared_data_dict[cve]["positive_passages"].extend(data["positive_passages"])
            shared_data_dict[cve]["negative_passages"].extend(data["negative_passages"])
    
    # Update shared docid
    for commit in local_docid:
        shared_docid[commit] = True
    
    elapsed_time = time.time() - start_time
    logger.info(f"Finished processing {os.path.basename(file_path)} in {elapsed_time:.2f} seconds")
    
    return len(df)

def main():
    input_dir = "/raid/data/hung/code/github_clone/wp1b_data/pf_test_full"
    output_file = "json/cve_test_full.json"
    
    # Get all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    # csv_files = csv_files[:10]
    if not csv_files:
        logger.error("No CSV files found in the input directory.")
        return
    
    logger.info(f"Found {len(csv_files)} CSV files to process.")
    
    # Create manager to share data between processes
    with Manager() as manager:
        shared_data_dict = manager.dict()
        shared_docid = manager.dict()  # Use a dict as a shared set
        
        # Process files in parallel
        total_start_time = time.time()
        
        # Number of processes to use (adjust based on your CPU)
        num_processes = os.cpu_count()
        num_processes = 64
        logger.info(f"Using {num_processes} processes for parallel processing.")
        
        with Pool(processes=num_processes) as pool:
            results = pool.starmap(
                process_file, 
                [(file, shared_data_dict, shared_docid) for file in csv_files]
            )
        
        # Convert manager.dict to regular dict for JSON serialization
        data_dict = dict(shared_data_dict)
        
        total_elapsed_time = time.time() - total_start_time
        total_rows = sum(results)
        logger.info(f"Processed {total_rows} rows from {len(csv_files)} files in {total_elapsed_time:.2f} seconds")
        
        # Write the final JSON file
        logger.info(f"Writing results to {output_file}...")
        with open(output_file, "w") as f:
            json.dump(list(data_dict.values()), f, indent=4)
        
        logger.info(f"Successfully created {output_file} with {len(data_dict)} unique CVEs")

if __name__ == "__main__":
    main()