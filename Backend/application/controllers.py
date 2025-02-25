import json
import yaml
import psutil
import time
import datetime

from flask import Flask, after_this_request, send_file, abort, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Subject, mydb, User, Chat


start_time = time.time()

# -----------------------------------
#             HEALTH
# -----------------------------------

default_ns = Namespace('Default', description="Default operations")

@default_ns.route('/health')
class HealthCheck(Resource):
    def get(self):
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

subject_ns = Namespace('Subject', description="Operations for subjects")
subject_model = subject_ns.model('Subject', {
    'name': fields.String(required=True, description="Subject Name"),
})

@subject_ns.route('/')
class SubjectResource(Resource):
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

    )
    @jwt_required()
    def post(self):
        """Create a new subject"""
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
            200: 'Subject updated successfully',
            400: 'Bad Request', 
            403: 'Unauthorized (Admin privilege required)',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
    )
    @jwt_required()
    def put(self):
        """Update a subject"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        try:
            data = request.get_json()
            subject_id = data.get('subject_id',None)
            if subject_id is None:
                return {'message': 'Subject ID is required for update'}, 400 
            if not data.get('name'):
                return {'message': 'Subject name is required'}, 400
            subject = Subject.query.get(subject_id)
            if not subject:
                return {'message': 'Subject not found'}, 404            

            subject.name = data['name']
            mydb.session.commit()
            
            return {
                'message': 'Subject updated successfully',
                'subject': {
                    'subject_id': subject.subject_id,
                    'name': subject.name
                }
            }, 200
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error updating subject: {str(e)}'}, 500
    
    @subject_ns.doc(
        responses={
            200: 'Subject deleted successfully',
            400: 'Bad Request',
            403: 'Unauthorized (Admin privilege required)',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
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
            subject_id = data.get('subject_id',None)
            if subject_id is None:
                return {'message': 'Subject ID is required for update'}, 400 
            subject = Subject.query.get(subject_id)
            if not subject:
                return {'message': 'Subject not found'}, 404
                
            mydb.session.delete(subject)
            mydb.session.commit()
            
            return {'message': 'Subject deleted successfully'}, 200
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error deleting subject: {str(e)}'}, 500

@subject_ns.route('/list')
class ListAllSubjectChats(Resource):
    @subject_ns.doc(
        responses={
            200: 'Success',
            403: 'Invalid User',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
    )
    @jwt_required()
    def get(self):
        """Get all subjects and chats of a particular user"""
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
                        'name': subject.name
                        },
                    'created_at': chat.created_at.isoformat(),
                })
            return result, 200
        except Exception as e:
            return {'message': f'Error retrieving subject(s): {str(e)}'}, 500

# -----------------------------------
#             CHAT
# -----------------------------------


chat_ns = Namespace('Chat', description="Operations for chats")
chat_model = chat_ns.model('Chat', {
    'subject_id': fields.Integer(required=True, description="Subject ID"),
    'uid': fields.Integer(required=False, description="User ID"),
    'title': fields.String(required=False, description="Chat Name"),
})

@chat_ns.route('/<int:chat_id>')
class ChatResource(Resource):
    @chat_ns.doc(
        responses={
            200: 'Success',
            403: 'Invalid User',
            404: 'Chat not found',
            500: 'Internal Server Error'
        }
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
            'messages': chat.messages
        }
        return result, 200
    
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


@chat_ns.route('/create')
class CreateChatResource(Resource):
    @chat_ns.expect(chat_model)
    @chat_ns.doc(
        responses={
            201: 'Chat created successfully',
            400: 'Bad Request',
            403: 'Invalid User',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
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