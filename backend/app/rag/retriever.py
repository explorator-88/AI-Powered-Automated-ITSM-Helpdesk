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

        self.index = faiss.read_index(
            str(INDEX_FILE)
        )

        print("Loading document metadata...")

        self.documents = json.loads(
            METADATA_FILE.read_text(
                encoding="utf-8"
            )
        )

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.index_modified_time = INDEX_FILE.stat().st_mtime

        print(
            f"Retriever ready. Indexed documents: "
            f"{self.index.ntotal}"
        )

    def reload_if_needed(self):

        current_modified_time = INDEX_FILE.stat().st_mtime

        if current_modified_time <= self.index_modified_time:
            return

        print(
            "Knowledge index changed. Reloading FAISS index..."
        )

        self.index = faiss.read_index(
            str(INDEX_FILE)
        )

        self.documents = json.loads(
            METADATA_FILE.read_text(
                encoding="utf-8"
            )
        )

        self.index_modified_time = current_modified_time

        print(
            f"Retriever reloaded. Indexed documents: "
            f"{self.index.ntotal}"
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict]:

        if not query.strip():
            return []

        self.reload_if_needed()

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        search_count = min(
            top_k,
            self.index.ntotal
        )

        scores, indices = self.index.search(
            query_embedding,
            search_count
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

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