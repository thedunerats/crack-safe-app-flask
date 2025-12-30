import os
from functools import wraps
from flask import request, jsonify


def require_api_key(f):
    """
    Decorator to require API key authentication for routes.
    
    The API key should be provided in the request headers as 'X-API-Key'.
    The expected API key is stored in the environment variable 'API_KEY'.
    
    This authentication method is generic and works regardless of:
    - Client IP address
    - Domain/hostname
    - Geographic location
    
    Usage:
        @app.route('/api/endpoint')
        @require_api_key
        def endpoint():
            return jsonify({'message': 'Success'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from environment
        expected_api_key = os.environ.get('API_KEY')
        
        # If no API key is configured, reject all requests
        if not expected_api_key:
            return jsonify({
                'error': 'Server configuration error: API key not configured'
            }), 500
        
        # Get API key from request headers
        provided_api_key = request.headers.get('X-API-Key')
        
        # Check if API key was provided
        if not provided_api_key:
            return jsonify({
                'error': 'Unauthorized: API key required',
                'message': 'Please provide API key in X-API-Key header'
            }), 401
        
        # Validate API key
        if provided_api_key != expected_api_key:
            return jsonify({
                'error': 'Unauthorized: Invalid API key'
            }), 401
        
        # API key is valid, proceed with the request
        return f(*args, **kwargs)
    
    return decorated_function
