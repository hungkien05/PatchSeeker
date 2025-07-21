import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from tempfile import NamedTemporaryFile
import re

import pandas as pd

from lib import setup_logger

logger =setup_logger("metric_llama2_0806.log")
metric_csv_path = "metric/metric_llama2_0806.csv"

def save_metrics_to_csv(avg_recalls, avg_mrr, avg_ndcgs, save_path, manual_efforts):
    """Save recall, MRR, and manual efforts to a CSV file."""
    data = {
        'k': list(k),
        'recall': [round(avg_recalls[ki], 3) for ki in k],
        'ndcg': [round(avg_ndcgs[ki], 3) for ki in k],  # Save NDCG values
        'manual_effort': [round(manual_efforts[k], 3) for k in manual_efforts],
        'MRR': [round(avg_mrr, 3) for _ in avg_recalls]

    }
    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False)
    
    


k = list(range(1, 11)) + [20, 50, 100, 1000]
# k = [1, 10]
recalls = {ki: 0 for ki in k}
mrr=0
ndcgs = {ki: 0 for ki in k} # Added NDCG tracking
manual_efforts_result = {ki: 0 for ki in k}  # Store manual efforts for each k
for i in k:
    # Paths
    input_dir = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/test_all/cve_qrels_0806_split"
    output_dir = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/beir_embedding_cve_test_0806_llama2/rank_cve"
    def evaluate_file(qrels_file):
        """Evaluate a single qrels file and return recall, ndcg, and mrr."""
        qrels_path = os.path.join(input_dir, qrels_file)
        result_path = os.path.join(output_dir, qrels_file)
        
        if not os.path.exists(result_path):
            return 0, 0, 0
        
        cmd = [
            "python", "-m", "pyserini.eval.trec_eval",
            "-c", 
            "-m", f"recall.{i}", 
            "-m", f"ndcg_cut.{i}",  # Now using variable k for ndcg_cut
            "-m", "recip_rank",     # Added MRR metric
            qrels_path, result_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout
            if result.returncode != 0:
                logger.error(f"Error computing {qrels_file}: {result.stderr}")
                return 0, 0, 0
                
            recall = ndcg = mrr = 0
            for line in output.splitlines():
                if f"recall_{i}" in line:
                    
                    recall = float(line.split()[-1])
                    # if i==1 and recall ==1.0:
                    #     # logger.info(f"Recall@{i}=1 for {qrels_file}: {recall}")
                    #     print(f"Recall@{i}=1 for {qrels_file}: {recall}")
                if f"ndcg_cut_{i}" in line:
                    ndcg = float(line.split()[-1])
                if "recip_rank" in line:
                    mrr = float(line.split()[-1])
            return recall, ndcg, mrr
        except Exception as e:
            logger.error(f"Error processing {qrels_file}: {e}")
            return 0, 0, 0
        
    def manual_effort(k):
        manual_efforts_sum = 0
        manual_efforts_count = 0

        for file in os.listdir(input_dir):
            if file.endswith(".trec"):
                input_dir_file = os.path.join(input_dir, file)
                if os.path.exists(input_dir_file):
                    manual_efforts_count += 1
                    with open(input_dir_file, 'r') as f:
                        first_line = f.readline().strip().split()
                        gold_doc_id = first_line[2]  

                        output_file = os.path.join(output_dir, first_line[0] + ".trec")

                        if os.path.exists(output_file):
                            with open(output_file, 'r') as output_f:
                                lines = output_f.readlines()

                                for rank_k, line in enumerate(lines[:k]):
                                    fields = line.strip().split()
                                    if fields[2] == gold_doc_id:
                                        manual_efforts_sum += min(rank_k+1, k)
                                        break
                                else:
                                    # Không tìm thấy trong danh sách => cộng thêm effort = k
                                    manual_efforts_sum += k
                        else:
                            print(f"Input file {output_file} does not exist.")
                else:
                    print(f"File {input_dir_file} does not exist.")

        print("Manual efforts count:", manual_efforts_count)
        print("Manual efforts sum:", manual_efforts_sum)
        manual_efforts = manual_efforts_sum / manual_efforts_count if manual_efforts_count > 0 else 0
        print("Manual Efforts@{}: {:.4f}".format(k, manual_efforts))
        return manual_efforts

    def main():
        global mrr
        # Collect all .trec files
        trec_files = [f for f in os.listdir(output_dir) if f.endswith(".trec")]
        if not trec_files:
            logger.error("No .trec files found.")
            return

        # Parallel processing
        total_recall = 0
        total_ndcg = 0
        total_mrr = 0
        n = 0
        
        
        with ProcessPoolExecutor() as executor:
            results = executor.map(evaluate_file, trec_files)

            for recall, ndcg, mrr in results:
                # if recall != 0 and ndcg != 0:  # Only count valid results
                total_recall += recall
                total_ndcg += ndcg
                total_mrr += mrr
                n += 1
        
        # Calculate manual efforts
        manual_efforts = manual_effort(i)
        # Print average results
        if n > 0:
            recalls[i] = total_recall / n
            print(f"total_recall: {total_recall}, n: {n}")
            ndcgs[i]= total_ndcg / n
            mrr = total_mrr / n
            manual_efforts_result[i] = manual_efforts
            logger.info(f"Recall@{i}: {total_recall / n:.10f}")
            logger.info(f"NDCG@{i}: {total_ndcg / n:.10f}")  # Now reports NDCG@k
            logger.info(f"MRR: {total_mrr / n:.10f}")       # Added MRR reporting
            logger.info(f"Manual Efforts@{i}: {manual_efforts:.4f}")
        else:
            logger.error("No valid results found.")

    if __name__ == "__main__":
        main()

save_metrics_to_csv(recalls, mrr, ndcgs, metric_csv_path, manual_efforts_result)