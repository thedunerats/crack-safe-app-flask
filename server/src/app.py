from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from src.services.safe_cracker import crack_safe, crack_safe_streaming
from src.middleware.auth import require_api_key

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure CORS based on environment
# In production, you should restrict this to your actual domain
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:4200').split(',')
CORS(app, origins=allowed_origins)


@app.route('/', methods=['GET'])
def home():
    """
    Default GET endpoint to verify the app is running.
    This endpoint does not require authentication.
    """
    return jsonify({
        'status': 'connected',
        'message': 'Safe Cracking API is running',
        'endpoints': {
            'crack_safe': '/api/crack_safe/ [POST] - Requires API Key',
            'crack_safe_stream': '/api/crack_safe/stream [POST] - Requires API Key (Real-time updates)'
        }
    }), 200


@app.route('/api/crack_safe/', methods=['POST'])
@require_api_key
def crack_safe_endpoint():
    """
    POST endpoint to crack a safe combination.
    
    Request Body:
        {
            "actual_combination": "08066666"
        }
    
    Response:
        {
            "attempts": 123,
            "time_taken": 15.75
        }
    """
    data = request.get_json()
    
    if not data or 'actual_combination' not in data:
        return jsonify({'error': 'actual_combination is required'}), 400
    
    actual_combination = data['actual_combination']
    
    # Call the crack_safe function
    result = crack_safe(actual_combination)
    
    return jsonify(result), 200


@app.route('/api/crack_safe/stream', methods=['POST'])
@require_api_key
def crack_safe_stream_endpoint():
    """
    POST endpoint to crack a safe combination with real-time progress updates.
    Streams progress as newline-delimited JSON (NDJSON).
    
    Request Body:
        {
            "actual_combination": "08066666"
        }
    
    Response: Stream of JSON objects
        Progress updates:
        {
            "type": "progress",
            "attempts": 10,
            "current_attempt": "0000000000",
            "correct_digits": 2,
            "total_digits": 10
        }
        
        Final result:
        {
            "type": "complete",
            "attempts": 55,
            "time_taken": 12.34
        }
    """
    data = request.get_json()
    
    if not data or 'actual_combination' not in data:
        return jsonify({'error': 'actual_combination is required'}), 400
    
    actual_combination = data['actual_combination']
    
    def generate():
        """Generator function that yields progress updates"""
        try:
            for update in crack_safe_streaming(actual_combination):
                yield json.dumps(update) + '\n'
        except Exception as e:
            yield json.dumps({'type': 'error', 'message': str(e)}) + '\n'
    
    return Response(
        generate(),
        mimetype='application/x-ndjson',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
