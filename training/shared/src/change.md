# Changes from original tevatron (unified for all models)

This is the unified training codebase for LLaMA, Qwen, and CodeReviewer.
Model-specific differences are handled via auto-detection, not separate copies.

## 1) dataset.py — smart local JSON vs HuggingFace auto-detect
- If `--dataset_name` ends with `.json`, loads as local file (for CVE data)
- Otherwise loads from HuggingFace Hub (for MS MARCO etc.)
- Also fixed bug: `self.encode_data.shard()` -> `self.train_data.shard()` in TrainDataset

## 2) encoder.py — auto-detect gradient checkpointing
- `hasattr(self.encoder, 'model')` detects causal LM (LLaMA/Qwen) vs encoder-decoder (T5/CR)
- LLaMA/Qwen: `self.encoder.model.gradient_checkpointing_enable()`
- CodeReviewer: `self.encoder.gradient_checkpointing_enable()`

## 3) encoder.py — trust_remote_code for model loading
- Reads `model_args.trust_remote_code` flag (pass `--trust_remote_code True` for Qwen)
- Passes it to `AutoModel.from_pretrained()`

## 4) dense.py — auto-detect encoder-decoder forward pass
- T5/CodeReviewer: calls `self.encoder.encoder(**qry)` (nested encoder)
- LLaMA/Qwen: calls `self.encoder(**qry)` directly
- Detection: `hasattr(self.encoder, 'encoder') and not hasattr(self.encoder, 'model')`

## 5) driver/train.py — trust_remote_code for tokenizer
- Reads `model_args.trust_remote_code` and passes to `AutoTokenizer.from_pretrained()`

## 6) driver/train.py — resume_from_checkpoint
- `trainer.train(resume_from_checkpoint=training_args.resume_from_checkpoint)`

## 7) External lib fix (deepspeed)
- Set `weights_only=False` in deepspeed torch_checkpoint_engine.py
- Path: `<conda_env>/lib/python3.10/site-packages/deepspeed/runtime/checkpoint_engine/torch_checkpoint_engine.py`

## 8) Lib versions
- xformer: 0.0.29 -> 0.0.28
- torch: 2.6.0 -> 2.4.1
- numpy: 1.24.3 -> 2.2.4

## Shell scripts
- `scripts/train_llama.sh` — LLaMA training
- `scripts/train_qwen.sh` — Qwen training (includes `--trust_remote_code True`)
- `scripts/train_codereviewer.sh` — CodeReviewer training
