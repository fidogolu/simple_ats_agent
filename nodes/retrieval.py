# nodes/retrieval.py
"""RAG retrieval node.

Handles document chunking, embedding, and semantic similarity search
using ChromaDB and HuggingFace embeddings.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from models.schemas import PipelineState
from utils import LOGGER

_embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def retrieval_node(state: PipelineState) -> PipelineState:
    """
    Retrieval node: Retrieves relevant document chunks based on context query.
    """
    LOGGER.info("Retrieval node: Performing RAG...")

    document_text = state.get("document_content", "")
    query = state.get("context_text", "")

    if document_text == "__EMPTY_SCAN__":
        LOGGER.error("Document seems to be an image. Analysis impossible without OCR.")
        return {"rag_result": "Error: Document seems to be an image (no OCR available)"}

    if not document_text or not query:
        LOGGER.warning("Content missing for analysis.")
        return {"rag_result": "Error: Missing content for analysis"}

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = splitter.split_text(document_text) or [document_text]

        vectorstore = Chroma.from_texts(texts=chunks, embedding=_embed_model)
        relevant_docs = vectorstore.similarity_search(query, k=4)

        return {
            "rag_result": {
                "relevant_docs": relevant_docs,
                "query": query,
            }
        }

    except Exception as e:
        LOGGER.error(f"Error during retrieval: {str(e)}")
        return {"rag_result": f"Error: {str(e)}"}
