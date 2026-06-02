from pathlib import Path
import uuid

from utils.file_loader import FileLoader
from utils.chunking import create_chunks

from rag.vectorstore import VectorStore

from logger import app_logger


RAW_DATA_PATH = Path("data/raw")


def ingest_documents():

    vectorstore = VectorStore()

    files = list(RAW_DATA_PATH.glob("*"))

    if not files:
        app_logger.warning(
            "No files found in data/raw"
        )
        return

    documents = []
    metadatas = []
    ids = []

    for file_path in files:

        app_logger.info(
            f"Processing {file_path.name}"
        )

        text = FileLoader.load_document(
            str(file_path)
        )

        chunks = create_chunks(text)

        for idx, chunk in enumerate(chunks):

            documents.append(chunk)

            metadatas.append(
                {
                    "source": file_path.name,
                    "chunk": idx
                }
            )

            ids.append(str(uuid.uuid4()))

    vectorstore.add_documents(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    app_logger.success(
        f"Ingested {len(documents)} chunks"
    )

    app_logger.success(
        f"Total vectors: {vectorstore.count()}"
    )