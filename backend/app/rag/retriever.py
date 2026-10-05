from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]

INDEX_FILE = PROJECT_ROOT / "faiss_index" / "knowledge.index"
METADATA_FILE = PROJECT_ROOT / "faiss_index" / "metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class KnowledgeRetriever:

    def __init__(self):

        if not INDEX_FILE.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {INDEX_FILE}"
            )

        if not METADATA_FILE.exists():
            raise FileNotFoundError(
                f"Metadata file not found: {METADATA_FILE}"
            )

        print("Loading FAISS index...")
        self.index = faiss.read_index(str(INDEX_FILE))

        print("Loading document metadata...")
        self.documents = json.loads(
            METADATA_FILE.read_text(encoding="utf-8")
        )

        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

        print(
            f"Retriever ready. Indexed documents: "
            f"{self.index.ntotal}"
        )

    def search(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        if not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, self.index.ntotal)
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index < 0:
                continue

            document = self.documents[index]

            results.append(
                {
                    "score": float(score),
                    "chunk_id": document["chunk_id"],
                    "text": document["text"],
                    "metadata": document["metadata"],
                    "source_file": document["source_file"],
                }
            )

        return results


if __name__ == "__main__":

    retriever = KnowledgeRetriever()

    results = retriever.search(
        "My VPN authentication keeps failing",
        top_k=3
    )

    for result in results:

        metadata = result["metadata"]

        print(
            f"\nScore: {result['score']:.4f}"
        )

        print(
            f"Article: "
            f"{metadata.get('article_id')} - "
            f"{metadata.get('title')}"
        )

        print(
            f"Category: "
            f"{metadata.get('category')} / "
            f"{metadata.get('subcategory')}"
        )

        print(
            f"Source: {result['source_file']}"
        )