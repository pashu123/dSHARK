import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from shark.shark_runner import SharkInference

torch.manual_seed(0)
tokenizer = AutoTokenizer.from_pretrained("microsoft/MiniLM-L12-H384-uncased")


def _prepare_sentence_tokens(sentence: str):
    return torch.tensor([tokenizer.encode(sentence)])


class MiniLMSequenceClassification(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "microsoft/MiniLM-L12-H384-uncased",  # The pretrained model.
            num_labels=2,  # The number of output labels--2 for binary classification.
            output_attentions=False,  # Whether the model returns attentions weights.
            output_hidden_states=False,  # Whether the model returns all hidden-states.
            torchscript=True,
        )

    def forward(self, tokens):
        return self.model.forward(tokens)[0]


test_input = _prepare_sentence_tokens("this project is very interesting")

shark_module = SharkInference(
    MiniLMSequenceClassification(), (test_input,), device="cpu", jit_trace=True
)
results = shark_module.forward((test_input,))
