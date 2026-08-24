import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class EduMorphModel:
    MODEL_NAME = "google/flan-t5-small"

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading EduMorph model on: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.MODEL_NAME
        ).to(self.device)

        self.model.eval()

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 150
    ) -> str:

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=384
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                num_beams=4
            )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()