# Safe Cracking Flask App

A Flask-based REST API that simulates safe cracking using an intelligent digit-by-digit algorithm.

## Project Structure

```
crack-safe-app-flask/
├── src/
│   ├── app.py                     # Main Flask application
│   └── services/
│       └── safe_cracker.py        # Safe cracking algorithm
├── tests/
│   ├── test_app.py                # Unit tests for Flask endpoints
│   └── test_safe_cracker.py       # Unit tests for safe cracker logic
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Features

- **Intelligent Cracking Algorithm**: Cracks safes digit-by-digit instead of brute force
- **Progress Logging**: Logs attempts and correct digit counts during cracking
- **REST API**: Simple POST endpoint to crack safe combinations
- **Fast Performance**: Maximum ~80 attempts for 8-digit combinations (vs. 100M brute force)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python src/app.py
   ```

2. **The server will start on** `http://localhost:5000`

3. **Test the connection**:
   ```bash
   curl http://localhost:5000/
   ```

## API Endpoints

### GET `/`
Health check endpoint to verify the API is running.

**Response:**
```json
{
    "status": "connected",
    "message": "Safe Cracking API is running",
    "endpoints": {
        "crack_safe": "/api/crack_safe/ [POST]"
    }
}
```

### POST `/api/crack_safe/`
Crack a safe combination.

**Request Body:**
```json
{
    "actual_combination": "08066666"
}
```

**Response:**
```json
{
    "attempts": 73,
    "time_taken": 5.23
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/crack_safe/ \
  -H "Content-Type: application/json" \
  -d "{\"actual_combination\": \"08066666\"}"
```

## Running Tests

### Install Test Dependencies

Test dependencies are included in `requirements.txt`. If you've already run `pip install -r requirements.txt`, you're all set!

If you need to install only test dependencies:
```bash
pip install pytest pytest-cov
```

### Run All Tests

Run all unit tests:
```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

This will show which lines of code are covered by tests.

### Run Specific Test Files

Test only the safe cracker logic:
```bash
pytest tests/test_safe_cracker.py
```

Test only the Flask endpoints:
```bash
pytest tests/test_app.py
```

### Run Specific Test Classes or Methods

Run a specific test class:
```bash
pytest tests/test_safe_cracker.py::TestCrackSafe
```

Run a specific test method:
```bash
pytest tests/test_app.py::TestCrackSafeEndpoint::test_crack_safe_endpoint_success
```

## Test Coverage

The project includes comprehensive unit tests:

- **test_safe_cracker.py**: Tests for the core safe cracking algorithm
  - Tests `count_correct_digits()` function
  - Tests `crack_safe()` function with various combinations
  - Tests edge cases (all zeros, all nines, single digits)
  
- **test_app.py**: Tests for Flask API endpoints
  - Tests GET `/` health check endpoint
  - Tests POST `/api/crack_safe/` endpoint
  - Tests error handling (missing fields, invalid JSON)
  - Tests response structures and status codes

## How the Algorithm Works

The safe cracking algorithm uses a smart digit-by-digit approach:

1. **Initialize**: Start with all zeros (e.g., `00000000` for 8 digits)
2. **For each digit position** (left to right):
   - Try digits 0-9 at that position
   - Count how many total digits are correct
   - Select the digit that maximizes correct positions
3. **Result**: Combination is cracked in ~10 attempts per digit

**Example for combination `08066666`:**
- Position 1: Try `0-9`, find `0` is correct → `0???????`
- Position 2: Try `0-9`, find `8` is correct → `08??????`
- Continue for all 8 positions
- Total: ~73 attempts (vs. 8,066,667 for brute force)

## Development

### Project Structure Decisions

- **src/**: Contains all source code
- **tests/**: Contains all unit tests (mirrors src/ structure)
- **services/**: Business logic separated from Flask routes

### Adding New Features

1. Add functionality to appropriate module in `src/`
2. Write corresponding tests in `tests/`
3. Run tests to ensure nothing breaks
4. Update this README if adding new endpoints or features

## License

This project is for educational purposes.
