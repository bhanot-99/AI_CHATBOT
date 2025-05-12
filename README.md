🇰🇿 Kazakhstan Constitution AI Assistant
An AI-powered assistant that answers questions about the Constitution of Kazakhstan using locally hosted language models via Ollama. The application features a user-friendly interface built with Streamlit and utilizes ChromaDB for efficient document retrieval.

🧠 Features
Local LLM Integration: Run language models like LLaMA, Mistral, or Phi locally using Ollama.

Document Upload: Upload PDF or TXT files containing the Constitution or related documents.

Vector Database: Store and retrieve document embeddings using ChromaDB.

Context-Aware Responses: Generate answers based on the uploaded documents.

Interactive UI: Engage with the assistant through a Streamlit-powered web interface.

Clone the Repository

git clone https://github.com/bhanot-99/AI_CHATBOT.git
cd AI_CHATBOT

2. Install Dependencies
Ensure you have Python 3.8 or higher installed. Then, create a virtual environment and install the required packages:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Install and Set Up Ollama
Follow the instructions on the Ollama website to install and configure Ollama on your system. Once installed, download the desired language model. For example:

ollama pull llama2
Replace llama2 with the model of your choice.

4. Configure Environment Variables
Create a .env file in the project root directory and add any necessary environment variables. For example:

OLLAMA_MODEL=llama2
Ensure that the model name matches the one you downloaded with Ollama.

💻 Running the Application
Start the Streamlit application:

streamlit run app.py
This will launch the web interface in your default browser. From there, you can upload documents and interact with the AI assistant.


📁 Project Structure

AI_CHATBOT/
├── app.py                 # Main Streamlit application
├── documents/             # Directory to store uploaded documents
├── utils/                 # Utility functions and modules
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

📝 License
This project is licensed under the MIT License. See the LICENSE file for details.