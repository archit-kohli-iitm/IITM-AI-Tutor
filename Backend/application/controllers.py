import json
import yaml
import psutil
import time

from flask import Flask, after_this_request, send_file, abort
from flask_restx import Resource, Namespace

start_time = time.time()

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
