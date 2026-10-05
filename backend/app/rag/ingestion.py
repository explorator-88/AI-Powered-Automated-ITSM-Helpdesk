
from pathlib import Path
from typing import Any

import yaml


KNOWLEDGE_BASE_DIR = (
    Path(__file__).resolve().parents[3] / "data" / "knowledge_base"
)


def parse_markdown_article(file_path: Path) -> dict[str, Any]:
    """
    Read a Markdown knowledge article containing YAML front matter.

    Expected structure:

    ---
    article_id: KB001
    title: VPN Authentication Failure
    ...
    ---

    # VPN Authentication Failure

    Article content...
    """

    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        raise ValueError(
            f"{file_path.name} does not contain YAML front matter."
        )

    parts = content.split("---", 2)

    if len(parts) != 3:
        raise ValueError(
            f"Invalid YAML front matter in {file_path.name}"
        )

    metadata_text = parts[1]
    article_text = parts[2].strip()

    metadata = yaml.safe_load(metadata_text) or {}

    return {
        "metadata": metadata,
        "text": article_text,
        "source_file": file_path.name,
    }


def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> list[str]:
    """
    Split article text into overlapping word-based chunks.

    This is intentionally simple for the prototype.
    """

    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - chunk_overlap

    return chunks


def load_knowledge_base() -> list[dict[str, Any]]:
    """
    Load every Markdown knowledge article and create chunks.
    """

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}"
        )

    articles = []

    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        article = parse_markdown_article(file_path)

        chunks = chunk_text(article["text"])

        for index, chunk in enumerate(chunks):
            articles.append(
                {
                    "chunk_id": (
                        f"{article['metadata']['article_id']}_chunk_{index}"
                    ),
                    "text": chunk,
                    "metadata": article["metadata"],
                    "source_file": article["source_file"],
                }
            )

    return articles


if __name__ == "__main__":
    documents = load_knowledge_base()

    print(f"Knowledge base loaded successfully.")
    print(f"Total chunks: {len(documents)}")

    for document in documents:
        print(
            f"{document['chunk_id']} | "
            f"{document['metadata']['title']}"
        )

