#!/bin/bash
deepspeed --include localhost:0,2,3,6 --master_port 60000 --module tevatron.retriever.driver.train \
  --deepspeed deepspeed/ds_zero3_config.json \
  --output_dir /mnt/moon-data/hung/neptune_data/tuanna/codereviewer_pf4 \
  --model_name_or_path microsoft/codereviewer \
  --save_steps 20 \
  --dataset_name /raid/data/hung/tuanna/tuanna/data_repllama/cve_all_parrallel_4_cleaned.json \
  --query_prefix "Query: " \
  --passage_prefix "Passage: " \
  --bf16 \
  --pooling eos \
  --append_eos_token \
  --normalize \
  --temperature 0.01 \
  --per_device_train_batch_size 16 \
  --gradient_checkpointing \
  --train_group_size 21 \
  --learning_rate 1e-4 \
  --query_max_len 32 \
  --passage_max_len 196 \
  --num_train_epochs 3000 \
  --logging_steps 2 \
  --overwrite_output_dir \
  --gradient_accumulation_steps 8 \
  --warmup_steps 10 \
  --lora \
  --lora_target_modules q,k,v,o,wi,wo,down_proj,up_proj,gate_proj \
  --resume_from_checkpoint /mnt/moon-data/hung/neptune_data/tuanna/codereviewer_pf3/checkpoint-2000

  # --resume_from_checkpoint /mnt/moon-data/hung/neptune_data/tuanna/codereviewer_3/checkpoint-4400

  # --report_to wandb 


    # for llama2 7b
    # --resume_from_checkpoint checkpoint-6600 \
    # --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \

  #     --lora \
  # --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \

  # 1e-3 , 100 with cr_1_test

  #   deepspeed --include localhost:0,3,5,6 --master_port 60000 --module tevatron.retriever.driver.train \
  # --deepspeed deepspeed/ds_zero3_config.json \
  # --output_dir /mnt/moon-data/hung/neptune_data/tuanna/retrieval_cr_test \
  # --model_name_or_path microsoft/codereviewer \
  # --lora \
  # --lora_target_modules q,k,v,o,wi,wo,down_proj,up_proj,gate_proj   \
  # --save_steps 10 \
  # --dataset_name Tevatron/msmarco-passage-aug \
  # --query_prefix "Query: " \
  # --passage_prefix "Passage: " \
  # --bf16 \
  # --pooling eos \
  # --append_eos_token \
  # --normalize \
  # --temperature 0.01 \
  # --per_device_train_batch_size 128 \
  # --gradient_checkpointing \
  # --train_group_size 31 \
  # --learning_rate 1e-3 \
  # --query_max_len 32 \
  # --passage_max_len 156 \
  # --num_train_epochs 300 \
  # --logging_steps 2 \
  # --warmup_steps 50 \
  # --overwrite_output_dir \
  # --gradient_accumulation_steps 128 \
  # --resume_from_checkpoint /mnt/moon-data/hung/neptune_data/tuanna/retrieval_cr/checkpoint-220

