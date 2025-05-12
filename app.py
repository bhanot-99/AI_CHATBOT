import os
import streamlit as st
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from utils.database import VectorDB
from utils.document_processing import process_text, process_pdf
import time

# Load environment variables
load_dotenv()

# Initialize Ollama LLM
llm = Ollama(
    model="mistral",  # Good for legal text (alternatives: llama3, gemma:2b)
    temperature=0.3,  # More factual responses
    top_k=50,
    top_p=0.9,
    repeat_penalty=1.1
)

# Initialize Vector Database
vector_db = VectorDB()

def generate_response(query, context):
    """
    Improved response generation with better context handling
    """
    try:
        prompt = f"""
        [INST] <<SYS>>
        You are a constitutional law expert analyzing Kazakhstan's Constitution.
        Always:
        - Answer in clear English
        - Cite relevant articles when possible
        - Be precise with legal terminology
        - If unsure, say "The Constitution doesn't explicitly state this"
        <</SYS>>
        
        Context from Constitution:
        {context if context else "No specific context available"}
        
        Question: {query}
        
        Answer: [/INST]
        """
        
        # Add typing delay for better UX
        with st.spinner("Analyzing the Constitution..."):
            response = llm.invoke(prompt)
            time.sleep(0.5)  # Small delay to prevent UI flickering
            
        return response
        
    except Exception as e:
        st.error(f"System error: {str(e)}")
        return "Sorry, I encountered an error processing your request."

def main():
    st.title("🇰🇿 Kazakhstan Constitution AI Assistant")
    st.caption("Powered by Ollama with local LLMs")
    
    # File upload section with improved UI
    with st.expander("📁 Upload Constitution Documents", expanded=True):
        uploaded_files = st.file_uploader(
            "Select PDF or TXT files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            
            for i, file in enumerate(uploaded_files):
                try:
                    if file.type == "application/pdf":
                        chunks = process_pdf(file)
                    else:
                        text = file.read().decode("utf-8")
                        chunks = process_text(text)
                    
                    vector_db.add_documents(chunks)
                    progress_bar.progress((i + 1) / total_files)
                    
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
            
            st.success(f"Processed {len(uploaded_files)} document(s) successfully!")
            progress_bar.empty()
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me anything about Kazakhstan's Constitution"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle user input
    if prompt := st.chat_input("Your constitutional question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Retrieve relevant context
        # Replace the query section in main() with:
        results = vector_db.query(
            query_text=prompt,
            n_results=5
        )

        context = "\n\n".join([
            f"📜 Excerpt {i+1}:\n{doc}" 
            for i, doc in enumerate(results["documents"])
        ]) if results["documents"] else None
        
        # Generate and display response
        with st.chat_message("assistant"):
            response = generate_response(prompt, context)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()