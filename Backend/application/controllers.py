import json
import yaml
import psutil
import time

from flask import Flask, after_this_request, send_file, abort, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Subject, mydb, User

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

core_ns = Namespace('Core', description="Core operations for subject, chat and message")

# -----------------------------------
#             SUBJECT
# -----------------------------------

subject_model = core_ns.model('Subject', {
    'name': fields.String(required=True, description="Subject Name"),
})

@core_ns.route('/subjects', '/subjects/<int:subject_id>')
class SubjectResource(Resource):
    @core_ns.doc(
        responses={
            200: 'Success',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
    )
    def get(self, subject_id=None):
        """Get all subjects or a specific subject by ID"""
        try:
            if subject_id is None:
                subjects = Subject.query.all()
                result = []
                for subject in subjects:
                    result.append({
                        'subject_id': subject.subject_id,
                        'name': subject.name
                    })
                return result, 200
            else:
                subject = Subject.query.get(subject_id)
                if not subject:
                    return {'message': 'Subject not found'}, 404
                return {
                    'subject_id': subject.subject_id,
                    'name': subject.name
                }, 200
        except Exception as e:
            return {'message': f'Error retrieving subject(s): {str(e)}'}, 500
    
    @core_ns.expect(subject_model)
    @core_ns.doc(
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
    def post(self, subject_id=None):
        """Create a new subject"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        if subject_id is not None:
            return {'message': 'Invalid endpoint for POST request, ID not required'}, 400
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
    
    @core_ns.expect(subject_model)
    @core_ns.doc(
        responses={
            200: 'Subject updated successfully',
            400: 'Bad Request', 
            403: 'Unauthorized (Admin privilege required)',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
    )
    @jwt_required()
    def put(self, subject_id=None):
        """Update a subject"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        if subject_id is None:
            return {'message': 'Subject ID is required for update'}, 400 
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                return {'message': 'Subject not found'}, 404
                
            data = request.get_json()
            
            if not data.get('name'):
                return {'message': 'Subject name is required'}, 400
                
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
    
    @core_ns.doc(
        responses={
            200: 'Subject deleted successfully',
            400: 'Bad Request',
            403: 'Unauthorized (Admin privilege required)',
            404: 'Subject not found',
            500: 'Internal Server Error'
        }
    )
    @jwt_required()
    def delete(self, subject_id=None):
        """Delete a subject"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if not user or user.utype != "tpadmin":
            return {"message": "Admin privileges required"}, 403
        if subject_id is None:
            return {'message': 'Subject ID is required for deletion'}, 400
            
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                return {'message': 'Subject not found'}, 404
                
            mydb.session.delete(subject)
            mydb.session.commit()
            
            return {'message': 'Subject deleted successfully'}, 200
        except Exception as e:
            mydb.session.rollback()
            return {'message': f'Error deleting subject: {str(e)}'}, 500

