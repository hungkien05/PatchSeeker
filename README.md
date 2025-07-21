# PatchSeeker
Replication package for the paper "PatchSeeker: Mapping NVD Records to their Vulnerability-fixing Commits with LLM Generated Commits and Embeddings".

## Setup

## Run
1) For enviroment :
+ Training llama2 7b : repllama2
+ Eval llama2 7b, CR : repllama_eval
+ Training CR : repllama2 or repllama_cr
+ Training qwen3 8b : repllama_qwen
+ Training llama3 8b and evaling qwen3 8b, llama3 8b: repllama_eval_qwen

2) To create input for model , first we need a csv file contain dataformat : ...
+ Data to train: running data/data.py to transform to json file , clean it with clean_data.py  (note that if data > 2gb you should divided it to <2 gb file )
+ Data to eval : from json clean file of data to train , run it with corpus_query.py to get corpus.json , queries.json and qrels.trec file 
+ When add cct5 , run data_cct5.py to get data for cct5 , run cct5 to get outputs folder (containing adding commit message) , run final_csv.py then run concat_data.py to get data that contain cct5 (note that only commit that <= 5 tokens are added cct5 commit message generation)
