from google import genai
from google.genai import types
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding, SparseTextEmbedding
from application.prompt import *
from application.constants import *
import json
from pydantic import BaseModel
import re
import httpx
from fuzzywuzzy import process

import logging
logger = logging.getLogger(__name__)

class ContextRetriever():
    dense_model_name = "models/text-embedding-004"

    def __init__(self, collection_name, client_url, google_api_key, qdrant_api_key=None):
        self.client = QdrantClient(url=client_url, api_key=qdrant_api_key)
        self.collection_name = collection_name
        self.genai_client = genai.Client(api_key=google_api_key)
        
        if not self.client.collection_exists(collection_name):
            raise Exception(f"Collection with name {collection_name} does not exist. Please create the collection first")

    def embed_query(self, text):
        response = self.genai_client.models.embed_content(
            model=self.dense_model_name,
            contents=[text],
        )
        return response.embeddings[0].values

    def retrieve(self, query, num_documents=5):
        dense_query_vector = self.embed_query(query)
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



class PromptBuilder:
    @staticmethod
    def build_system_prompt(query: str, chat_history: str, context: str) -> str:
        return SYSTEM_PROMPT.format(chat_history=chat_history, input_query=query, context=context)
    
    @staticmethod
    def build_summarization_prompt(query:str, chat_history: str) -> str:
        return SUMMARIZATION_PROMPT.format(query=query,chat_history=chat_history)
    
    @staticmethod
    def build_classifier_prompt(query: str, chat_history: str) -> str:
        return CLASSIFIER_PROMPT.format(query=query, chat_history=chat_history)
    
    @staticmethod
    def build_assignment_prompt(query: str, week: str, chat_history:str) -> str:
        if int(week)%2 == 0:
            return PRACTICE_ASSIGNMENT_PROMPT.format(query=query, chat_history=chat_history)
        else:
            return GRADED_ASSIGNMENT_PROMPT.format(query=query, chat_history=chat_history)

class Utils:
    @staticmethod
    def jsonify(s: str):
        s = re.sub(r"```(?:json)?", "", s, flags=re.IGNORECASE).strip()

        match = re.search(r'(\{.*\}|\[.*\])', s, flags=re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object or array found in the string.")

        json_str = match.group(1)
        return json.loads(json_str)
    
    @staticmethod
    def extractWeek(w: int):
        return week2assgn["Week "+str(w)]

class QueryClassifier:
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def classify(self, query: str, chat_history:str) -> str:
        prompt = PromptBuilder.build_classifier_prompt(query, chat_history)
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            response = Utils.jsonify(response.text)
            return response
        except Exception as e:
            logger.info("Error in classify" + str(e))
            return {"guardrail_category":"ERROR"}
            

class ResponseGenerator:
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name

    def rejection_generator(self, category: str):
        def generator():
            if category == "INVALID":
                yield INVALID_RESPONSE, None
            elif category == "NOT_FOUND":
                yield NOT_FOUND_RESPONSE, None
            else:
                yield ERROR_RESPONSE, None
        return generator()

    def _load_pdf_parts(self, pdf_sources):
        parts = []
        for src in pdf_sources or []:
            try:
                file_id = src.split("/file/d/")[1].split("/")[0]
                src = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"

                response = httpx.get(src)
                response.raise_for_status()
                parts.append(types.Part.from_bytes(
                        data=response._content,
                        mime_type='application/pdf',
                    )
                )
            except Exception as e:
                logger.info(f"Error loading PDF from {src}: {e}")
        return parts

    def _build_content(self, prompt: str, context: str = None, pdf_sources=None):
        parts = self._load_pdf_parts(pdf_sources)
        if context:
            parts.append(f"\n\nContext:\n{context}")
        parts.append(prompt)
        return parts

    def stream_response(self, prompt: str, context: str = None, pdf_paths=None):
        contents = self._build_content(prompt, context, pdf_paths)
        stream = self.client.models.generate_content_stream(
            model=self.model_name,
            contents=contents
        )

        def generator():
            full_response = []
            try:
                for chunk in stream:
                    chunk_text = chunk.text
                    full_response.append(chunk_text)
                    yield chunk_text, None
            except Exception as e:
                logger.info(f"Streaming error: {e}")
                yield ERROR_RESPONSE, None

            # Add sources after the stream ends
            if pdf_paths:
                sources_text = "\n\n##### Sources:\n" + "\n".join(f"- {path}" for path in set(pdf_paths))
                yield sources_text, None

        return generator()


    def get_response(self, prompt: str, context: str = None, pdf_paths=None):
        contents = self._build_content(prompt, context, pdf_paths)
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents
            )
            return response.text
        except Exception as e:
            logger.info(f"Response error: {e}")
            return ERROR_RESPONSE


class RAGModel:
    def __init__(self, gemini_model_name: str, gemini_api_key: str,
                 qdrant_collection_name: str, qdrant_client_url: str, qdrant_api_key: str):
        self.model_name = gemini_model_name
        self.genai_client = genai.Client(api_key=gemini_api_key)

        self.retriever = ContextRetriever(qdrant_collection_name, qdrant_client_url,
                                          gemini_api_key, qdrant_api_key)
        self.classifier = QueryClassifier(self.genai_client, self.model_name)
        self.generator = ResponseGenerator(self.genai_client, self.model_name)

    def _get_context_string(self, query: str) -> tuple[list,str]:
        context_documents = self.retriever.retrieve(query).points
        sources = list(set(doc.payload["source"] for doc in context_documents))
        pdf_paths = []
        for src in sources:
            title = process.extractOne(src, title2lecture.keys())[0]
            if title is not None:
                week, lec = title2lecture[title]
                pdf_paths.append(week2pdf[week][lec]["Transcript"])
        return pdf_paths, "\n\n".join([doc.payload["content"] for doc in context_documents])

    # def _get_context_source(self, query: str) -> tuple[str, str]:
    #     week = int(self.retriever.retrieve(query,1).points[0].payload["metadata"]["week"])
    #     if week%2 == 0:
    #         assgn_type = "GRADED"
    #     else:
    #         assgn_type = "PRACTICE"
    #     source_path = Utils.extractWeek(week)
    #     return source_path, assgn_type

    def stream(self, query: str, chat_history: str = None):
        category = self.classifier.classify(query, chat_history)
        logger.info(category)

        if category["guardrail_category"] == "INVALID" :
            return self.generator.rejection_generator("INVALID")
        
        elif category["guardrail_category"] == "VALID":
            if category["category"] == "ASSIGNMENT":
                try:
                    pdf_path = week2assgn["Week "+str(category["week"])]
                    prompt = PromptBuilder.build_assignment_prompt(query, category["week"], chat_history)
                    return self.generator.stream_response(prompt=prompt, pdf_paths=[pdf_path])
                except Exception as e:
                    logger.info(e)
                    return self.generator.rejection_generator("NOT_FOUND")
            
            elif category["category"] == "SUMMARIZATION":
                try:
                    if "week" in category and category["week"] is not None and category["week"].isnumeric():
                        if "lecture" in category and category["lecture"] is not None and category["lecture"].isnumeric():
                            pdf_paths = [week2pdf["Week "+str(category["week"])]["Lecture "+str(category["lecture"])]["Transcript"]]
                        else:
                            pdf_paths = [week2pdf["Week "+str(category["week"])][lecture]["Transcript"] for lecture in week2pdf["Week "+str(category["week"])]]
                    else:
                        pdf_paths = None
                    prompt = PromptBuilder.build_summarization_prompt(query=query,chat_history=chat_history)
                    return self.generator.stream_response(prompt=prompt,pdf_paths=pdf_paths)
                except Exception as e:
                    logger.info(e)
                    return self.generator.rejection_generator("NOT_FOUND")
            
            else:
                try:
                    if "week" in category and category["week"] is not None and category["week"].isnumeric():
                        if "lecture" in category and category["lecture"] is not None and category["lecture"].isnumeric():
                            pdf_paths = [week2pdf["Week "+str(category["week"])]["Lecture "+str(category["lecture"])]["Transcript"]]
                        else:
                            pdf_paths = [week2pdf["Week "+str(category["week"])][lecture]["Transcript"] for lecture in week2pdf["Week "+str(category["week"])]]
                    else:
                        pdf_paths = None
                except Exception as e:
                    logger.info(e)
                    return self.generator.rejection_generator("NOT_FOUND")
                if pdf_paths is None and ("what_context_needed" not in category or category["what_context_needed"] != "NO CONTEXT NEEDED"):
                    if "what_context_needed" not in category:
                        pdf_paths, context = self._get_context_string(query)
                    else:
                        pdf_paths, context = self._get_context_string(category["what_context_needed"])
                else:
                    context = None
                logger.info(f"{context} {pdf_paths}")
                prompt = PromptBuilder.build_system_prompt(query, chat_history, context)
                return self.generator.stream_response(prompt=prompt, context=context, pdf_paths=pdf_paths)
        else:
            return self.generator.rejection_generator("ERROR")

    def __call__(self, query: str, chat_history: str = None):
        context = self._get_context_string(query)
        prompt = PromptBuilder.build_system_prompt(query, chat_history, context)
        response = self.generator.get_response(prompt)
        return response, context

