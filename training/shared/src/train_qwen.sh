#!/bin/bash
deepspeed --include localhost:0,2,3,4 --master_port 60001 --module tevatron.retriever.driver.train \
  --deepspeed deepspeed/ds_zero3_config.json \
  --output_dir "Your path to output directory" \
  --model_name_or_path Qwen/Qwen3-8B \
  --trust_remote_code True \
  --lora \
  --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \
  --lora_dropout 0.3\
  --save_steps 100 \
  --dataset_name "Your path to dataset"  \
  --query_prefix "Query: " \
  --passage_prefix "Passage: " \
  --bf16 \
  --pooling eos \
  --append_eos_token \
  --normalize \
  --temperature 0.01 \
  --per_device_train_batch_size 4 \
  --gradient_checkpointing \
  --train_group_size 16 \
  --learning_rate 5e-4 \
  --query_max_len 32 \
  --passage_max_len 196 \
  --num_train_epochs 1000 \
  --logging_steps 1 \
  --overwrite_output_dir \
  --warmup_steps 2 \
  --gradient_accumulation_steps 256\
  --report_to wandb \
  --resume_from_checkpoint "Your path to checkpoint" \
    # for llama2 7b
    # --resume_from_checkpoint checkpoint-6600 \
    # --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \

  #     --lora \
  # --lora_target_modules q_proj,k_proj,v_proj,o_proj,down_proj,up_proj,gate_proj \

