from typing import List, Any
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os


def load_jd(jd_path: str) -> str:
    """
    Loads the job description text from a file.
    """
    loader = TextLoader(jd_path)
    documents = loader.load()
    return documents[0].page_content


def split_jd(jd_text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[Any]:
    """
    Splits the job description text into chunks for embedding.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    # Wrap in a Document object for compatibility
    from langchain.schema import Document
    doc = Document(page_content=jd_text)
    return text_splitter.split_documents([doc])


def embed_and_save_chunks(split_docs: List[Any], config: dict) -> None:
    """
    Embeds the split job description chunks and saves them to ChromaDB.
    """
    # Ensure the API key is set in the environment
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    os.makedirs(config['CHROMA_DB_PATH'], exist_ok=True)
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=config['CHROMA_DB_PATH']
    ) 