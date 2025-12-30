from flask import Flask, request, jsonify
from services.safe_cracker import crack_safe

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Default GET endpoint to verify the app is running.
    """
    return jsonify({
        'status': 'connected',
        'message': 'Safe Cracking API is running',
        'endpoints': {
            'crack_safe': '/api/crack_safe/ [POST]'
        }
    }), 200


@app.route('/api/crack_safe/', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
