from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    UploadFile,
    HTTPException
)

from app.rag.embeddings import build_index
from app.rag.ingestion import (
    KNOWLEDGE_BASE_DIR,
    load_knowledge_base,
)


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Management"],
)


@router.post("/upload")
async def upload_knowledge_document(
    file: UploadFile = File(...)
):

    """
    Upload a Markdown or PDF knowledge document
    and rebuild the FAISS knowledge index.
    """

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )


    filename = Path(
        file.filename
    ).name

    extension = Path(
        filename
    ).suffix.lower()


    if extension not in {
        ".md",
        ".pdf"
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only Markdown (.md) and PDF (.pdf) "
                "knowledge documents are supported."
            )
        )


    KNOWLEDGE_BASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    file_path = (
        KNOWLEDGE_BASE_DIR
        / filename
    )


    if file_path.exists():

        raise HTTPException(
            status_code=409,
            detail=(
                f"A knowledge document named "
                f"'{filename}' already exists."
            )
        )


    try:

        content = await file.read()

        file_path.write_bytes(
            content
        )


        # Rebuild FAISS index
        build_index()


        # Load indexed documents
        documents = load_knowledge_base()


        uploaded_chunks = [
            document
            for document in documents
            if document["source_file"]
            == filename
        ]


        return {

            "status": "success",

            "message": (
                "Knowledge document uploaded and "
                "indexed successfully."
            ),

            "file_name": filename,

            "file_type": extension,

            "chunks_created": len(
                uploaded_chunks
            ),

            "total_chunks": len(
                documents
            ),

            "index_updated": True,
        }


    except Exception as exc:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                f"Knowledge indexing failed: "
                f"{str(exc)}"
            )
        )