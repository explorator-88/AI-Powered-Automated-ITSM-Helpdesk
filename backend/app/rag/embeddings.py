
from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer

from app.rag.ingestion import load_knowledge_base


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Where the vector index and metadata will be stored
INDEX_DIR = PROJECT_ROOT / "faiss_index"
INDEX_FILE = INDEX_DIR / "knowledge.index"
METADATA_FILE = INDEX_DIR / "metadata.json"

# Open-source embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_index():
    print("Loading knowledge base...")

    documents = load_knowledge_base()

    if not documents:
        raise ValueError("No knowledge-base documents found.")

    print(f"Documents loaded: {len(documents)}")

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    texts = [document["text"] for document in documents]

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    print(f"Embedding shape: {embeddings.shape}")

    # Inner Product + normalized embeddings ≈ cosine similarity
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    INDEX_DIR.mkdir(exist_ok=True)

    faiss.write_index(index, str(INDEX_FILE))

    # Save the metadata separately because FAISS only stores vectors
    metadata = []

    for document in documents:
        metadata.append(
            {
                "chunk_id": document["chunk_id"],
                "text": document["text"],
                "metadata": document["metadata"],
                "source_file": document["source_file"],
            }
        )

    METADATA_FILE.write_text(
        json.dumps(metadata, indent=2, default=str),
        encoding="utf-8",
    )

    print()
    print("FAISS index created successfully.")
    print(f"Vectors: {index.ntotal}")
    print(f"Dimension: {dimension}")
    print(f"Index: {INDEX_FILE}")
    print(f"Metadata: {METADATA_FILE}")


if __name__ == "__main__":
    build_index()

