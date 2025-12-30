# Safe Cracking Flask App

A Flask-based REST API that simulates safe cracking using an intelligent digit-by-digit algorithm.

## Project Structure

```
crack-safe-app-flask/
├── client/                        # Angular frontend application
│   ├── src/
│   │   └── app/
│   │       ├── safe-cracker/      # Safe cracker component
│   │       └── services/          # API services
│   └── ...                        # Angular config files
├── server/                        # Backend Flask application
│   ├── src/
│   │   ├── app.py                 # Main Flask application
│   │   └── services/
│   │       └── safe_cracker.py    # Safe cracking algorithm
│   ├── tests/
│   │   ├── test_app.py            # Unit tests for Flask endpoints
│   │   └── services/
│   │       └── test_safe_cracker.py  # Unit tests for safe cracker logic
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                 # Git ignore rules
├── .gitignore                     # Root level git ignore
└── README.md                      # This file
```

## Features

- **Intelligent Cracking Algorithm**: Cracks safes digit-by-digit instead of brute force
- **Progress Logging**: Logs attempts and correct digit counts during cracking
- **REST API**: Simple POST endpoint to crack safe combinations
- **Fast Performance**: Maximum ~100 attempts for 10-digit combinations
- **Angular Frontend**: Modern, responsive UI with form validation
- **Real-time Results**: Displays cracking attempts and time taken
- **CORS Enabled**: Frontend and backend communicate seamlessly

## Installation

### Backend Setup

1. **Navigate to the server directory**:
   ```bash
   cd server
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies** (including flask-cors):
   ```bash
   pip install -r requirements.txt
   ```
   
   **Important:** Make sure flask-cors installs successfully. If you get errors, try:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to the client directory**:
   ```bash
   cd client
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

## Running the Application

### Start the Backend

1. **Navigate to the server folder** (if not already there):
   ```bash
   cd server
   ```

2. **Activate your virtual environment** (if not already activated):
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Verify flask-cors is installed**:
   ```bash
   pip list | grep flask-cors
   ```
   If not installed, run: `pip install flask-cors`

4. **Run the Flask app**:
   ```bash
   python -m src.app
   ```

5. **Backend will start on** `http://localhost:5000`
   
   You should see output like:
   ```
   * Running on http://127.0.0.1:5000
   * Running on http://0.0.0.0:5000
   ```

### Start the Frontend

1. **Open a new terminal and navigate to the client folder**:
   ```bash
   cd client
   ```

2. **Start the Angular development server**:
   ```bash
   ng serve
   ```
   or
   ```bash
   npm start
   ```

3. **Frontend will start on** `http://localhost:4200`

4. **Open your browser** and navigate to `http://localhost:4200`

### Using the Application

1. Enter a 10-digit combination in the input field (e.g., `1234567890`)
2. Click "🔓 Crack Safe" to submit
3. View the results showing:
   - Number of attempts needed
   - Time taken in milliseconds
4. Click "🔄 Reset" to try another combination

### Troubleshooting

**Backend Issues:**

**"ModuleNotFoundError: No module named 'flask_cors'"**
- Solution: Install the package with `pip install flask-cors` or `pip install -r requirements.txt`
- Make sure your virtual environment is activated

**"No module named 'src'"**
- Make sure you're in the `server/` directory when running the command
- Use `python -m src.app` (not `python src/app.py`)

**Port already in use:**
- Another app is using port 5000. Either stop it or change the port in `src/app.py`

**Import errors:**
- Verify your virtual environment is activated
- Confirm all dependencies are installed: `pip list`
- Re-install if needed: `pip install -r requirements.txt`

**Frontend Issues:**
- Ensure Node.js and Angular CLI are installed
- Run `npm install` if you encounter module errors
- Check that the backend is running on `http://localhost:5000`
- Verify CORS is enabled in the Flask app

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

All test commands should be run from the `server/` directory.

### Install Test Dependencies

Test dependencies are included in `requirements.txt`. If you've already run `pip install -r requirements.txt`, you're all set!

### Run All Tests

```bash
cd server
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
pytest tests/services/test_safe_cracker.py
```

Test only the Flask endpoints:
```bash
pytest tests/test_app.py
```

### Run Specific Test Classes or Methods

Run a specific test class:
```bash
pytest tests/services/test_safe_cracker.py::TestCrackSafe
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

**Example for combination `1234567890`:**
- Position 1: Try `0-9`, find `1` is correct → `1?????????`
- Position 2: Try `0-9`, find `2` is correct → `12????????`
- Continue for all 10 positions
- Total: ~55 attempts (vs. 10,000,000,000 for brute force)

## Development

### Project Organization

- **client/src/app/**: Angular frontend components and services
  - **safe-cracker/**: Main component with form and results display
  - **services/**: API service for backend communication
- **server/src/**: All backend source code
- **server/tests/**: All unit tests (mirrors src/ structure)
- **server/src/services/**: Business logic separated from Flask routes

### Frontend Features

The Angular frontend includes:
- **Form Validation**: Ensures exactly 10 numeric digits
- **Real-time Feedback**: Shows validation errors as you type
- **Loading States**: Displays loading indicator during API calls
- **Error Handling**: Graceful error messages for failed requests
- **Results Display**: Beautiful card layout showing attempts and time
- **Responsive Design**: Works on mobile and desktop

### Adding New Backend Features

1. Add functionality to appropriate module in `server/src/`
2. Write corresponding tests in `server/tests/`
3. Run tests to ensure nothing breaks
4. Update this README if adding new endpoints or features

### Adding New Frontend Features

1. Create components in `client/src/app/`
2. Update services in `client/src/app/services/`
3. Test in the browser
4. Update this README if needed

## License

This project is for educational purposes.
