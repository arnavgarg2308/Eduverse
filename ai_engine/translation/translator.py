import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class RegionalTranslator:
    """
    English -> Indian/regional language translation.

    NLLB is used as the practical local fallback for the
    current demo because IndicTrans2 access is blocked.
    """

    MODEL_NAME = "facebook/nllb-200-distilled-600M"

    LANGUAGE_CODES = {
        "hindi": "hin_Deva",
        "bengali": "ben_Beng",
        "punjabi": "pan_Guru",
        "marathi": "mar_Deva",
        "gujarati": "guj_Gujr",
        "tamil": "tam_Taml",
        "telugu": "tel_Telu",
        "kannada": "kan_Knda",
        "malayalam": "mal_Mlym",
        "odia": "ory_Orya",
        "assamese": "asm_Beng",
    }

    def __init__(self):
        # Keep translation on CPU so FLAN-T5 can use the RTX 2050.
        self.device = "cpu"

        print("Loading regional translation model on CPU...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.MODEL_NAME
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        print("Regional translation model ready.")

    def translate(
        self,
        text: str,
        target_language: str = "hindi"
    ) -> str:

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        target_language = target_language.lower().strip()

        if target_language not in self.LANGUAGE_CODES:
            supported = ", ".join(
                self.LANGUAGE_CODES.keys()
            )

            raise ValueError(
                f"Unsupported language: {target_language}. "
                f"Supported languages: {supported}"
            )

        target_code = self.LANGUAGE_CODES[
            target_language
        ]

        self.tokenizer.src_lang = "eng_Latn"

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=384
        ).to(self.device)

        forced_bos_token_id = (
            self.tokenizer.convert_tokens_to_ids(
                target_code
            )
        )

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=180,
                num_beams=4
            )

        return self.tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )[0].strip()