from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding, SparseTextEmbedding
from application.prompt import SYSTEM_PROMPT, GUARDRAIL_PROMPT
from application.constants import *
import json
from pydantic import BaseModel
import re

class ContextRetriever():
    dense_model_name = "models/text-embedding-004"

    def __init__(self, collection_name, client_url, google_api_key, qdrant_api_key=None):

        self.client = QdrantClient(url=client_url,api_key=qdrant_api_key)
        self.collection_name = collection_name
        self.dense_embedding_model = GoogleGenerativeAIEmbeddings(model=self.dense_model_name,google_api_key=google_api_key)
        
        if not self.client.collection_exists(collection_name):
            raise Exception(f"Collection with name {collection_name} does not exist. Please create the collection first")

    def retrieve(self, query, num_documents=10):
        dense_query_vector = self.dense_embedding_model.embed_query(query)
        prefetch = [
            models.Prefetch(
                query=dense_query_vector,
                using=self.dense_model_name,
                limit=20,
            ),
        ]
        results = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=prefetch,
            query=models.FusionQuery(
                fusion=models.Fusion.RRF,
            ),
            with_payload=True,
            limit=num_documents,
        )

        return results

class RAGModel():
    def __init__(self,gemini_model_name:str,gemini_api_key:str,qdrant_collection_name:str,qdrant_client_url:str,qdrant_api_key:str):
        self.llm = ChatGoogleGenerativeAI(model=gemini_model_name,api_key=gemini_api_key)
        self.retriever = ContextRetriever(qdrant_collection_name, qdrant_client_url, gemini_api_key, qdrant_api_key)

    def _get_context(self, query:str):
        points = self.retriever.retrieve(query).points
        result = []
        for point in points:
            result.append(point.payload)
        return result
    
    def stream(self, query:str, chat_history:str=None):

        try:
            guardrail_prompt = GUARDRAIL_PROMPT.format(query=query)
            class GuardrailResponse(BaseModel):
                category: str
            guardrail_response = self.llm.with_structured_output(GuardrailResponse).invoke(guardrail_prompt)
            if guardrail_response is None:
                guardrail_response = self.llm.invoke(guardrail_prompt)
                guardrail_response = json.loads(re.search(r'{.*}', guardrail_response.content, re.DOTALL).group(0))

            category = guardrail_response.get("category", "VALID")
            if category not in categories:
                category = "VALID"
        except Exception as e:
            print(f"Guardrail error: {e}")
            category = "VALID"

        if category != "VALID":
            def rejection_response():
                if category == "UNETHICAL":
                    yield UNETHICAL_RESPONSE, None
                elif category == "INVALID":
                    yield INVALID_RESPONSE, None
                else:
                    yield ERROR_RESPONSE, None
            return rejection_response()

        context_documents = self._get_context(query)
        context = "\n\n".join([doc["content"] for doc in context_documents])
        formatted_prompt = SYSTEM_PROMPT.format(chat_history=chat_history, input_query=query, context=context)
        
        stream = self.llm.stream(formatted_prompt)
        
        def response_generator():
            full_response = []
            try:
                for chunk in stream:
                    chunk_text = chunk.content
                    full_response.append(chunk_text)
                    yield chunk_text, None  # Streaming chunk
                
                # Final yield with complete response and context
                yield ''.join(full_response), context
            except Exception as e:
                print(f"Streaming error: {e}")
                yield "Error in generating response", None
                
        return response_generator()
    
    def _get_history(self, *args, **kwargs):
        pass
    
    def __call__(self, query:str, chat_history:str=None):
        context_documents = self._get_context(query)
        context = "\n\n".join([doc["content"] for doc in context_documents])
        formatted_prompt = SYSTEM_PROMPT.format(chat_history=chat_history, input_query=query, context=context)
        response = self.llm.invoke(formatted_prompt)
        
        return response, context
