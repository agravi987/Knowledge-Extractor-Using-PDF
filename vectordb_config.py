import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import models


def initialize_vectordb(collection_name="pdf_docs"):
    """
    Initialize and return a Chroma vector database instance.

    Args:
        collection_name (str): Name of the collection to use (default: "pdf_docs")

    Returns:
        Chroma: Initialized vector database instance
    """
    hugging_face_embeddings = models.create_hugging_face_embedding_model()

    vector_db = Chroma(
        embedding_function=hugging_face_embeddings,
        collection_name=collection_name,
        persist_directory="./chroma_db"
    )

    return vector_db


def store_pdf_in_vectordb(uploaded_file, collection_name="pdf_docs"):
    """
    Store uploaded PDF file in the vector database.

    Args:
        uploaded_file: Streamlit uploaded file object
        collection_name (str): Name of the collection to store documents in (default: "pdf_docs")

    Returns:
        tuple: (success: bool, message: str, num_chunks: int)
    """
    try:
        # Create data_source directory if it doesn't exist
        os.makedirs("data_source", exist_ok=True)

        vectordb = initialize_vectordb(collection_name)

        file_path = f"data_source/temp_{uploaded_file.name}"

        # Save uploaded file temporarily
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load PDF documents
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # Add documents to vector database
        vectordb.add_documents(splits)

        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

        return True, f"File '{uploaded_file.name}' uploaded and indexed successfully!", len(splits)

    except Exception as e:
        # Clean up temporary file in case of error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return False, f"Error processing file: {str(e)}", 0


def get_all_documents(collection_name="pdf_docs"):
    """
    Retrieve all documents from the vector database.

    Args:
        collection_name (str): Name of the collection (default: "pdf_docs")

    Returns:
        list: List of document chunks
    """
    try:
        vectordb = initialize_vectordb(collection_name)
        # Get all documents from the collection
        results = vectordb.get()
        return results.get('documents', [])
    except Exception as e:
        return []
