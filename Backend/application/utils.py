from flask import current_app
from application.agent import RAGModel
from dotenv import load_dotenv
import os
import time

import logging
logger = logging.getLogger(__name__)

load_dotenv()

SOURCE_DIRECTORY = os.environ.get("SOURCE_DIRECTORY")
QDRANT_CLIENT_URL = os.environ.get("QDRANT_CLIENT_URL")
QDRANT_CLIENT_API_KEY = os.environ.get("QDRANT_CLIENT_API_KEY")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME")

# retry decorator
def retry(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.info(f"Error occurred: {e}")
                time.sleep(1)
        return None
    return wrapper

def getAgent():
    if not hasattr(current_app, "agent"):
        current_app.agent = RAGModel(
            gemini_model_name=GEMINI_MODEL_NAME,
            gemini_api_key=GOOGLE_API_KEY,
            qdrant_collection_name=COLLECTION_NAME,
            qdrant_client_url=QDRANT_CLIENT_URL,
            qdrant_api_key=QDRANT_CLIENT_API_KEY
        )
    return current_app.agent

def getChatHistory(messages,msg_limit=None):
    if not messages:
        return None
    out = ""
    for message in messages if not msg_limit else messages[-msg_limit:]:
        out += f"{message.timestamp} - {message.msg_type}: {message.content}\n"
    return out

def getContextHistory(messages,ctx_limit=None):
    if not messages:
        return None
    context = ""
    for message in messages if not ctx_limit else messages[-ctx_limit:]:
        if message.context:
            context += f"{message.context}\n"
    return context

@retry
def getQueryResponse(query, messages):
    chat_history = getChatHistory(messages, msg_limit=None)
    logger.info(f"User Query: {query}")
    
    agent = getAgent()
    response_generator = agent.stream(query, chat_history=chat_history)
    
    return response_generator