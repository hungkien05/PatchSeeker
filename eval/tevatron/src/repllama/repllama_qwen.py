import torch
import torch.nn as nn
from torch import Tensor
from transformers import LlamaModel, PreTrainedModel
import logging
from peft import LoraConfig, get_peft_model, PeftModel, TaskType
from tevatron.modeling.encoder import EncoderModel
from transformers import AutoModel

logger = logging.getLogger(__name__)


class RepLLaMA(EncoderModel):
    def __init__(self,
                 lm_q: PreTrainedModel,
                 lm_p: PreTrainedModel,
                 pooler: nn.Module = None,
                 untie_encoder: bool = False,
                 negatives_x_device: bool = False
                 ):
        super().__init__(lm_q, lm_p, pooler, untie_encoder, negatives_x_device)
        self.config = lm_q.config

    # Existing methods (encode_passage, encode_query, compute_similarity, etc.) remain unchanged
    def encode_passage(self, psg):
        if psg is None:
            return None
        psg_out = self.lm_p(**psg, output_hidden_states=True)
        p_hidden = psg_out.hidden_states[-1]
        attention_mask = psg['attention_mask']
        sequence_lengths = attention_mask.sum(dim=1)
        last_token_indices = sequence_lengths - 1
        p_reps = p_hidden[torch.arange(p_hidden.size(0)), last_token_indices]
        p_reps = nn.functional.normalize(p_reps, p=2, dim=-1)
        return p_reps

    def encode_query(self, qry):
        if qry is None:
            return None
        qry_out = self.lm_q(**qry, output_hidden_states=True)
        q_hidden = qry_out.hidden_states[-1]
        attention_mask = qry['attention_mask']
        sequence_lengths = attention_mask.sum(dim=1)
        last_token_indices = sequence_lengths - 1
        q_reps = q_hidden[torch.arange(q_hidden.size(0)), last_token_indices]
        q_reps = nn.functional.normalize(q_reps, p=2, dim=-1)
        return q_reps

    def compute_similarity(self, q_reps, p_reps):
        return torch.matmul(q_reps, p_reps.transpose(0, 1)) / 0.01

    def gradient_checkpointing_enable(self):
        self.lm_q.base_model.gradient_checkpointing_enable()

    @classmethod
    def load(cls, model_name_or_path, **hf_kwargs):
        # Load Qwen3 model directly without LoRA
        base_model = AutoModel.from_pretrained(model_name_or_path, **hf_kwargs)
        
        # Set padding token ID if not already set
        if base_model.config.pad_token_id is None:
            base_model.config.pad_token_id = 0
        
        # Initialize RepLLaMA with the loaded model
        model = cls(
            lm_q=base_model,
            lm_p=base_model,
            pooler=None,
            untie_encoder=False
        )
        return model

    def save(self, output_dir: str):
        self.lm_q.save_pretrained(output_dir)
