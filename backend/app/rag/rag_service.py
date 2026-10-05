
from app.rag.retriever import KnowledgeRetriever
from app.rag.generator import RAGGenerator


class RAGService:

    def __init__(self):
        self.retriever = KnowledgeRetriever()
        self.generator = RAGGenerator()

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> dict:

        results = self.retriever.search(
            question,
            top_k=top_k,
        )

        # Minimum relevance threshold.
        # This prevents unrelated KB articles from
        # being treated as valid grounding.
        relevant_results = [
            result
            for result in results
            if result["score"] >= 0.30
        ]

        if not relevant_results:
            return {
                "answer": (
                    "I could not find an approved knowledge-base "
                    "article relevant to your request. "
                    "Please contact the IT helpdesk."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        answer = self.generator.generate(
            question,
            relevant_results,
        )

        sources = []

        for result in relevant_results:

            metadata = result["metadata"]

            sources.append(
                {
                    "article_id": metadata.get("article_id"),
                    "title": metadata.get("title"),
                    "category": metadata.get("category"),
                    "source_file": result["source_file"],
                    "similarity_score": round(
                        result["score"],
                        4,
                    ),
                }
            )

        confidence = relevant_results[0]["score"]

        return {
            "answer": answer,
            "sources": sources,
            "confidence": round(confidence, 4),
        }

