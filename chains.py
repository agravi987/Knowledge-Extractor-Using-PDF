from langchain_core.output_parsers import StrOutputParser

import models
import prompts
from vectordb_config import initialize_vectordb


def generate_pdf_summary_chain(collection_name="pdf_docs", max_chunks=20):
    """
    Generate a comprehensive summary of the PDF document using LLM.

    Args:
        collection_name (str): Name of the collection containing PDF documents (default: "pdf_docs")
        max_chunks (int): Maximum number of document chunks to retrieve for summarization (default: 20)

    Returns:
        str: Generated summary of the PDF document
    """
    try:
        # Initialize vector database
        db = initialize_vectordb(collection_name=collection_name)

        # Get all documents or top chunks for summarization
        retriever = db.as_retriever(search_kwargs={"k": max_chunks})
        retriever_results = retriever.invoke("summary main topics key points")

        if not retriever_results:
            return "No documents found in the database. Please upload a PDF file first."

        # Combine all retrieved chunks into context
        context = "\n\n".join(doc.page_content for doc in retriever_results)

        # Initialize LLM
        llm = models.create_chat_groq_model()

        # Create summarization chain
        summary_chain = prompts.pdf_summarizer_prompt() | llm | StrOutputParser()

        # Generate summary
        response = summary_chain.invoke({
            "context": context
        })

        return response

    except Exception as e:
        return f"Error generating summary: {str(e)}. Please ensure a PDF has been uploaded and indexed."


def generate_pdf_qa_chain(question, collection_name="pdf_docs", k=5):
    """
    Generate answer to user's question based on PDF document content using RAG.

    Args:
        question (str): User's question about the PDF content
        collection_name (str): Name of the collection containing PDF documents (default: "pdf_docs")
        k (int): Number of document chunks to retrieve (default: 5)

    Returns:
        str: Answer to the user's question based on PDF content
    """
    try:
        # Initialize vector database
        db = initialize_vectordb(collection_name=collection_name)

        # Create retriever with specified number of chunks
        retriever = db.as_retriever(search_kwargs={"k": k})

        # Retrieve relevant document chunks based on the question
        retriever_results = retriever.invoke(question)

        if not retriever_results:
            return "No relevant documents found. Please ensure a PDF has been uploaded and indexed, and try rephrasing your question."

        # Combine retrieved chunks into context
        context = "\n\n".join(doc.page_content for doc in retriever_results)

        # Initialize LLM
        llm = models.create_chat_groq_model()

        # Create Q&A chain
        qa_chain = prompts.pdf_qa_prompt() | llm | StrOutputParser()

        # Generate answer
        response = qa_chain.invoke({
            "question": question,
            "context": context
        })

        return response

    except Exception as e:
        return f"Error answering question: {str(e)}. Please ensure a PDF has been uploaded and indexed."