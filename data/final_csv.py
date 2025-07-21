
import csv
import sys
import os
from collections import defaultdict
import pandas as pd

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)

# Supported file type extensions
FILE_EXT_MAP = {
    'c': 'cpp',
    'cpp': 'cpp',
    'py': 'python',
    'java': 'java',
    'cs': 'cs',
    'js': 'js'
}

# Paths and settings
CSV_INPUT_PATH = "/mnt/moon-data/hung/wp1b_data_new/test_0806/429.csv"
PRED_BASE_DIR = "/raid/data/hung/tuanna/tuanna/CCT5/outputs_0706/models/fine-tuning/CommitMsgGeneration"
CHUNK_SIZE = 10000000  # Adjust based on available RAM
FILE_TYPES = list(set(FILE_EXT_MAP.values()))


def get_file_type(file_path):
    """Return mapped file type or None if unsupported."""
    ext = file_path.rsplit('.', 1)[-1].lower()
    return FILE_EXT_MAP.get(ext)


def init_output_files():
    """Remove existing concatenation files to start fresh."""
    for ft in FILE_TYPES:
        fname = f"data_concat_{ft}.csv"
        if os.path.exists(fname):
            os.remove(fname)


def process_csv_in_chunks(input_csv, chunk_size=CHUNK_SIZE):
    """Stream input CSV in chunks, extract records, and append to per-type CSVs."""
    # Ensure fresh output
    init_output_files()

    reader = pd.read_csv(input_csv, chunksize=chunk_size, encoding='latin-1')
    for chunk in reader:
        # Collect partial results by file type
        partial = defaultdict(list)
        for _, row in chunk.iterrows():
            diff = row.get("diff_token", "")
            for line in diff.splitlines():
                if line.startswith(('--- ', '+++ ')):
                    path = line.split(maxsplit=1)[1]
                    ft = get_file_type(path)
                    if isinstance(row['msg_token'], str):
                        len_text = len(row['msg_token'].split())
                    else:
                        len_text = 0                    
                    if ft:
                        partial[ft].append({
                            "cve": row["cve"],
                            "commit_id": row["commit_id"]+row["cve"],
                            "label": row["label"],
                            "cct5_msg_token": "",
                            "len_text": len_text
                        })
                    break
        # Append each file type block to its CSV
        for ft, records in partial.items():
            out_file = f"data_concat_{ft}.csv"
            df_part = pd.DataFrame(records)
            # Write header only if file is new
            header = not os.path.exists(out_file)
            df_part.to_csv(out_file, index=False, mode='a', header=header)
            print(f"Appended {len(df_part)} rows to {out_file}")


def concat_predictions_for_type(ft):
    """Merge preds lines into the corresponding CSV, writing to a new final file."""
    src_csv = f"data_concat_{ft}.csv"
    preds_txt = os.path.join(PRED_BASE_DIR, ft, f"cct5_test_new_{ft}-preds.txt")
    final_csv = f"test_0806_concat_{ft}_final.csv"

    if not (os.path.exists(src_csv) and os.path.exists(preds_txt)):
        print(f"Skipping {ft}: missing {src_csv} or {preds_txt}")
        return

    with open(src_csv, newline='', encoding='latin-1') as in_f, \
         open(preds_txt, encoding='latin-1') as pred_f, \
         open(final_csv, 'w', newline='', encoding='latin-1') as out_f:

        reader = csv.DictReader(in_f)
        writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row, pred_line in zip(reader, pred_f):
            row['cct5_msg_token'] = pred_line.strip()
            writer.writerow(row)

    print(f"Wrote merged data to {final_csv}")


def main():
    # Step 1: Extract and group diff metadata
    process_csv_in_chunks(CSV_INPUT_PATH)

    # Step 2: Concatenate predictions for each file type
    for ft in FILE_TYPES:
        concat_predictions_for_type(ft)


if __name__ == "__main__":
    main()