
from app.rag.retriever import KnowledgeRetriever
from app.rag.generator import RAGGenerator


class RAGService:

    def __init__(self):

        self.retriever = KnowledgeRetriever()
        self.generator = RAGGenerator()

    def ask(
        self,
        question: str,
        top_k: int = 5
    ) -> dict:

        if not question.strip():

            return {
                "answer": (
                    "Please enter a question so I can "
                    "search the knowledge base."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        results = self.retriever.search(
            question,
            top_k=top_k,
        )

        # Only use reasonably relevant results.
        relevant_results = [
            result
            for result in results
            if result["score"] >= 0.30
        ]

        if not relevant_results:

            return {
                "answer": (
                    "I could not find an approved "
                    "knowledge-base article relevant "
                    "to your request. Please contact "
                    "the IT helpdesk."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        # Give the generator only the strongest results.
        generator_documents = relevant_results[:3]

        answer = self.generator.generate(
            question,
            generator_documents,
        )

        # Deduplicate sources.
        source_map = {}

        for result in relevant_results:

            metadata = result["metadata"]

            source_file = result["source_file"]

            if (
                source_file not in source_map
                or result["score"]
                > source_map[source_file]["similarity_score"]
            ):

                source_map[source_file] = {
                    "article_id": metadata.get(
                        "article_id"
                    ),
                    "title": metadata.get(
                        "title"
                    ),
                    "category": metadata.get(
                        "category"
                    ),
                    "source_file": source_file,
                    "similarity_score": round(
                        result["score"],
                        4
                    ),
                }

        sources = list(
            source_map.values()
        )

        confidence = relevant_results[0]["score"]

        return {
            "answer": answer,
            "sources": sources,
            "confidence": round(
                confidence,
                4
            ),
        }