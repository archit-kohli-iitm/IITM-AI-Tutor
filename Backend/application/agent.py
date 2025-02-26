import time

class ContextRetriever():
    def __init__(self, collection_name, client_url, google_api_key, qdrant_api_key=None):
        self.collection_name = collection_name

    def retrieve(self, query, num_documents=10):
        return {"points": [{"payload": {"content": "Dummy context for: " + query}}] * num_documents}

class RAGModel():
    def __init__(self, gemini_model_name: str, gemini_api_key: str, qdrant_collection_name: str, qdrant_client_url: str, qdrant_api_key: str):
        self.retriever = ContextRetriever(qdrant_collection_name, qdrant_client_url, gemini_api_key, qdrant_api_key)

    def _get_context(self, query: str):
        points = self.retriever.retrieve(query)["points"]
        return [point["payload"] for point in points]
    
    def stream(self, query: str, chat_history: str = None):
        context_documents = self._get_context(query)
        context = "\n\n".join([doc["content"] for doc in context_documents])
        
        def response_generator():
            full_response = []
            for chunk in ["This is a dummy", " response part 1.", " This is part 2."]:
                time.sleep(1)
                full_response.append(chunk)
                yield chunk, None
            yield "".join(full_response), context
        
        return response_generator()
    
    def __call__(self, query: str, chat_history: str = None):
        context_documents = self._get_context(query)
        context = "\n\n".join([doc["content"] for doc in context_documents])
        response = "This is a hardcoded response to: " + query
        return response, context