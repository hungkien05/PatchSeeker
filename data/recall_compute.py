import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from tempfile import NamedTemporaryFile
import re



k= list(range(1, 11)) + [20, 50, 100, 1000]
for i in k:
# Paths
    input_dir = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/test_all/cve_qrels_split"
    output_dir = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/beir_embedding_cve_test_ckpt4/rank_cve"

    def evaluate_file(qrels_file):
        """Evaluate a single qrels file and return recall and ndcg."""
        # print(f"Processing {qrels_file} for recall@{i} and ndcg@10")
        qrels_path = os.path.join(input_dir, qrels_file)
        result_path = os.path.join(output_dir, qrels_file)
        
        if not os.path.exists(result_path):
            return 0, 0
        
        cmd = [
            "python", "-m", "pyserini.eval.trec_eval",
            "-c", "-m", f"recall.{i}", "-m", "ndcg_cut.10",
            qrels_path, result_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout
            if result.returncode != 0:
                print(f"Error computing {qrels_file}: {result.stderr}")
                return 0, 0
            # print(f"Output: {output}")
            recall = ndcg = 0
            for line in output.splitlines():
                if f"recall_{i}" in line:
                    recall = float(line.split()[-1])
                if "ndcg_cut_10" in line:
                    ndcg = float(line.split()[-1])
            return recall, ndcg
        except Exception as e:
            print(f"Error processing {qrels_file}: {e}")
            return 0, 0

    def main():
        # Collect all .trec files
        trec_files = [f for f in os.listdir(output_dir) if f.endswith(".trec")]
        if not trec_files:
            print("No .trec files found.")
            return

        # Parallel processing
        total_recall = 0
        total_ndcg = 0
        n = 0
        
        with ProcessPoolExecutor() as executor:
            results = executor.map(evaluate_file, trec_files)

            for recall, ndcg in results:
                # if recall != 0 and ndcg != 0:  # Only count valid results
                total_recall += recall
                total_ndcg += ndcg
                n += 1
        
        # Print average results
        if n > 0:
            print(f"Recall@{i}: {total_recall / n:.10f}")
            print(f"NDCG@10: {total_ndcg / n:.10f}")
        else:
            print("No valid results found.")

    if __name__ == "__main__":
        main()

