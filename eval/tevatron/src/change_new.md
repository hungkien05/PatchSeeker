1) In repllama_cr.py
Before:         psg_out = self.lm_p(**psg, output_hidden_states=True)
After :         psg_out = self.lm_p.encoder(**psg, output_hidden_states=True)
2) Change in encode_cve.py
Before :        tokenizer.pad_token_id = tokenizer.unk_token_id # llama and CR
        tokenizer.pad_token = tokenizer.unk_token
        tokenizer.padding_side = "right"
After:        tokenizer.pad_token_id = tokenizer.eos_token_id # qwen only
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
