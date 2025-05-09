import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
import os
import tempfile

# Initialize Ollama
llm = Ollama(model="mistral")
embeddings = OllamaEmbeddings(model="mistral")

# Initialize ChromaDB
persist_directory = "chroma_db"
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

# Load Kazakhstan Constitution by default
def load_constitution():
    constitution_url = "https://www.akorda.kz/en/constitution-of-the-republic-of-kazakhstan-50912"
    loader = WebBaseLoader(constitution_url)
    documents = loader.load()
    return documents

# Process documents
def process_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(docs)
    return texts

# Initialize or get existing vector store
def get_vector_store(texts):
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

# Main app
def main():
    st.title("AI Assistant for Kazakhstan Constitution")
    
    # Initialize session state
    if "vector_store" not in st.session_state:
        # Load constitution first
        constitution_docs = load_constitution()
        processed_docs = process_documents(constitution_docs)
        st.session_state.vector_store = get_vector_store(processed_docs)
        st.session_state.docs_loaded = True
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload additional documents (PDF)", 
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process Uploaded Files"):
        with st.spinner("Processing files..."):
            temp_dir = tempfile.mkdtemp()
            for uploaded_file in uploaded_files:
                temp_filepath = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                loader = PyPDFLoader(temp_filepath)
                documents = loader.load()
                processed_docs = process_documents(documents)
                
                # Add to existing vector store
                st.session_state.vector_store.add_documents(processed_docs)
                st.session_state.vector_store.persist()
            
            st.success("Files processed successfully!")
    
    # Question answering
    st.subheader("Ask a question about the Constitution or uploaded documents")
    question = st.text_input("Your question:")
    
    if question and st.session_state.docs_loaded:
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=st.session_state.vector_store.as_retriever(),
            return_source_documents=True
        )
        
        result = qa({"query": question})
        st.write("**Answer:**")
        st.write(result["result"])
        
        with st.expander("See source documents"):
            for doc in result["source_documents"]:
                st.write(doc.metadata["source"])
                st.write(doc.page_content)
                st.write("---")

if __name__ == "__main__":
    main()