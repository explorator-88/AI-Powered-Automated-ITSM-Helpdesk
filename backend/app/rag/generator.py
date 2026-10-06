
import re

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
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model.to(self.device)

        print(
            f"LLM loaded successfully on "
            f"{self.device}."
        )

    def _tokenize_for_matching(
        self,
        text: str
    ) -> set[str]:

        words = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower()
        )

        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "to",
            "for",
            "of",
            "and",
            "or",
            "in",
            "on",
            "with",
            "how",
            "what",
            "why",
            "can",
            "i",
            "my",
            "me",
            "it",
            "this",
            "that",
        }

        return {
            word
            for word in words
            if word not in stop_words
            and len(word) > 2
        }

    def _extract_relevant_sentences(
        self,
        question: str,
        retrieved_documents: list[dict],
        max_sentences: int = 10,
    ) -> list[dict]:

        question_terms = self._tokenize_for_matching(
            question
        )

        candidates = []

        for document in retrieved_documents:

            text = document["text"]

            # Split both PDF lines and normal sentences.
            raw_sentences = re.split(
                r"(?<=[.!?])\s+|\n+",
                text
            )

            for sentence in raw_sentences:

                sentence = sentence.strip()

                if len(sentence) < 20:
                    continue

                sentence_terms = (
                    self._tokenize_for_matching(
                        sentence
                    )
                )

                overlap = question_terms.intersection(
                    sentence_terms
                )

                lexical_score = (
                    len(overlap)
                    / max(len(question_terms), 1)
                )

                candidates.append(
                    {
                        "sentence": sentence,
                        "lexical_score": lexical_score,
                        "retrieval_score": document["score"],
                        "source_file": document["source_file"],
                    }
                )

        # Rank sentences using both semantic retrieval
        # and question-term overlap.
        candidates.sort(
            key=lambda item: (
                item["lexical_score"] * 0.65
                + item["retrieval_score"] * 0.35
            ),
            reverse=True,
        )

        selected = []

        seen = set()

        for candidate in candidates:

            normalized = candidate["sentence"].lower()

            if normalized in seen:
                continue

            seen.add(normalized)

            selected.append(candidate)

            if len(selected) >= max_sentences:
                break

        return selected

    def generate(
        self,
        question: str,
        retrieved_documents: list[dict]
    ) -> str:

        if not retrieved_documents:

            return (
                "I could not find an approved knowledge-base "
                "article relevant to your request. "
                "Please contact the IT helpdesk."
            )

        relevant_sentences = (
            self._extract_relevant_sentences(
                question,
                retrieved_documents,
                max_sentences=10,
            )
        )

        if not relevant_sentences:

            return (
                "The knowledge base does not contain enough "
                "information to answer this request. "
                "Please contact the IT helpdesk."
            )

        context_lines = []

        for index, item in enumerate(
            relevant_sentences,
            start=1
        ):

            context_lines.append(
                f"{index}. {item['sentence']}"
            )

        context = "\n".join(context_lines)

        prompt = f"""
You are an enterprise IT helpdesk assistant.

Answer the employee's question using ONLY the approved
knowledge statements provided below.

Employee question:
{question}

Approved knowledge:
{context}

Strict rules:
- Do not invent troubleshooting steps.
- Do not use outside knowledge.
- Do not copy article titles or headings as the answer.
- Do not mention unrelated symptoms.
- Use only information that helps answer the employee's question.
- Give a short, practical answer.
- If multiple troubleshooting steps are provided, present them
  as a numbered list.
- If the knowledge does not answer the question, say:
  "The knowledge base does not contain enough information to
  answer this request. Please contact the IT helpdesk."

Answer:
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
                max_new_tokens=160,
                do_sample=False,
                num_beams=4,
                early_stopping=True,
            )

        answer = self.tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        ).strip()

        return self._clean_answer(answer)

    def _clean_answer(
        self,
        answer: str
    ) -> str:

        if not answer:
            return (
                "The knowledge base does not contain enough "
                "information to answer this request. "
                "Please contact the IT helpdesk."
            )

        # Remove accidental duplicated whitespace.
        answer = re.sub(
            r"\s+",
            " ",
            answer
        ).strip()

        # Guard against the exact failure pattern
        # seen in the current application.
        words = answer.split()

        if len(words) < 6:
            return (
                "The knowledge base does not contain enough "
                "information to answer this request. "
                "Please contact the IT helpdesk."
            )

        return answer