from langchain_core.prompts import ChatPromptTemplate


def pdf_summarizer_prompt():
    """
    Generates prompt template for PDF summarization using LLM.

    Returns:
        ChatPromptTemplate: Configured ChatPromptTemplate instance for PDF summarization
    """
    system_msg = '''
                You are an expert document summarization assistant. Your task is to create comprehensive, 
                well-structured summaries of PDF documents based on the provided context. Follow these guidelines:

                1. Create a clear and concise summary that captures the main points, key ideas, and important details.
                2. Organize the summary with appropriate sections if the document covers multiple topics.
                3. Maintain the logical flow and structure of the original document.
                4. Highlight important facts, figures, dates, and names mentioned in the document.
                5. Keep the summary informative but concise - aim for 3-5 paragraphs unless the document is very long.
                6. If the context is empty or insufficient, inform the user that the document could not be processed.
                7. Use clear, professional language and proper formatting.
                '''

    user_msg = '''
               Please provide a comprehensive summary of the following PDF document content.

               Document Content:
               {context}

               Generate a well-structured summary that covers the main topics, key points, and important information.
               '''

    prompt_template = ChatPromptTemplate([
        ("system", system_msg),
        ("user", user_msg)
    ])

    return prompt_template


def pdf_qa_prompt():
    """
    Generates prompt template for question-answering based on PDF documents using RAG.

    Returns:
        ChatPromptTemplate: Configured ChatPromptTemplate instance for PDF Q&A
    """
    system_msg = '''
                You are a helpful question-answering assistant specialized in answering questions 
                based on PDF document content. Your task is to provide accurate, relevant answers 
                using only the information provided in the context. Follow these guidelines:

                1. Answer questions based solely on the provided context from the PDF document.
                2. Provide clear, concise, and accurate answers.
                3. If the answer is found in the context, cite relevant information and be specific.
                4. If the question cannot be answered from the provided context, clearly state: 
                   "I cannot find the answer to this question in the uploaded PDF document. Please ensure the PDF has been uploaded and contains relevant information."
                5. If the context is empty or no documents are indexed, inform the user to upload a PDF first.
                6. Do not make up information or use knowledge outside the provided context.
                7. If multiple pieces of information are relevant, include all of them in your answer.
                8. Format your answer in a clear, readable manner with proper structure.
                '''

    user_msg = '''
               Please answer the following question based on the content from the uploaded PDF document.

               Context from PDF:
               {context}

               Question:
               {question}

               Provide a detailed answer based on the context above.
               '''

    prompt_template = ChatPromptTemplate([
        ("system", system_msg),
        ("user", user_msg)
    ])

    return prompt_template

