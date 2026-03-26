import json
import math
from tqdm import tqdm
from config import (CORPUS_QUERY_RAW_JSON, CORPUS_QUERY_CORPUS_OUT,
                    CORPUS_QUERY_QUERIES_OUT, CORPUS_QUERY_QRELS_OUT,
                    CORPUS_QUERY_ALT_INPUT_JSONL, CORPUS_QUERY_ALT_QRELS_TREC)

# # Đọc file dữ liệu đầu vào laf file jsonl
# with open(CORPUS_QUERY_ALT_INPUT_JSONL, "r") as f:
#     data = [json.loads(line) for line in f]

raw_json_file = CORPUS_QUERY_RAW_JSON
with open(raw_json_file, "r",encoding = "latin-1") as f:
    data = json.load(f)

# Tạo file corpus (cve_corpus.json)
corpus = []
for item in tqdm(data, desc="Building corpus"):
    for passage in item["positive_passages"]:
        # Kiểm tra passage["text"] có rỗng hoặc là NaN, nếu đúng thì thay bằng ""
        text = passage["text"] if passage.get("text") and not (isinstance(passage["text"], float) and math.isnan(passage["text"])) else ""
        doc = {"docid": passage["docid"], "text": text, "query_id": item["query_id"], "query": item["query"]}
        # doc = {"docid": passage["docid"], "text": text, "query_id": item["query_id"], "query": item["query"]}
        corpus.append(doc)
    for passage in item["negative_passages"]:
        # Kiểm tra passage["text"] có rỗng hoặc là NaN, nếu đúng thì thay bằng ""
        text = passage["text"] if passage.get("text") and not (isinstance(passage["text"], float) and math.isnan(passage["text"])) else ""
        doc = {"docid": passage["docid"], "text": text, "query_id": item["query_id"], "query": item["query"]}
        corpus.append(doc)

with open(CORPUS_QUERY_CORPUS_OUT, "w") as f:
    json.dump(corpus, f, indent=4)

# Tạo file queries (cve_queries.json)
queries = []
for item in data:
    # Kiểm tra item["query"] có rỗng hoặc là NaN, nếu đúng thì thay bằng ""
    query_text = item["query"] if item.get("query") and not (isinstance(item["query"], float) and math.isnan(item["query"])) else ""
    query = {"query_id": item["query_id"], "query": query_text}
    queries.append(query)

with open(CORPUS_QUERY_QUERIES_OUT, "w") as f:
    json.dump(queries, f, indent=4)

# Tạo file qrels TREC

with open(CORPUS_QUERY_QRELS_OUT, "w") as f:
    for item in data:
        query_id = item["query_id"]
        for passage in item["positive_passages"]:
            f.write(f"{query_id} 0 {passage['docid']} 1\n")
        for passage in item["negative_passages"]:
            f.write(f"{query_id} 0 {passage['docid']} 0\n")

# # Tạo file qrels TREC cho top100 fusion
# with open(CORPUS_QUERY_ALT_QRELS_TREC, "w") as f:
#     for item in data:
#         query_id = item["query_id"]
#         f.write(f"{query_id} 0 {item['docid']} {item['label']}\n")
