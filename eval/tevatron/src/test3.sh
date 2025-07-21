# Attetion , if you want to encode the corpus and queries, please run change the corpus and queries path in the repllama/data.py
ckpt=checkpoint-6100

mkdir beir_embedding_cve_test
for s in 0 1 2 3;
do

echo "Encode corpus"
CUDA_VISIBLE_DEVICES=1 python repllama/encode.py \
  --output_dir=temp \
  --model_name_or_path $ckpt \
  --tokenizer_name meta-llama/Llama-2-7b-hf \
  --fp16 \
  --per_device_eval_batch_size 16 \
  --p_max_len 512 \
  --dataset_name json \
  --train_dir test_all/cve_corpus.json \
  --encoded_save_path beir_embedding_cve_test/corpus_cve.${s}.pkl \
  --encode_num_shard 4 \
  --encode_shard_index ${s}
done


echo "Encode queries"
CUDA_VISIBLE_DEVICES=1 python repllama/encode.py \
  --output_dir=temp \
  --model_name_or_path $ckpt \
  --tokenizer_name meta-llama/Llama-2-7b-hf \
  --fp16 \
  --per_device_eval_batch_size 16 \
  --q_max_len 512 \
  --dataset_name json \
  --train_dir test_all/cve_queries.json \
  --encoded_save_path beir_embedding_cve_test/queries_cve.pkl \
  --encode_is_qry

python -m tevatron.faiss_retriever \
--query_reps beir_embedding_cve_test/queries_cve.pkl \
--passage_reps 'beir_embedding_cve_test/corpus_cve.*.pkl' \
--depth 1000 \
--batch_size 64 \
--save_text \
--save_ranking_to beir_embedding_cve_test/rank.cve.txt

python -m tevatron.utils.format.convert_result_to_trec --input beir_embedding_cve_test/rank.cve.txt \
                                                       --output beir_embedding_cve_test/rank.cve.trec \
                                                       --remove_query

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mndcg_cut.10 test_all/cve_qrels.trec beir_embedding_cve_test/rank.cve.trec