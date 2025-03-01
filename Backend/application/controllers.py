import json
import yaml
import psutil
import time
import datetime

from flask import Flask, after_this_request, send_file, abort, request, stream_with_context, Response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Subject, mydb, User, Chat, Message
from application.utils import *


start_time = time.time()

# -----------------------------------
#             HEALTH
# -----------------------------------

health_ns = Namespace('Health', description="Check API health")

@health_ns.route('/')
class HealthCheck(Resource):
    @health_ns.doc(
        description="Get API health information like `uptime_seconds`, `cpu usage_percent` and `memory_usage_percent`"
    )
    def get(self):
        """Get health information"""
        uptime = time.time() - start_time
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        health_status = {
            "status": "healthy",
            "uptime_seconds": uptime,
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_usage
        }
        
        return health_status, 200


# -----------------------------------
#             SUBJECT
# -----------------------------------

subject_ns = Namespace('Subject', description="Subject Management operations")
subject_model = subject_ns.model('Subject', {
    'name': fields.String(required=True, description="Subject Name"),
})

@subject_ns.route('/')
class SubjectResource(Resource):
    @subject_ns.doc(
        responses={
            200: 'Subjects retrieved successfully',
            403: 'Unauthorized (Admin privilege required)',
            500: 'Internal Server Error'
        },
        description="List all subjects currently available in the database along with their `subject_id` and `name`"
    )
    @jwt_required()
    def get(self):
        """List all subjects"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        try:
            subjects = Subject.query.all()
            response = []
            for subject in subjects:
                response.append({
                    "subject_id":subject.subject_id,
                    "name": subject.name
                })
            return response, 200
        except Exception as e:
            return {'message': f'Error retrieving subject(s): {str(e)}'}, 500

    @subject_ns.expect(subject_model)
    @subject_ns.doc(
        responses={
            201: 'Subject created successfully',
            200: 'Subject updated successfully',
            400: 'Bad Request',
            403: 'Unauthorized (Admin privilege required)',
            404: 'Subject not found',
            500: 'Internal Server Error'
        },
        description="Add a new subject to the database (Admin privileges required)"
    )
    @jwt_required()
    def post(self):
        """Add a new subject"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        try:
            data = request.get_json()
            if not data.get('name'):
                return {'message': 'Subject name is required'}, 400
            new_subject = Subject(name=data['name'])
            mydb.session.add(new_subject)
            mydb.session.commit()
            return {
                'message': 'Subject created successfully',
                'subject': {
                    'subject_id': new_subject.subject_id,
                    'name': new_subject.name
                }
            }, 201
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error creating subject: {str(e)}'}, 500
    
    @subject_ns.expect(subject_model)
    @subject_ns.doc(
        responses={
            200: 'Subject deleted successfully',
            400: 'Bad Request',
            403: 'Unauthorized (Admin privilege required)',
            404: 'Subject not found',
            500: 'Internal Server Error'
        },
        description="Remove a subject from the database (Admin privileges required)"
    )
    @jwt_required()
    def delete(self):
        """Delete a subject"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        try:
            data = request.get_json()
            if not data.get('name'):
                return {'message': 'Subject name is required'}, 400
            subject_name = data.get('name')
            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                return {'message': 'Subject not found'}, 404
                
            mydb.session.delete(subject)
            mydb.session.commit()
            
            return {'message': 'Subject deleted successfully'}, 200
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error deleting subject: {str(e)}'}, 500


# -----------------------------------
#             CHAT
# -----------------------------------


chat_ns = Namespace('Chat', description="Operations for chats")
chat_model = chat_ns.model('Chat', {
    'subject_id': fields.Integer(required=True, description="Subject ID"),
    'title': fields.String(required=False, description="Chat Name"),
})

@chat_ns.route('/<int:chat_id>')
class SpecificChatResource(Resource):
    @chat_ns.doc(
        responses={
            200: 'Success',
            403: 'Invalid User',
            404: 'Chat not found',
            500: 'Internal Server Error'
        },
        description="Get all messages from a particular `chat_id` (Chat must belong to the current user)"
    )
    @jwt_required()
    def get(self, chat_id=None):
        """Get all messages from a chat"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return {"message": "Invalid User"}, 403
        if chat_id is None:
            return {"message": "Bad Request, chat_id is required"}, 400
        
        chat = Chat.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, 404
        if chat.uid != user.uid:
            return {"message": "Chat does not belong to the user"}, 403
        subject = Subject.query.filter_by(subject_id=chat.subject_id).first()
        result = {
            'chat_id': chat.chat_id,
            'title': chat.title,
            'subject':{
                'subject_id': subject.subject_id,
                'name': subject.name
                },
            'created_at': chat.created_at.isoformat(),
            'messages': [message.to_dict() for message in chat.messages]
        }
        return result, 200
    
    @chat_ns.doc(
        responses={
            200: 'Success',
            400: 'Bad Request',
            403: 'Invalid User',
            404: 'Chat not found',
            500: 'Internal Server Error'
        },
        description="Get all messages from a particular `chat_id` (Chat must belong to the current user)"
    )
    @jwt_required()
    def delete(self, chat_id=None):
        """Delete a chat"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return {"message": "Invalid User"}, 403
        if chat_id is None:
            return {'message': 'Chat ID is required for deletion'}, 400
            
        try:
            chat = Chat.query.filter_by(chat_id=chat_id).first()
            if not chat:
                return {'message': 'Chat not found'}, 404
            if chat.uid!=user.uid:
                return {'message': 'Chat does not belong to the user'}, 403
            
            mydb.session.delete(chat)
            mydb.session.commit()
            
            return {'message': 'Chat deleted successfully'}, 200
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error deleting chat: {str(e)}'}, 500


@chat_ns.route('/')
class ChatResource(Resource):
    @chat_ns.doc(
        responses={
            200: 'Success',
            403: 'Invalid User',
            404: 'Subject not found',
            500: 'Internal Server Error'
        },
        description="Get a list of all chats of the current user including the `subject_id` and `subject_name`. (Does not include chat messages)"
    )
    @jwt_required()
    def get(self):
        """Lists all chats of the current user"""
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            if not user:
                return {"message": "Invalid User"}, 403            
            result = []
            for chat in user.chats:
                subject = Subject.query.filter_by(subject_id=chat.subject_id).first()
                result.append({
                    'chat_id': chat.chat_id,
                    'title': chat.title,
                    'subject':{
                        'subject_id': subject.subject_id,
                        'subject_name': subject.name
                        },
                    'created_at': chat.created_at.isoformat(),
                })
            return result, 200
        except Exception as e:
            return {'message': f'Error retrieving subjectChat(s): {str(e)}'}, 500

    @chat_ns.expect(chat_model)
    @chat_ns.doc(
        responses={
            201: 'Chat created successfully',
            400: 'Bad Request',
            403: 'Invalid User',
            404: 'Subject not found',
            500: 'Internal Server Error'
        },
        description="Create a new chat belonging to the current user under a specified subject"
    )
    @jwt_required()
    def post(self, chat_id=None):
        """Create a new chat"""
        if chat_id is not None:
            return {'message': 'Invalid endpoint for POST request, ID not required'}, 400
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            if not user:
                return {"message": "Invalid User"}, 403
            data = request.get_json()
            subject = Subject.query.get(data['subject_id'])
            if not subject:
                return {'message': 'Subject not found'}, 404
                
            new_chat = Chat(
                uid=user.uid,
                subject_id=data['subject_id'],
                title=data.get('title', 'New Chat')
            )
            
            mydb.session.add(new_chat)
            mydb.session.commit()
            
            return {
                'message': 'Chat created successfully',
                'chat': {
                    'chat_id': new_chat.chat_id,
                    'title': new_chat.title,
                    'subject': {
                        'subject_id': subject.subject_id,
                        'name': subject.name
                    },
                    'created_at': new_chat.created_at.isoformat()
                }
            }, 201
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error creating chat: {str(e)}'}, 500
        

# -----------------------------------
#             MESSAGE
# -----------------------------------

message_ns = Namespace('Message', description="Operations for messages")
message_model = message_ns.model('Message', {
    'chat_id': fields.Integer(required=True, description="Subject ID"),
    'content': fields.String(required=True, description="Message Content")
})
@message_ns.route('/send')
class MessageResource(Resource):
    @message_ns.expect(message_model)
    @message_ns.doc(
        responses={
            200: 'Streaming Response from AI',
            403: 'Invalid User',
            500: 'Internal Server Error'
        },
        description="Send a message to the AI Tutor with context information automatically fetched from a particular `chat_id` and vector database (Returns a stream of output tokens)"
    )
    @jwt_required()
    def post(self):
        """Send a message to the AI Tutor"""
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            if not user:
                return {"message": "Invalid User"}, 403
            
            data = request.get_json()
            chat_id = data.get('chat_id')
            content = data.get('content')
            
            chat = Chat.query.filter_by(chat_id=chat_id).first()
            
            def generate_response():
                complete_response = []
                context = None
                try:
                    # Store user message immediately
                    user_message = Message(content=content, context='')
                    chat.messages.append(user_message)
                    mydb.session.commit()

                    # Get streaming response from LLM
                    response_generator = getQueryResponse(content, chat.messages)
                    
                    for chunk_text, ctx in response_generator:
                        if ctx is not None:  # This is the final yield with context
                            context = ctx
                            break
                        complete_response.append(chunk_text)
                        yield chunk_text
                    
                    # Store complete AI response after streaming
                    final_response = ''.join(complete_response)
                    ai_message = Message(
                        content=final_response,
                        msg_type='assistant',
                        context=context if context else ''
                    )
                    chat.messages.append(ai_message)
                    mydb.session.commit()

                except Exception as e:
                    error_msg = "Error: Failed to get response. Please try again."
                    yield error_msg
                    
                    ai_message = Message(
                        content=error_msg,
                        msg_type='assistant',
                        context=''
                    )
                    chat.messages.append(ai_message)
                    mydb.session.commit()
            return Response(
                stream_with_context(generate_response()),
                mimetype='text/plain'
            )
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error getting response: {str(e)}'}, 500