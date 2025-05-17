import os
import time
import chromadb
from chromadb.utils import embedding_functions
from pymongo import MongoClient

class VectorDB:
    def __init__(self):
        # Initialize ChromaDB for vector search
        self.client = chromadb.Client()
        self.embedding_func = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="constitution_kz",
            embedding_function=self.embedding_func
        )
        # Initialize MongoDB for Q&A storage
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client["constitution_ai"]
        self.qa_collection = self.mongo_db["qa_pairs"]
    

    def add_documents(self, documents, metadatas=None, ids=None):
        # Ensure each document has at least an empty metadata dict
        if metadatas is None:
            metadatas = [{"source": "uploaded_document"} for _ in documents]
        elif len(metadatas) != len(documents):
            metadatas = [{} for _ in documents]
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}_{hash(doc[:50])}" for i, doc in enumerate(documents)]
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text, n_results=5):
        """Returns documents and their metadata"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0]
        }

    def save_qa_pair(self, question, answer, context=None):
        doc = {
            "question": question,
            "answer": answer,
            "context": context,
            "timestamp": time.time()
        }
        self.qa_collection.insert_one(doc)