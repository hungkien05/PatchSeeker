1) When eval llama or CR you should use eos token , Qwen is unk token , change in encode.py
        #for qwen is eos and for llama or cr is unk
        tokenizer.pad_token_id = tokenizer.eos_token_id
        tokenizer.pad_token = tokenizer.eos_token