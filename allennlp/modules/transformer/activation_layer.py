from typing import Union
import torch

from allennlp.common import FromParams

from allennlp.modules.transformer.transformer_module import TransformerModule

from transformers.modeling_bert import ACT2FN


class ActivationLayer(TransformerModule, FromParams):
    def __init__(
        self,
        hidden_size: int,
        intermediate_size: int,
        activation: Union[str, torch.nn.Module],
    ):
        super().__init__()
        self.dense = torch.nn.Linear(hidden_size, intermediate_size)
        if isinstance(activation, str):
            self.act_fn = ACT2FN[activation]
        else:
            self.act_fn = activation

    def forward(self, hidden_states, pool=False):
        if pool:
            hidden_states = hidden_states[:, 0]
        hidden_states = self.dense(hidden_states)
        hidden_states = self.act_fn(hidden_states)
        return hidden_states
