1) Change lib
pyarrow : 17.0.0 -> 12.0.0
2) Change in repllama/data.py (In HFCorpus and HFQueries)
+) Before:
        data_files = data_args.encode_in_path
            if data_files:
                data_files = {data_args.dataset_split: data_files}
            self.dataset = load_dataset(data_args.dataset_name,
                                    data_args.dataset_language,
                                    data_files=data_files, cache_dir=cache_dir, use_auth_token=True)[data_args.dataset_split]
            script_prefix = data_args.dataset_name (remove this line with HFQueries)
+) After: 
        json_file_path = "/home/huuhungn/tuanna/tevatron_v1/tevatron/src/data_eval_diff/cve_corpus.json"

        self.dataset = load_dataset('json', data_files=json_file_path, split='train')
        data_args.dataset_name = "json"

3) change in repllama/encode_cve.py and encode_cr.py
add pickle save/load
Note: when run eval_xxx.sh, remember to change model_pickle_dir

4) change in repllama/encode_cve.py
add "sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))" to fix import error. 
Don't know why we have this import error

5) Qwen tokenizer eval need new version of transformers (>4.38) => use env "repllama_eval_qwen"