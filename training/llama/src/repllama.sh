#This script is used to train the Llama model for PatchSeeker retrieval tasks.
# deepspeed --include localhost:2,3,5,6 --master_port 60000 --module tevatron.retriever.driver.train \
#   --deepspeed deepspeed/ds_zero3_config.json \
#   --output_dir /mnt/moon-data/hung/neptune_data/tuanna/qwen3_8b_PF_4 \
#   --model_name_or_path Qwen/Qwen3-8B \
#   --lora \
#   --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \
#   --save_steps 10 \
#   --dataset_name /raid/data/hung/tuanna/tuanna/data_repllama/cve_all_parrallel_4_cleaned.json\
#   --query_prefix "Query: " \
#   --passage_prefix "Passage: " \
#   --bf16 \
#   --pooling eos \
#   --append_eos_token \
#   --normalize \
#   --temperature 0.01 \
#   --per_device_train_batch_size 64 \
#   --gradient_checkpointing \
#   --train_group_size 16 \
#   --learning_rate 1e-4 \
#   --query_max_len 32 \
#   --passage_max_len 196 \
#   --num_train_epochs 700 \
#   --logging_steps 10 \
#   --overwrite_output_dir \
#   --gradient_accumulation_steps 64 \
#   --resume_from_checkpoint /mnt/moon-data/hung/neptune_data/tuanna/qwen3_8b_PF_3/checkpoint-340\
#   --report_to wandb 


# THIS IS FOR TRAINING MSMARCO AUGMENTED DATASET
  deepspeed --include localhost:2,3,4,5 --master_port 60000 --module tevatron.retriever.driver.train \
  --deepspeed deepspeed/ds_zero3_config.json \
  --output_dir /mnt/moon-data/hung/neptune_data/tuanna/retrieval_qwen3_8b \
  --model_name_or_path Qwen/Qwen3-8B \
  --lora \
  --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \
  --save_steps 10 \
  --dataset_name Tevatron/msmarco-passage-aug \
  --query_prefix "Query: " \
  --passage_prefix "Passage: " \
  --bf16 \
  --pooling eos \
  --append_eos_token \
  --normalize \
  --temperature 0.01 \
  --per_device_train_batch_size 16 \
  --gradient_checkpointing \
  --train_group_size 31 \
  --learning_rate 1e-4 \
  --query_max_len 32 \
  --passage_max_len 156 \
  --num_train_epochs 1 \
  --logging_steps 2 \
  --overwrite_output_dir \
  --gradient_accumulation_steps 32
