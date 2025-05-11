import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.database import VectorDB
from utils.document_processing import process_text, process_pdf

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyDpqTgf3rhDZ9vzoNaZIHqUlXa0Ew7gELI"))
model = genai.GenerativeModel('gemini-1.5-pro-latest') 

# TEMPORARY: List available models (remove after checking)
print("Available Gemini models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f" - {m.name}")


# Initialize Vector Database
vector_db = VectorDB()

def generate_response(query, context):
    prompt = f"""
    You are an AI assistant specialized in the Constitution of Kazakhstan.
    Use the following context to answer the question at the end.
    If you don't know the answer, say you don't know.
    
    Context:
    {context}
    
    Question: {query}
    
    Answer:
    """
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Kazakhstan Constitution AI Assistant")
    
    # File upload section
    uploaded_files = st.file_uploader(
        "Upload documents about Kazakhstan's Constitution",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                chunks = process_pdf(file)
            else:
                text = file.read().decode("utf-8")
                chunks = process_text(text)
            
            vector_db.add_documents(chunks)
        st.success("Documents processed and stored successfully!")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask about Kazakhstan's Constitution"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get relevant context from vector DB
        results = vector_db.query(prompt)
        context = "\n".join(results["documents"][0])
        
        with st.spinner("Thinking..."):
            response = generate_response(prompt, context)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()