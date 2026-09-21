import shutil

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import ROOT_DIR
from app.rag.embeddings import get_embeddings


DATA_PATH = ROOT_DIR / "data" / "knowledge"

CHROMA_PATH = ROOT_DIR / "data" / "chroma"


def build_index():

    documents = []

    for file in DATA_PATH.glob("*.txt"):

        text = file.read_text(
            encoding="utf-8"
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file.name
                }
            )
        )


    print(
        "Documents loaded:",
        len(documents)
    )


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )


    chunks = splitter.split_documents(
        documents
    )


    print(
        "Chunks created:",
        len(chunks)
    )


    for chunk in chunks:
        print(
            chunk.page_content[:100]
        )


    if CHROMA_PATH.exists():

        shutil.rmtree(
            CHROMA_PATH
        )


    CHROMA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )


    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(
            CHROMA_PATH
        )
    )


    return len(chunks)