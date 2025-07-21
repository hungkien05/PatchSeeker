import os

gr_truth = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/test_all/cve_qrels_0806_split"
input_dir = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/beir_embedding_cve_test_0806_qwen8b/rank_cve"


for k in [1, 5, 10, 20, 50 ,100]:
    manual_efforts_sum = 0
    manual_efforts_count = 0

    for file in os.listdir(gr_truth):
        if file.endswith(".trec"):
            gr_truth_file = os.path.join(gr_truth, file)
            if os.path.exists(gr_truth_file):
                manual_efforts_count += 1
                with open(gr_truth_file, 'r') as f:
                    first_line = f.readline().strip().split()
                    gold_doc_id = first_line[2]  

                    input_file = os.path.join(input_dir, first_line[0] + ".trec")

                    if os.path.exists(input_file):
                        with open(input_file, 'r') as input_f:
                            lines = input_f.readlines()

                            for rank_k, line in enumerate(lines[:k]):
                                fields = line.strip().split()
                                if fields[2] == gold_doc_id:
                                    manual_efforts_sum += min(rank_k+1, k)
                                    break
                            else:
                                # Không tìm thấy trong danh sách => cộng thêm effort = k
                                manual_efforts_sum += k
                    else:
                        print(f"Input file {input_file} does not exist.")
            else:
                print(f"File {gr_truth_file} does not exist.")

    print("Manual efforts count:", manual_efforts_count)
    print("Manual efforts sum:", manual_efforts_sum)
    manual_efforts = manual_efforts_sum / manual_efforts_count if manual_efforts_count > 0 else 0
    print("Manual Efforts@{}: {:.4f}".format(k, manual_efforts))
