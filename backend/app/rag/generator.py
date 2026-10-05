
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)


MODEL_NAME = "google/flan-t5-small"


class RAGGenerator:

    def __init__(self):

        print(f"Loading LLM: {MODEL_NAME}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_NAME
        )

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model.to(self.device)

        print(
            f"LLM loaded successfully on {self.device}."
        )

    def generate(
        self,
        question: str,
        retrieved_documents: list[dict],
    ) -> str:

        if not retrieved_documents:
            return (
                "I could not find an approved knowledge-base "
                "article relevant to your request. "
                "Please contact the IT helpdesk."
            )

        context_parts = []

        for document in retrieved_documents:

            metadata = document["metadata"]

            context_parts.append(
                f"""
Article ID: {metadata.get("article_id")}
Title: {metadata.get("title")}
Category: {metadata.get("category")}
Subcategory: {metadata.get("subcategory")}

Approved Knowledge:
{document["text"]}
"""
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an enterprise IT helpdesk assistant.

Answer the employee question using ONLY the approved
knowledge provided below.

Do not invent troubleshooting steps.

If the knowledge does not contain enough information,
say that the information is unavailable and recommend
contacting the IT helpdesk.

Employee question:
{question}

Approved knowledge:
{context}

Give a concise, practical answer.
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            output = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False,
            )

        answer = self.tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        )

        return answer.strip()
