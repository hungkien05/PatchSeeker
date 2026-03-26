import os

# Base directory of this config file (PatchSeeker/data/)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Base roots (relative to data/) ===
_DATA_REPLLAMA = os.path.join(_BASE_DIR, "..", "..", "tuanna", "data_repllama")
_TEVATRON_SRC = os.path.join(_BASE_DIR, "..", "..", "tuanna", "tevatron_v1", "tevatron", "src")
_CCT5_OUTPUTS = os.path.join(_BASE_DIR, "..", "..", "tuanna", "CCT5", "outputs_0706")
_GITHUB_CLONE = os.path.join(_BASE_DIR, "..", "..", "..", "code", "github_clone")

# NFS mount - cannot be relative, use env var with default
_MOON_DATA = os.environ.get(
    "PATCHSEEKER_MOON_DATA",
    "Your path to folder to store data"
)

# ============================================================
# Per-file path variables
# Each variable is named: <FILENAME>_<PURPOSE>
# ============================================================

# --- data.py ---
DATA_INPUT_CSV = os.path.join(_MOON_DATA, "wp1b_data_new", "implicit_2025_ground_truth.csv")
DATA_OUTPUT_JSON = os.path.join(_DATA_REPLLAMA, "implicit_2025_ground_truth.json")

# --- clean_data.py ---
CLEAN_DATA_INPUT = os.path.join(_DATA_REPLLAMA, "implicit_2025_ground_truth.json")
CLEAN_DATA_OUTPUT = os.path.join(_DATA_REPLLAMA, "implicit_2025_ground_truth_cleaned.json")

# --- corpus_query.py ---
CORPUS_QUERY_RAW_JSON = os.path.join(_DATA_REPLLAMA, "implicit_2025_ground_truth_cleaned.json")
CORPUS_QUERY_CORPUS_OUT = os.path.join(_DATA_REPLLAMA, "implicit_2025_100", "cve_corpus.json")
CORPUS_QUERY_QUERIES_OUT = os.path.join(_DATA_REPLLAMA, "implicit_2025_100", "cve_queries.json")
CORPUS_QUERY_QRELS_OUT = os.path.join(_DATA_REPLLAMA, "implicit_2025_100", "cve_qrels.trec")
CORPUS_QUERY_ALT_INPUT_JSONL = os.path.join(_TEVATRON_SRC, "repllama", "patchfinder_phase2", "top_100_fusion", "top_100_fusion.jsonl")  # used in commented code
CORPUS_QUERY_ALT_QRELS_TREC = os.path.join(_TEVATRON_SRC, "repllama", "patchfinder_phase2", "top_100_fusion.trec")  # used in commented code

# --- cve_corpus_split.py ---
CVE_CORPUS_SPLIT_INPUT = os.path.join(_DATA_REPLLAMA, "24_01_2026", "cve_corpus.json")
CVE_CORPUS_SPLIT_OUTPUT_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_corpus_24_01_2026_split")

# --- cve_queries_split.py ---
CVE_QUERIES_SPLIT_INPUT = os.path.join(_DATA_REPLLAMA, "24_01_2026", "cve_queries.json")
CVE_QUERIES_SPLIT_OUTPUT_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_queries_24_01_2026_split")

# --- cve_qrels_split.py ---
CVE_QRELS_SPLIT_INPUT = os.path.join(_DATA_REPLLAMA, "24_01_2026", "cve_qrels.trec")
CVE_QRELS_SPLIT_OUTPUT_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_24_01_2026_split")

# --- data_parallel.py ---
DATA_PARALLEL_INPUT_DIR = os.path.join(_GITHUB_CLONE, "wp1b_data", "pf_test_full")

# --- data_cct5.py ---
DATA_CCT5_INPUT_CSV = os.path.join(_MOON_DATA, "wp1b_data_new", "test_0806", "429.csv")

# --- final_csv.py ---
FINAL_CSV_INPUT = os.path.join(_MOON_DATA, "wp1b_data_new", "test_0806", "429.csv")
FINAL_CSV_PRED_BASE_DIR = os.path.join(_CCT5_OUTPUTS, "models", "fine-tuning", "CommitMsgGeneration")

# --- concat_data.py ---
CONCAT_DATA_BASE_DIR = os.path.join(_DATA_REPLLAMA, "test_cct5_0806")
CONCAT_DATA_JSON_INPUT = os.path.join(_DATA_REPLLAMA, "test_cct5_0806", "mf_71_cleaned.json")
CONCAT_DATA_OUTPUT_JSON = os.path.join(_DATA_REPLLAMA, "test_cct5_0806", "matched_cve_entries_71cve.json")
CONCAT_DATA_OUTPUT_DOCIDS = os.path.join(_DATA_REPLLAMA, "test_cct5_0806", "matched_docids_71cve.txt")

# --- extract_failure.py ---
EXTRACT_FAILURE_OUTPUT = os.path.join(_DATA_REPLLAMA, "metric", "qwen8b_0806_failure_top1.txt")
EXTRACT_FAILURE_QRELS_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_0806_split")
EXTRACT_FAILURE_RANK_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_0806_qwen8b", "rank_cve")
EXTRACT_FAILURE_ALT_QRELS_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_split")  # used in commented code
EXTRACT_FAILURE_ALT_RANK_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_ckpt4", "rank_cve")  # used in commented code

# --- check_duplicate.py ---
CHECK_DUPLICATE_QRELS_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_split")
CHECK_DUPLICATE_RANK_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_ckpt4", "rank_cve")  # used in commented code

# --- duplicate_removal.py ---
DUPLICATE_REMOVAL_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_ckpt4", "CCT5_old", "rank_cve")

# --- manual_recall.py ---
MANUAL_RECALL_GROUND_TRUTH = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_0806_split")
MANUAL_RECALL_INPUT_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_0806_qwen8b", "rank_cve")

# --- metric_compute.py ---
METRIC_COMPUTE_QRELS_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_0806_split")
METRIC_COMPUTE_RANK_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_0806_llama2", "rank_cve")

# --- recall_compute.py ---
RECALL_COMPUTE_QRELS_DIR = os.path.join(_TEVATRON_SRC, "test_all", "cve_qrels_split")
RECALL_COMPUTE_RANK_DIR = os.path.join(_TEVATRON_SRC, "beir_embedding_cve_test_ckpt4", "rank_cve")

# --- phase2_csv_to_json.py ---
PHASE2_INPUT_CSV = os.path.join(_TEVATRON_SRC, "repllama", "patchfinder_phase2", "top_100_fusion", "top_100_fusion.csv")
PHASE2_OUTPUT_JSONL = os.path.join(_TEVATRON_SRC, "repllama", "patchfinder_phase2", "top_100_fusion", "top_100_fusion.jsonl")
