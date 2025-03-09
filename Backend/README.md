# AI Tutor for academic guidance

### The application backend is written in Flask and follows the standard Flask REST API structure and best code practices. The backend has also been deployed and can be found at [ai-study-iitm-backend.onrender.com](https://ai-tutor-iitm-backend.onrender.com)

## Features
- RESTful API architecture
- Database integration with SQLAlchemy
- Authentication and authorization
- Request validation and error handling
- CORS support for frontend integration
- RAG model for Question Answering

## Prerequisites
- Python (recommended: v3.10.11)

## Technologies Used
- **Flask** - Lightweight web framework for building APIs
- **Flask-Bcrypt** - Secure password hashing
- **Flask-JWT-Extended** - Authentication and token management
- **Flask-RESTx** - API documentation and request parsing
- **Flask-SQLAlchemy** - ORM for database interactions
- **LangChain-Google-GenAI** - AI model integration for chatbot functionality
- **Qdrant-Client [FastEmbed]** - Vector database for similarity search
- **Psutil** - System monitoring utilities
Here's a cleaner and more structured version of your README setup instructions:  

## Installation
1. Open the folder on the local system:
   ```sh
   cd Backend
   ```
2. Create a virtual environment and activate it (_We recommend using Python 3.10.11_):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables using one of the following methods:

   **Option 1: Retrieve from a shared document**  
   - Download the environment variables from [this link](https://docs.google.com/document/d/12lkPKbjwtNIgZAGyzB-CguNvvUAEZhqAYi_FL9vPo6o/edit?usp=sharing)  
   - Save them in a file named `.env` in the same directory as `.env.dist`

   **Option 2: Manually generate the required keys**  
   - Login to [Qdrant](https://qdrant.tech/), start a cluster, and obtain:  
     - `QDRANT_CLIENT_URL`  
     - `QDRANT_CLIENT_API_KEY`  
   - Create a new collection (or get credentials from @Archit-Kohli) and set:  
     - `COLLECTION_NAME`  
   - Login to [Google AI Studio](https://aistudio.google.com/welcome) (requires a personal account with billing enabled) and get:  
     - `GOOGLE_API_KEY`  
   - Generate a secure key and password salt (numeric) using a hash function and set:  
     - `SECRET_KEY`  
     - `SECURITY_PASSWORD_SALT`  

5. Run the program:
   ```sh
   python main.py
   ```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Authenticate user |
| POST | `/auth/logout` | Logout user |
| POST | `/auth/signup` | Register a new user |
| POST | `/chats/create` | Create a new chat |
| GET | `/chats/{chat_id}` | Get all messages from a chat |
| DELETE | `/chats/{chat_id}` | Delete a chat |
| GET | `/default/health` | Check API stats |
| POST | `/message/send` | Send a message to AI |
| GET | `/subjects/` | Get all subjects |
| POST | `/subjects/` | Create a new subject |
| DELETE | `/subjects/` | Delete a subject |
| GET | `/subjects/list` | Get all subjects and chats of a user |

## Documentation
You can find the API documentation on running the application at `http://127.0.0.1:5000/` or through the `documentation.yaml` file provided in the codebase.

## Project Structure

The project follows the standard Flask API structure with the following key files:

- `application/`: Application directory
  - `agent.py`: RAG Agent
  - `auth.py`: Authentication APIs
  - `config.py`: Flask Config
  - `controllers.py`: API Definitions
  - `models.py`: DB Models
  - `prompt.py`: LLM Prompt
  - `redis_cache.py`: Redis Initialization
  - `utils.py`: Utility Functions
- `instance/`: Database Instance
- `main.py`: Entrypoint
- `ingestion.ipynb`: Ingestion Code for Vector DB
- `requirements.txt`: Project Requirements

## Run the test cases
   ```sh
   cd Backend
   pytest/tests
   ```