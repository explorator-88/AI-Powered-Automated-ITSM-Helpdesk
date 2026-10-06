
import re

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)


MODEL_NAME = "google/flan-t5-small"


FALLBACK = (
    "The knowledge base does not contain enough information to answer "
    "this request. Please contact the IT helpdesk."
)


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
            "do",
            "does",
            "doesnt",
            "not",
            "please",
            "tell",
        }

        return {
            word
            for word in words
            if word not in stop_words
            and len(word) > 2
        }

    def _is_overview_sentence(
        self,
        sentence: str
    ) -> bool:

        text = sentence.lower().strip()

        overview_patterns = [
            "this article provides",
            "this article covers",
            "this article describes",
            "this guide provides",
            "this guide covers",
            "common microsoft teams problems",
            "common teams problems",
            "microsoft teams is used",
            "problems, including",
            "issues, including",
            "including:",
        ]

        return any(
            pattern in text
            for pattern in overview_patterns
        )

    def _is_heading_or_metadata(
        self,
        sentence: str
    ) -> bool:

        text = sentence.lower().strip()

        metadata_patterns = [
            "article id:",
            "title:",
            "category:",
            "subcategory:",
            "assignment group:",
            "priority:",
            "source type:",
            "last reviewed:",
            "symptoms",
            "troubleshooting",
            "escalation",
            "important",
        ]

        return (
            len(sentence) < 35
            or any(
                text.startswith(pattern)
                for pattern in metadata_patterns
            )
        )

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

            raw_sentences = re.split(
                r"(?<=[.!?])\s+|\n+",
                text
            )

            for sentence in raw_sentences:

                sentence = sentence.strip()

                if len(sentence) < 20:
                    continue

                if self._is_heading_or_metadata(sentence):
                    continue

                if self._is_overview_sentence(sentence):
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

                # Give a small preference to sentences
                # that contain actual troubleshooting language.
                troubleshooting_bonus = 0.0

                troubleshooting_terms = {
                    "close",
                    "restart",
                    "verify",
                    "confirm",
                    "check",
                    "attempt",
                    "contact",
                    "escalate",
                    "account",
                    "authenticate",
                    "authentication",
                    "credentials",
                    "sign",
                    "login",
                    "password",
                }

                if sentence_terms.intersection(
                    troubleshooting_terms
                ):
                    troubleshooting_bonus = 0.20

                final_score = (
                    lexical_score * 0.55
                    + document["score"] * 0.25
                    + troubleshooting_bonus
                )

                candidates.append(
                    {
                        "sentence": sentence,
                        "lexical_score": lexical_score,
                        "retrieval_score": document["score"],
                        "final_score": final_score,
                        "source_file": document["source_file"],
                    }
                )

        candidates.sort(
            key=lambda item: item["final_score"],
            reverse=True,
        )

        selected = []
        seen = set()

        for candidate in candidates:

            normalized = re.sub(
                r"\s+",
                " ",
                candidate["sentence"].lower()
            ).strip()

            if normalized in seen:
                continue

            seen.add(normalized)
            selected.append(candidate)

            if len(selected) >= max_sentences:
                break

        return selected

    def _build_extractive_answer(
        self,
        relevant_sentences: list[dict]
    ) -> str:

        if not relevant_sentences:
            return FALLBACK

        # Prefer sentences that actually describe an action.
        action_terms = {
            "close",
            "restart",
            "verify",
            "confirm",
            "check",
            "attempt",
            "contact",
            "escalate",
            "retry",
        }

        action_sentences = []

        for item in relevant_sentences:

            terms = self._tokenize_for_matching(
                item["sentence"]
            )

            if terms.intersection(action_terms):
                action_sentences.append(
                    item["sentence"]
                )

        # If action-oriented sentences exist,
        # use them instead of generic descriptive sentences.
        if action_sentences:

            unique = []
            seen = set()

            for sentence in action_sentences:

                normalized = sentence.lower().strip()

                if normalized in seen:
                    continue

                seen.add(normalized)
                unique.append(sentence)

            action_sentences = unique[:6]

            return " ".join(
                f"{index}. {sentence}"
                for index, sentence
                in enumerate(action_sentences, start=1)
            )

        return " ".join(
            item["sentence"]
            for item in relevant_sentences[:5]
        )

    def _is_bad_generated_answer(
        self,
        answer: str,
        question: str
    ) -> bool:

        if not answer:
            return True

        normalized = answer.lower().strip()

        bad_patterns = [
            "list of common microsoft teams problems",
            "list of common teams problems",
            "use only troubleshooting steps",
            "answer the question using only",
            "the knowledge base does not contain enough",
            "context:",
            "question:",
            "approved knowledge:",
        ]

        if any(
            pattern in normalized
            for pattern in bad_patterns
        ):
            return True

        words = normalized.split()

        if len(words) < 8:
            return True

        return False

    def generate(
        self,
        question: str,
        retrieved_documents: list[dict]
    ) -> str:

        if not retrieved_documents:
            return FALLBACK

        relevant_sentences = (
            self._extract_relevant_sentences(
                question,
                retrieved_documents,
                max_sentences=10,
            )
        )

        if not relevant_sentences:
            return FALLBACK

        context_lines = []

        for index, item in enumerate(
            relevant_sentences,
            start=1
        ):
            context_lines.append(
                f"{index}. {item['sentence']}"
            )

        context = "\n".join(context_lines)

        print(
            "\n===== RAG CONTEXT SENT TO FLAN-T5 ====="
        )
        print(context)
        print(
            "========================================\n"
        )

        prompt = f"""
question: {question}

context:
{context}

Using the context, provide the answer to the question.
Give only the relevant troubleshooting steps.
Do not repeat the context.
Do not describe the article.
Do not list unrelated problems.
If the context contains troubleshooting steps, use those steps directly.

answer:
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

        # If FLAN-T5 produces an instruction,
        # article description, or another poor answer,
        # use the retrieved approved troubleshooting content.
        if self._is_bad_generated_answer(
            answer,
            question
        ):
            print(
                "FLAN-T5 produced a non-actionable answer. "
                "Using grounded extractive answer."
            )

            return self._build_extractive_answer(
                relevant_sentences
            )

        return self._clean_answer(answer)

    def _clean_answer(
        self,
        answer: str
    ) -> str:

        if not answer:
            return FALLBACK

        answer = re.sub(
            r"\s+",
            " ",
            answer
        ).strip()

        words = answer.split()

        if len(words) < 6:
            return FALLBACK

        return answer