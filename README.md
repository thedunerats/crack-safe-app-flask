# 🔐 Safe Cracking App - Flask Backend

A fun and interactive safe cracking game built with Flask! Test your code-breaking skills by trying to crack a 4-digit combination lock with limited attempts.

## 🎮 Game Features

- **4-digit combination lock** with digits ranging from 0-9
- **5 attempts** to crack the safe
- **Color-coded feedback** after each attempt:
  - 🟢 **Green (Correct)**: Right digit in the right position
  - 🟠 **Orange (Present)**: Right digit but wrong position
  - ⚪ **Gray (Absent)**: Digit not in the combination
- **Attempt history** tracking
- **Beautiful, responsive UI** with gradient design
- **Reset functionality** to start a new game

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/thedunerats/crack-safe-app-flask.git
cd crack-safe-app-flask
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 📚 API Documentation

### GET `/api/safe`
Get the current status of the safe.

**Response:**
```json
{
  "is_locked": true,
  "attempts_remaining": 5,
  "max_attempts": 5,
  "combination_length": 4,
  "max_digit": 9
}
```

### POST `/api/safe/attempt`
Submit an attempt to crack the safe.

**Request Body:**
```json
{
  "combination": [1, 2, 3, 4]
}
```

**Response (Incorrect):**
```json
{
  "success": true,
  "unlocked": false,
  "message": "Incorrect combination. 4 attempts remaining.",
  "attempts_remaining": 4,
  "feedback": [
    {"position": 0, "digit": 1, "status": "absent"},
    {"position": 1, "digit": 2, "status": "present"},
    {"position": 2, "digit": 3, "status": "correct"},
    {"position": 3, "digit": 4, "status": "absent"}
  ],
  "game_over": false
}
```

**Response (Correct):**
```json
{
  "success": true,
  "unlocked": true,
  "message": "Congratulations! You cracked the safe!",
  "attempts_remaining": 3,
  "feedback": [...]
}
```

### POST `/api/safe/reset`
Reset the safe with a new random combination.

**Response:**
```json
{
  "success": true,
  "message": "Safe has been reset with a new combination.",
  "attempts_remaining": 5,
  "combination_length": 4,
  "max_digit": 9
}
```

### GET `/api/safe/reveal` (Debug Only)
Reveal the current combination for testing purposes.

**Response:**
```json
{
  "combination": [4, 5, 0, 6],
  "note": "This endpoint is for debugging only and should be removed in production"
}
```

## 🎯 How to Play

1. Enter a 4-digit combination (each digit from 0-9)
2. Click "Try Combination" to submit your attempt
3. Observe the color-coded feedback:
   - Green boxes show correct digits in correct positions
   - Orange boxes show correct digits in wrong positions
   - Gray boxes show digits not in the combination
4. Use the feedback to refine your next guess
5. Crack the safe within 5 attempts to win!
6. Click "Reset Safe" to start a new game with a different combination

## 🏗️ Project Structure

```
crack-safe-app-flask/
├── app.py                 # Main Flask application with API endpoints
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend HTML with CSS and JavaScript
└── README.md             # Project documentation
```

## 🛠️ Technologies Used

- **Backend**: Flask 3.0.0
- **CORS**: Flask-CORS 4.0.0
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Security**: Python's secrets module for cryptographically secure random numbers

## 🔒 Security Notes

- The `/api/safe/reveal` endpoint should be removed in production
- Current implementation stores game state in memory (single-user)
- For production multi-user support, implement session management or database storage
- Consider adding rate limiting for the attempt endpoint

## 📝 License

This project is open source and available for educational purposes.

## 🎨 Screenshots

### Initial State
The safe is locked and ready to be cracked with 5 attempts available.

### During Gameplay
Color-coded feedback helps you deduce the correct combination.

### Success!
Congratulations screen when you successfully crack the safe!
