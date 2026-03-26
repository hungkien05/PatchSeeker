#The name of top 1000 that repllama can't find
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from config import (EXTRACT_FAILURE_OUTPUT, EXTRACT_FAILURE_QRELS_DIR,
                    EXTRACT_FAILURE_RANK_DIR, EXTRACT_FAILURE_ALT_QRELS_DIR,
                    EXTRACT_FAILURE_ALT_RANK_DIR)

# Chọn danh sách giá trị k để tính Recall@k
ks = [1]  # Bạn có thể thêm các giá trị khác: [1, 5, 10, 20, 100, 1000, ...]
k_ndcg =1
output_path = EXTRACT_FAILURE_OUTPUT
# Thư mục chứa file qrels và kết quả xếp hạng
input_dir = EXTRACT_FAILURE_QRELS_DIR
output_dir = EXTRACT_FAILURE_RANK_DIR

# input_dir = EXTRACT_FAILURE_ALT_QRELS_DIR
# output_dir = EXTRACT_FAILURE_ALT_RANK_DIR

def evaluate_file(qrels_file, k_val):
    """Evaluate a single qrels file and return recall and ndcg."""
    qrels_path = os.path.join(input_dir, qrels_file)
    result_path = os.path.join(output_dir, qrels_file)

    if not os.path.exists(result_path):
        return 0, 0

    cmd = [
        "python", "-m", "pyserini.eval.trec_eval",
        "-c", "-m", f"recall.{k_val}", "-m", f"ndcg_cut.{k_ndcg}",
        qrels_path, result_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        recall = ndcg = 0
        for line in output.splitlines():
            if f"recall_{k_val}" in line:
                recall = float(line.split()[-1])
            if f"ndcg_cut_{k_ndcg}" in line:
                ndcg = float(line.split()[-1])
        return recall, ndcg
    except Exception as e:
        print(f"Error processing {qrels_file}: {e}")
        return 0, 0

def evaluate_with_name(args):
    """Wrapper to allow ProcessPoolExecutor with multiple arguments."""
    qrels_file, k_val = args
    recall, ndcg = evaluate_file(qrels_file, k_val)
    return qrels_file, recall, ndcg

def main():
    # Lặp qua các giá trị k cần đánh giá
    cve_set = set()
    for k_val in ks:
        # Lấy danh sách các file .trec
        trec_files = [f for f in os.listdir(input_dir) if f.endswith(".trec")]
        if not trec_files:
            print("No .trec files found.")
            continue

        total_recall = 0
        total_ndcg = 0
        n = 0

        with ProcessPoolExecutor() as executor:
            # Dùng executor.map với danh sách tham số dạng tuple
            results = executor.map(evaluate_with_name, [(f, k_val) for f in trec_files])

            for qrels_file, recall, ndcg in results:
                if recall == 0: ## change 0 or 1 depends on what you want: failure or success
                    cve_id = qrels_file.split(".")[0]
                    cve_set.add(cve_id)
                    print(f"Processed file: {qrels_file} | Recall@{k_val}: {recall:.4f}, NDCG@{k_ndcg}: {ndcg:.4f}")
                total_recall += recall
                total_ndcg += ndcg
                n += 1

        # In kết quả trung bình
        if n > 0:
            print(f"\n📊 Tổng kết với k = {k_val}")
            print(f"Recall@{k_val}: {total_recall / n:.10f}")
            print(f"NDCG@10: {total_ndcg / n:.10f}\n")
        else:
            print(f"No valid results found for k = {k_val}")

    # output cve_set to a text file
    with open(output_path, "w") as f:
        for cve_id in sorted(cve_set):
            f.write(f"{cve_id}\n")
if __name__ == "__main__":
    main()