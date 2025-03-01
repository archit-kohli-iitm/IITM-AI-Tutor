from flask import Flask, current_app
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_jwt_extended import JWTManager

from application.redis_cache import cache
from application.agent import RAGModel
from application.models import mydb
from application.config import *

from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

SOURCE_DIRECTORY = os.environ.get("SOURCE_DIRECTORY")
QDRANT_CLIENT_URL = os.environ.get("QDRANT_CLIENT_URL")
QDRANT_CLIENT_API_KEY = os.environ.get("QDRANT_CLIENT_API_KEY")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

def create_app():    
    myapp = Flask(__name__)
    myapp.config.from_object(DevConfig)

    api = Api(myapp,validate=True)
    
    mydb.init_app(myapp)
    bcrypt = Bcrypt(myapp)
    cache.init_app(myapp)
    jwt = JWTManager(myapp)
    CORS(myapp)

    # app initializations
    with myapp.app_context():
        if not hasattr(current_app, 'agent'):
            current_app.agent = RAGModel(
                gemini_model_name="gemini-exp-1206",
                gemini_api_key=GOOGLE_API_KEY,
                qdrant_collection_name=COLLECTION_NAME,
                qdrant_client_url=QDRANT_CLIENT_URL,
                qdrant_api_key=QDRANT_CLIENT_API_KEY
            )

        # check if the database exists
        mydb.create_all()
    
    return myapp,api

myapp,api = create_app()

from application.controllers import *
from application.auth import *

api.add_namespace(health_ns,'/health')
api.add_namespace(auth_ns,'/auth')
api.add_namespace(subject_ns,'/subjects')
api.add_namespace(chat_ns,'/chats')
api.add_namespace(message_ns,'/message')

# run the app
if __name__ == '__main__':
    myapp.run('0.0.0.0', port=5000, debug=True)