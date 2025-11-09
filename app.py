import streamlit as st
import chains
from vectordb_config import store_pdf_in_vectordb


def pdf_analyzer_app():
    """
    PDF Analyzer Application with Streamlit, providing PDF upload, summarization, and Q&A features.
    """
    # Page configuration
    st.set_page_config(
        page_title="PDF Analyzer",
        page_icon="📄",
        layout="wide"
    )

    # Sidebar navigation
    st.sidebar.title('📄 PDF Analyzer')
    st.sidebar.markdown("---")
    
    section = st.sidebar.radio(
        "Choose a feature:",
        ("Upload PDF", "PDF Summarizer", "Ask Questions")
    )

    # Initialize session state for tracking uploaded files
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    # Main content area
    if section == "Upload PDF":
        st.title("📤 Upload PDF Document")
        st.markdown("Upload a PDF file to analyze it using AI-powered summarization and Q&A features.")
        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF file to get started with analysis"
        )

        if uploaded_file is not None:
            st.info(f"📄 Selected file: **{uploaded_file.name}**")
            
            with st.spinner("Processing and indexing PDF... This may take a moment."):
                success, message, num_chunks = store_pdf_in_vectordb(uploaded_file)
                
                if success:
                    st.success(f"✅ {message}")
                    st.info(f"📊 Document split into **{num_chunks}** chunks for analysis.")
                    
                    # Track uploaded file in session state
                    if uploaded_file.name not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(uploaded_file.name)
                else:
                    st.error(f"❌ {message}")

        # Display uploaded files history
        if st.session_state.uploaded_files:
            st.markdown("---")
            st.subheader("📚 Uploaded Files")
            for file_name in st.session_state.uploaded_files:
                st.write(f"• {file_name}")

    elif section == "PDF Summarizer":
        st.title("📝 PDF Summarizer")
        st.markdown("Generate a comprehensive summary of your uploaded PDF document using AI.")
        st.markdown("---")

        if st.button("Generate Summary", type="primary", use_container_width=True):
            with st.spinner("Generating summary... This may take a few moments."):
                summary = chains.generate_pdf_summary_chain()
                
                if summary:
                    st.subheader("📄 Document Summary")
                    st.markdown("---")
                    st.write(summary)
                else:
                    st.warning("⚠️ Could not generate summary. Please ensure a PDF has been uploaded first.")

    elif section == "Ask Questions":
        st.title("❓ Ask Questions About Your PDF")
        st.markdown("Ask any question about the content of your uploaded PDF document.")
        st.markdown("---")

        with st.form("qa_form"):
            question = st.text_input(
                "Enter your question:",
                placeholder="e.g., What are the main topics discussed in this document?",
                help="Ask any question about the PDF content"
            )
            submitted = st.form_submit_button("Get Answer", type="primary", use_container_width=True)

            if submitted:
                if question.strip():
                    with st.spinner("Searching through the document and generating answer..."):
                        answer = chains.generate_pdf_qa_chain(question)
                        
                        if answer:
                            st.subheader("💡 Answer")
                            st.markdown("---")
                            st.write(answer)
                        else:
                            st.warning("⚠️ Could not generate an answer. Please ensure a PDF has been uploaded first.")
                else:
                    st.warning("⚠️ Please enter a question.")


if __name__ == "__main__":
    pdf_analyzer_app()
