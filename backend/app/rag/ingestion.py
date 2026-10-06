from pathlib import Path
from typing import Any

import yaml
from pypdf import PdfReader


KNOWLEDGE_BASE_DIR = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "knowledge_base"
)


def parse_markdown_article(file_path: Path) -> dict[str, Any]:
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


def parse_pdf_article(file_path: Path) -> dict[str, Any]:
    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages.append(text.strip())

    article_text = "\n\n".join(pages).strip()

    if not article_text:
        raise ValueError(
            f"No extractable text found in {file_path.name}"
        )

    article_id = file_path.stem.upper()

    metadata = {
        "article_id": article_id,
        "title": file_path.stem.replace("_", " ").replace("-", " ").title(),
        "category": "General IT",
        "subcategory": "Knowledge Article",
        "assignment_group": "IT Helpdesk",
        "priority": "P3",
        "source_type": "uploaded_pdf",
    }

    return {
        "metadata": metadata,
        "text": article_text,
        "source_file": file_path.name,
    }


def chunk_text(
    text: str,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> list[str]:
    """
    Split knowledge articles into focused word-based chunks.

    Smaller chunks improve semantic retrieval because each vector
    represents a more focused troubleshooting section.
    """

    words = text.split()

    if not words:
        return []

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - chunk_overlap

    return chunks


def load_knowledge_base() -> list[dict[str, Any]]:

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}"
        )

    articles = []

    # Markdown knowledge articles
    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):

        article = parse_markdown_article(file_path)

        chunks = chunk_text(article["text"])

        for index, chunk in enumerate(chunks):

            articles.append(
                {
                    "chunk_id": (
                        f"{article['metadata']['article_id']}"
                        f"_chunk_{index}"
                    ),
                    "text": chunk,
                    "metadata": article["metadata"],
                    "source_file": article["source_file"],
                }
            )

    # Uploaded PDF knowledge articles
    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.pdf")):

        article = parse_pdf_article(file_path)

        chunks = chunk_text(article["text"])

        for index, chunk in enumerate(chunks):

            articles.append(
                {
                    "chunk_id": (
                        f"{article['metadata']['article_id']}"
                        f"_chunk_{index}"
                    ),
                    "text": chunk,
                    "metadata": article["metadata"],
                    "source_file": article["source_file"],
                }
            )

    return articles


if __name__ == "__main__":

    documents = load_knowledge_base()

    print("Knowledge base loaded successfully.")
    print(f"Total chunks: {len(documents)}")

    for document in documents:

        print(
            f"{document['chunk_id']} | "
            f"{document['metadata']['title']} | "
            f"{document['source_file']}"
        )