from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import secrets

app = Flask(__name__)
CORS(app)

# Game state stored in memory (in production, use a database or session)
game_state = {
    'combination': None,
    'attempts_remaining': 5,
    'max_attempts': 5,
    'is_locked': True,
    'combination_length': 4,
    'max_digit': 9
}


def initialize_game():
    """Initialize a new safe cracking game with a random combination."""
    game_state['combination'] = [
        secrets.randbelow(game_state['max_digit'] + 1) 
        for _ in range(game_state['combination_length'])
    ]
    game_state['attempts_remaining'] = game_state['max_attempts']
    game_state['is_locked'] = True


def check_combination(attempt):
    """
    Check the attempted combination against the correct one.
    Returns a dict with feedback for each digit.
    """
    if not game_state['combination']:
        return None
    
    feedback = []
    for i, digit in enumerate(attempt):
        if digit == game_state['combination'][i]:
            feedback.append({'position': i, 'digit': digit, 'status': 'correct'})
        elif digit in game_state['combination']:
            feedback.append({'position': i, 'digit': digit, 'status': 'present'})
        else:
            feedback.append({'position': i, 'digit': digit, 'status': 'absent'})
    
    return feedback


@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/api/safe', methods=['GET'])
def get_safe_status():
    """Get the current status of the safe."""
    if not game_state['combination']:
        initialize_game()
    
    return jsonify({
        'is_locked': game_state['is_locked'],
        'attempts_remaining': game_state['attempts_remaining'],
        'max_attempts': game_state['max_attempts'],
        'combination_length': game_state['combination_length'],
        'max_digit': game_state['max_digit']
    })


@app.route('/api/safe/attempt', methods=['POST'])
def attempt_combination():
    """Submit an attempt to crack the safe."""
    if not game_state['combination']:
        initialize_game()
    
    # Check if the safe is already unlocked
    if not game_state['is_locked']:
        return jsonify({
            'success': False,
            'message': 'Safe is already unlocked!'
        }), 400
    
    # Check if there are attempts remaining
    if game_state['attempts_remaining'] <= 0:
        return jsonify({
            'success': False,
            'message': 'No attempts remaining. Please reset the safe.'
        }), 400
    
    # Get the attempted combination from the request
    data = request.get_json()
    if not data or 'combination' not in data:
        return jsonify({
            'success': False,
            'message': 'Missing combination in request'
        }), 400
    
    attempt = data['combination']
    
    # Validate the attempt
    if not isinstance(attempt, list) or len(attempt) != game_state['combination_length']:
        return jsonify({
            'success': False,
            'message': f'Combination must be a list of {game_state["combination_length"]} digits'
        }), 400
    
    # Validate each digit
    for digit in attempt:
        if not isinstance(digit, int) or digit < 0 or digit > game_state['max_digit']:
            return jsonify({
                'success': False,
                'message': f'Each digit must be an integer between 0 and {game_state["max_digit"]}'
            }), 400
    
    # Decrement attempts
    game_state['attempts_remaining'] -= 1
    
    # Check if the combination is correct
    if attempt == game_state['combination']:
        game_state['is_locked'] = False
        return jsonify({
            'success': True,
            'unlocked': True,
            'message': 'Congratulations! You cracked the safe!',
            'attempts_remaining': game_state['attempts_remaining'],
            'feedback': check_combination(attempt)
        })
    
    # Provide feedback on the attempt
    feedback = check_combination(attempt)
    
    return jsonify({
        'success': True,
        'unlocked': False,
        'message': f'Incorrect combination. {game_state["attempts_remaining"]} attempts remaining.',
        'attempts_remaining': game_state['attempts_remaining'],
        'feedback': feedback,
        'game_over': game_state['attempts_remaining'] == 0
    })


@app.route('/api/safe/reset', methods=['POST'])
def reset_safe():
    """Reset the safe with a new combination."""
    initialize_game()
    return jsonify({
        'success': True,
        'message': 'Safe has been reset with a new combination.',
        'attempts_remaining': game_state['attempts_remaining'],
        'combination_length': game_state['combination_length'],
        'max_digit': game_state['max_digit']
    })


@app.route('/api/safe/reveal', methods=['GET'])
def reveal_combination():
    """Reveal the current combination (for debugging/testing)."""
    if not game_state['combination']:
        initialize_game()
    
    return jsonify({
        'combination': game_state['combination'],
        'note': 'This endpoint is for debugging only and should be removed in production'
    })


if __name__ == '__main__':
    # Initialize the game when the app starts
    initialize_game()
    app.run(debug=True, host='0.0.0.0', port=5000)
