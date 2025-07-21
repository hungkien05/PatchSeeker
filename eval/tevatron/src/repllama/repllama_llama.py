import torch
import torch.nn as nn
from torch import Tensor
from transformers import LlamaModel, LlamaConfig, LlamaTokenizer
import json
import logging
from huggingface_hub import hf_hub_download
from tevatron.modeling.encoder import EncoderModel

logger = logging.getLogger(__name__)

class RepLLaMA(EncoderModel):
    def __init__(self,
                 lm_q: LlamaModel,
                 lm_p: LlamaModel,
                 pooler: nn.Module = None,
                 untie_encoder: bool = False,
                 negatives_x_device: bool = False,
                 device: str = "cuda" if torch.cuda.is_available() else "cpu"
                 ):
        super().__init__(lm_q, lm_p, pooler, untie_encoder, negatives_x_device)
        self.config = lm_q.config
        self.device = device
        self.lm_q.to(self.device)
        self.lm_p.to(self.device)

    def encode_passage(self, psg):
        if psg is None:
            return None
        psg = {k: v.to(self.device) for k, v in psg.items()}
        psg_out = self.lm_p(**psg, output_hidden_states=True)
        p_hidden = psg_out.hidden_states[-1]
        attention_mask = psg['attention_mask']
        sequence_lengths = attention_mask.sum(dim=1)
        last_token_indices = sequence_lengths - 1
        p_reps = p_hidden[torch.arange(p_hidden.size(0), device=self.device), last_token_indices]
        p_reps = nn.functional.normalize(p_reps, p=2, dim=-1)
        return p_reps

    def encode_query(self, qry):
        if qry is None:
            return None
        qry = {k: v.to(self.device) for k, v in qry.items()}
        qry_out = self.lm_q(**qry, output_hidden_states=True)
        q_hidden = qry_out.hidden_states[-1]
        attention_mask = qry['attention_mask']
        sequence_lengths = attention_mask.sum(dim=1)
        last_token_indices = sequence_lengths - 1
        q_reps = q_hidden[torch.arange(q_hidden.size(0), device=self.device), last_token_indices]
        q_reps = nn.functional.normalize(q_reps, p=2, dim=-1)
        return q_reps

    def compute_similarity(self, q_reps, p_reps):
        q_reps = q_reps.to(self.device)
        p_reps = p_reps.to(self.device)
        return torch.matmul(q_reps, p_reps.transpose(0, 1)) / 0.01
    
    def gradient_checkpointing_enable(self):
        self.lm_q.base_model.gradient_checkpointing_enable()

    @classmethod
    def load(
            cls,
            local_weights_path=None,
            device: str = "cuda" if torch.cuda.is_available() else "cpu",
            token: str = None,  # Add token for gated models
            **kwargs,
    ):
            # Use local paths
            local_weights_path = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/repllama/llama2_base/consolidated.00.pth"
            config_path = "/raid/data/hung/tuanna/tuanna/tevatron_v1/tevatron/src/repllama/llama2_base/params.json"
            
            # Load configuration from params.json
            with open(config_path, 'r') as f:
                llama_config_dict = json.load(f)
            llama_config = LlamaConfig(**llama_config_dict)
            
            # Instantiate the base model from config
            base_model = LlamaModel(llama_config)
            
            # Load the state dictionary from the local weights file
            state_dict = torch.load(local_weights_path, map_location=device)
            base_model.load_state_dict(state_dict, strict=False)
            
            # Move the model to the specified device
            base_model.to(device)
            
            # Set padding token ID if not already set
            if base_model.config.pad_token_id is None:
                base_model.config.pad_token_id = 0
            
            # Initialize RepLLaMA with the loaded model
            model = cls(
                lm_q=base_model,
                lm_p=base_model,
                pooler=None,
                untie_encoder=False,
                device=device
            )
            return model

    def save(self, output_dir: str):
        self.lm_q.save_pretrained(output_dir)