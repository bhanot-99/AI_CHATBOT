import chromadb
from chromadb.utils import embedding_functions

class VectorDB:
    def __init__(self):
        self.client = chromadb.Client()
        self.embedding_func = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="constitution_kz",
            embedding_function=self.embedding_func
        )
    
    def add_documents(self, documents, metadatas=None, ids=None):
        if not metadatas:
            metadatas = [{} for _ in documents]
        if not ids:
            ids = [str(i) for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text, n_results=3):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results