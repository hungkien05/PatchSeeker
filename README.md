## PatchSeeker
This is the official replication package for the paper "PatchSeeker: Mapping NVD Records to their Vulnerability-fixing Commits with LLM Generated Commits and Embeddings". This repository provides the code, data processing scripts, and instructions to reproduce the experiments described in the paper.
### Overview
PatchSeeker is a framework for mapping National Vulnerability Database (NVD) records to their corresponding vulnerability-fixing commits using Large Language Models (LLMs) and embeddings. This repository includes scripts for data preparation, model training, and evaluation, leveraging models such as LLaMA2 7B, LLaMA3 8B, Qwen3 8B, and CCT5.

Our codebase is based on the implementation of Tevatron (https://github.com/texttron/tevatron)

### Real-World Impact 

We have submitted 77 VFCs that PatchSeeker found, covering 76 CVEs in 2025, to CNAs. Details can be found at this [Excel file](Submitted_VFCs_of_PatchSeeker.xlsx)
### Environment Setups


To run the experiments, set up the following environments based on the task:

- Training LLaMA2 7B: Use the repllama2 environment.
- Evaluating LLaMA2 7B and CR: Use the repllama_eval environment.
- Training CR: Use either the repllama2 or repllama_cr environment.
- Training Qwen3 8B: Use the repllama_qwen environment.
- Training LLaMA3 8B and Evaluating Qwen3 8B or LLaMA3 8B: Use the repllama_eval_qwen environment.



Set up the required environments using the provided environment configurations (e.g., requirements.txt or environment-specific setup scripts). Ensure you have the necessary dependencies installed, including Python 3.8+, PyTorch, and other libraries specified in the environment setup files.

### Checkpoint of model: 

LlaMA2 7B: https://huggingface.co/meta-llama/Llama-2-7b

LLaMA3 8B: https://huggingface.co/meta-llama/Meta-Llama-3-8B

Qwen3 8B: https://huggingface.co/Qwen/Qwen3-8B

CodeReviewer: https://huggingface.co/microsoft/codereviewer


Note: Ensure GPU support is configured if training or evaluating on GPU-enabled systems. Refer to the specific environment setup scripts for detailed instructions.
Data Preparation
To prepare the input data for training and evaluation, follow these steps:

### Datasets:

The dataset is hosted on [Academic Torrent](https://academictorrents.com/details/bbad518053332f3578794b476405555a58232d77)

### Input Data Format:

Prepare a CSV file with the following columns: `cve,owner,repo,commit_id,label,desc_token,msg_token,diff_token,source_file`. 
This CSV format are the same with PatchFinder's CSV data format (https://github.com/MarkLee131/PatchFinder).



#### Training Data:

Run data/data.py to convert the CSV file to a JSON 

Clean the JSON file using clean_data.py
Note: If the data file exceeds 2GB, split it into smaller files (<2GB each) before processing.


#### Evaluation Data:

From the cleaned JSON file, generate corpus.json, queries.json, and qrels.trec files using corpus_query.py


#### CCT5 Integration:

- To incorporate CCT5-generated commit messages:
Run data_cct5.py to prepare data for CCT5

- Run the CCT5 model to generate commit messages, storing results in an outputs folder: https://github.com/Ringbo/CCT5

- Process the CCT5 outputs using final_csv.py:python data/final_csv.py

- Concatenate the data with concat_data.py to include CCT5 commit messages (only for commits with ≤5 tokens)



### Running Experiments
To run the training and evaluation experiments, follow these steps:

- Training:

Step 1: Train the model on the Ms_macro_aug dataset from Hugging Face(In the src/tevatron/retriever/dataset.py, you should use code for Ms_macro_aug)


Step 2: Train the model on your prepared dataset(In the src/tevatron/retriever/dataset.py, you should use code for Checkpoint)

Script to train : PatchSeeker/training/llama/src/repllama.sh
Run in terminal , cd to the /src and run: bash repllama.sh > repllama_model.log 2>&1

Note: Use the --resume_from_checkpoint flag to continue training from a previous checkpoint if needed



- Evaluation:

Read the sh file and you might need to change checkpoint_path , tokenize_name base on the model you are using: 
bash eval_cve_llama2.sh > eval_llama2_mf.log 2>&1

Ensure the number of GPUs for evaluation matches the training configuration.


- Scripts:

All training and evaluation scripts are located in the {model}/src . Review and modify the .sh files as needed to adjust paths, hyperparameters, or GPU settings.



### Notes

- GPU Requirements: Ensure the number of GPUs used for training and evaluation is consistent to avoid compatibility issues.
- Data Size: Split large data files (>2GB) to ensure compatibility with processing scripts.
- CCT5 Integration: Only commits with ≤5 tokens are augmented with CCT5-generated commit messages to maintain efficiency.
- Checkpoints: Save and manage checkpoints carefully to avoid overwriting. Use the --resume_from_checkpoint option to resume training from a specific checkpoint.
- Dependencies: Ensure all required libraries (e.g., PyTorch, Hugging Face Transformers) are installed in the specified environments (repllama2, repllama_eval, etc.).





### Acknowledgement
We want to thank the authors of CCT5 (https://github.com/Ringbo/CCT5), Tevatron (https://github.com/texttron/tevatron) and PatchFinder (https://github.com/MarkLee131/PatchFinder)