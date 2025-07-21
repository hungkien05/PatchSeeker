#!/bin/bash

# Set the checkpoint path (update this to your actual checkpoint path)
ckpt="/mnt/moon-data/hung/neptune_data/tuanna/qwen3_8b_PF_4/checkpoint-470"
cve_corpus_dir="test_all/cve_corpus_implicit_2025_100_split/"
cve_queries_dir="test_all/cve_queries_implicit_2025_100_split"
cve_qrels_dir="test_all/cve_qrels_implicit_2025_100_split"
# Create output directories if they don't exist
base_output_dir="beir_embedding_cve_test_implicit_2025_100_qwen8b"
mkdir -p ${base_output_dir}/cve_corpus
mkdir -p ${base_output_dir}/cve_queries
mkdir -p ${base_output_dir}/rank_cve

#set the model pickle path
model_pickle_dir="pickle/qwen8b_PF_4"
mkdir -p ${model_pickle_dir}
model_pickle_path="${model_pickle_dir}/encode_model_tokenizer.pkl"
# delete the current model pickle path if you want to use a new and fresh model
# rm -rf ${model_pickle_path}



# Iterate over all CVE files in the corpus directory
for cve_file in ${cve_corpus_dir}/*.json; do
    # Extract the CVE-ID from the filename (remove path and .json extension)
    cve=$(basename "$cve_file" .json)
    
    echo "Processing ${cve}"
    python tevatron/arguments.py \
    echo "--------${cve}: Encode corpus "
    CUDA_VISIBLE_DEVICES=1 python repllama/encode_qwen.py \
      --output_dir=temp \
      --model_name_or_path $ckpt \
      --fp16 \
      --dataset_proc_num 64 \
      --per_device_eval_batch_size 64 \
      --p_max_len 512 \
      --dataset_name json \
      --train_dir ${cve_corpus_dir}/${cve}.json \
      --raw_file_path ${cve_corpus_dir}/${cve}.json \
      --encoded_save_path ${base_output_dir}/cve_corpus/${cve}.pkl \
      --encode_num_shard 1 \
      --encode_shard_index 0 \
      --model_pickle_path ${model_pickle_path}

    echo "---------${cve}: Encode queries"
    CUDA_VISIBLE_DEVICES=1 python repllama/encode_qwen.py \
      --output_dir=temp \
      --model_name_or_path $ckpt \
      --fp16 \
      --dataset_proc_num 64 \
      --per_device_eval_batch_size 64 \
      --q_max_len 512 \
      --dataset_name json \
      --train_dir ${cve_queries_dir}/${cve}.json \
      --raw_file_path ${cve_queries_dir}/${cve}.json \
      --encoded_save_path ${base_output_dir}/cve_queries/${cve}.pkl \
      --encode_is_qry \
      --model_pickle_path ${model_pickle_path}

    python -m tevatron.faiss_retriever \
    --query_reps ${base_output_dir}/cve_queries/${cve}.pkl \
    --passage_reps ${base_output_dir}/cve_corpus/${cve}.pkl \
    --depth 1000 \
    --batch_size 64 \
    --save_text \
    --save_ranking_to ${base_output_dir}/rank_cve/${cve}.txt

    python -m tevatron.utils.format.convert_result_to_trec --input ${base_output_dir}/rank_cve/${cve}.txt \
                                                           --output ${base_output_dir}/rank_cve/${cve}.trec \
                                                           --remove_query
                                                           
    
    echo "--------Completed processing ${cve}"
    python -m pyserini.eval.trec_eval -c -mrecall.100 -mndcg_cut.10 ${cve_qrels_dir}/${cve}.trec  ${base_output_dir}/rank_cve/${cve}.trec
    python -m pyserini.eval.trec_eval -c -mrecall.10  ${cve_qrels_dir}/${cve}.trec  ${base_output_dir}/rank_cve/${cve}.trec
    python -m pyserini.eval.trec_eval -c -mrecall.1  ${cve_qrels_dir}/${cve}.trec  ${base_output_dir}/rank_cve/${cve}.trec

    echo "----- Output: /raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/${base_output_dir}/rank_cve/${cve}.txt"
    echo "-----------------------------------"
    # break
done

echo "All CVE files processed successfully!"

      # --tokenizer_name Qwen/Qwen3-8B \
