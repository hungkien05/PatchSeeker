# import os
# import re
# from collections import Counter

# rank_cve = "/home/huuhungn/tuanna/tevatron_v1/tevatron/src/beir_embedding_cve_test_ckpt4/rank_cve"
# seen_ids = set()
# duplicates = []

# def check_duplicate_files(directory):
#     global seen_ids, duplicates
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.trec'):
#                 file_path = os.path.join(root, file)
#                 with open(file_path, 'r') as f:
#                     for line in f:
#                         columns = line.strip().split()
#                         if len(columns) >= 3:
#                             cve_id = columns[0]
#                             q0 = columns[1]
#                             docid = columns[2]
#                             if docid in seen_ids:
#                                 # Lưu chỉ 3 trường mong muốn
#                                 duplicates.append(f"{cve_id}")
#                             else:
#                                 seen_ids.add(docid)
#     return duplicates

# # Run the function
# result = check_duplicate_files(rank_cve)

# # Đếm tần suất mỗi dòng (đã rút gọn)
# freq = Counter(result)
# result_dup = set(result)
# # In ra mỗi dòng một lần kèm theo tần suất
# for line, count in freq.items():
#     print(f"{line} [Tần suất: {count}]")

# #delete result file in rank_cve
# for file in result_dup:
#     file_path1 = os.path.join(rank_cve, f"{file}.txt")
#     file_path2 = os.path.join(rank_cve, f"{file}.trec")
#     if os.path.exists(file_path1):
#         os.remove(file_path1)
#         print(f"Đã xóa tệp: {file_path1}")
#     else:
#         print(f"Tệp không tồn tại: {file_path1}")
#     if os.path.exists(file_path2):
#         os.remove(file_path2)
#         print(f"Đã xóa tệp: {file_path2}")
#     else:
#         print(f"Tệp không tồn tại: {file_path2}")

data = """CVE-2019-15522 [Tần suất: 458]
CVE-2022-31796 [Tần suất: 906]
CVE-2017-18120 [Tần suất: 83]
CVE-2013-2220 [Tần suất: 888]
CVE-2022-29869 [Tần suất: 510]
CVE-2021-45934 [Tần suất: 85]
CVE-2021-45937 [Tần suất: 85]
CVE-2017-9205 [Tần suất: 475]
CVE-2022-2279 [Tần suất: 621]
CVE-2017-9202 [Tần suất: 475]
CVE-2022-32202 [Tần suất: 906]
CVE-2016-9843 [Tần suất: 200]
CVE-2019-13226 [Tần suất: 710]
CVE-2019-13227 [Tần suất: 710]
CVE-2015-5685 [Tần suất: 870]
CVE-2020-22875 [Tần suất: 722]
CVE-2022-30592 [Tần suất: 462]
CVE-2019-19275 [Tần suất: 775]
CVE-2016-7838 [Tần suất: 311]
CVE-2017-20006 [Tần suất: 964]
CVE-2018-14680 [Tần suất: 580]
CVE-2021-45936 [Tần suất: 85]
CVE-2018-16253 [Tần suất: 685]
CVE-2019-16347 [Tần suất: 822]
CVE-2016-9840 [Tần suất: 200]
CVE-2018-17568 [Tần suất: 494]
CVE-2019-14495 [Tần suất: 21]
CVE-2019-14934 [Tần suất: 814]
CVE-2019-3877 [Tần suất: 567]
CVE-2016-6271 [Tần suất: 652]
CVE-2018-18585 [Tần suất: 580]
CVE-2018-0429 [Tần suất: 768]
CVE-2021-32436 [Tần suất: 577]
CVE-2016-9842 [Tần suất: 200]
CVE-2021-45933 [Tần suất: 85]
CVE-2017-6439 [Tần suất: 14]
CVE-2022-25298 [Tần suất: 571]
CVE-2022-40673 [Tần suất: 450]
CVE-2020-15007 [Tần suất: 887]
CVE-2020-20740 [Tần suất: 814]
CVE-2021-3881 [Tần suất: 621]
CVE-2022-1908 [Tần suất: 621]
CVE-2019-25016 [Tần suất: 718]
CVE-2019-14323 [Tần suất: 627]
CVE-2018-10677 [Tần suất: 822]
CVE-2022-32978 [Tần suất: 906]
CVE-2016-6255 [Tần suất: 268]
CVE-2018-16150 [Tần suất: 685]
CVE-2016-9841 [Tần suất: 200]
CVE-2019-13229 [Tần suất: 710]"""

import re
import os

def extract_cve_ids(data: str) -> list[str]:
    """
    Extract CVE IDs from the given data string.

    Args:
        data (str): The input data string containing CVE IDs and their frequencies.

    Returns:
        list[str]: A list of extracted CVE IDs.
    """
    cve_ids = re.findall(r'(CVE-\d{4}-\d+)', data)
    return cve_ids
# Path to the qrel folder
qrel = "/home/huuhungn/tuanna/tevatron_v1/tevatron/src/test_all/cve_qrels_split"
cve_ids_to_remove = extract_cve_ids(data)
# Remove CVE IDs from files in the qrel folder
for root, _, files in os.walk(qrel):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        with open(file_path, 'w') as f:
            for line in lines:
                # Check if any CVE ID from cve_ids_to_remove is in the line
                should_write = True
                for cve_id in cve_ids_to_remove:
                    if cve_id in line:
                        should_write = False
                        break
                if should_write:
                    f.write(line)

print(f"Removed {len(cve_ids_to_remove)} CVE IDs from files in {qrel}")