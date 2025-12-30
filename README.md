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
- **Real-time Progress Updates**: Watch the cracking process live with attempt counter
- **Progress Logging**: Logs attempts and correct digit counts during cracking
- **REST API**: Simple POST endpoint to crack safe combinations
- **Streaming Endpoint**: Real-time progress updates every 10 attempts via NDJSON streaming
- **Fast Performance**: Maximum ~100 attempts for 10-digit combinations
- **Angular Frontend**: Modern, responsive UI with form validation
- **Live Counter Display**: See current attempts, testing combination, and progress bar
- **Real-time Results**: Displays cracking attempts and time taken
- **CORS Enabled**: Frontend and backend communicate seamlessly
- **API Authentication**: Secure API key authentication to protect endpoints

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

4. **Install dependencies** (including flask-cors and python-dotenv):
   ```bash
   pip install -r requirements.txt
   ```
   
   **Important:** Make sure flask-cors and python-dotenv install successfully. If you get errors, try:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```
   
   Then edit `.env` and set your API key:
   ```bash
   API_KEY=your-secure-api-key-here
   ```
   
   **Generate a secure API key** (optional but recommended):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
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

3. **Configure API key** (must match backend):
   
   Edit `client/src/environments/environment.ts` and set the API key:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:5000',
     apiKey: 'your-secure-api-key-here'  // Must match server/.env API_KEY
   };
   ```
   
   **Important:** The API key in the frontend must exactly match the `API_KEY` in your backend `.env` file.

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
3. **Watch real-time progress** as the safe is being cracked:
   - Current attempt counter updates every 10 attempts
   - See the combination being tested
   - Progress bar shows how many digits are correct
4. View the final results showing:
   - Total number of attempts needed
   - Time taken in milliseconds
5. Click "🔄 Reset" to try another combination

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
        "crack_safe": "/api/crack_safe/ [POST] - Requires API Key",
        "crack_safe_stream": "/api/crack_safe/stream [POST] - Requires API Key (Real-time updates)"
    }
}
```

### POST `/api/crack_safe/`
Crack a safe combination. **Requires API Key authentication.**

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Request Body:**
```json
{
    "actual_combination": "1234567890"
}
```

**Response:**
```json
{
    "attempts": 55,
    "time_taken": 5.23
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/crack_safe/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d "{\"actual_combination\": \"1234567890\"}"
```

### POST `/api/crack_safe/stream` ✨ NEW
Crack a safe combination with **real-time progress updates**. **Requires API Key authentication.**

Returns a stream of newline-delimited JSON (NDJSON) with progress updates every 10 attempts.

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Request Body:**
```json
{
    "actual_combination": "1234567890"
}
```

**Response Stream (NDJSON):**
```json
{"type": "progress", "attempts": 10, "current_attempt": "1000000000", "correct_digits": 1, "total_digits": 10}
{"type": "progress", "attempts": 20, "current_attempt": "1200000000", "correct_digits": 2, "total_digits": 10}
{"type": "progress", "attempts": 30, "current_attempt": "1230000000", "correct_digits": 3, "total_digits": 10}
...
{"type": "complete", "attempts": 55, "time_taken": 5.23}
```

**Progress Update Format:**
- `type`: Always "progress" for intermediate updates
- `attempts`: Current number of attempts made
- `current_attempt`: The combination currently being tested
- `correct_digits`: How many digits are correct in current position
- `total_digits`: Total digits in the combination (always 10)

**Complete Update Format:**
- `type`: Always "complete" for final result
- `attempts`: Total attempts needed to crack the safe
- `time_taken`: Time taken in milliseconds

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/crack_safe/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d "{\"actual_combination\": \"1234567890\"}" \
  --no-buffer
```

**Example using Python:**
```python
import requests
import json

url = "http://localhost:5000/api/crack_safe/stream"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "your-api-key-here"
}
data = {"actual_combination": "1234567890"}

response = requests.post(url, json=data, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        update = json.loads(line)
        if update['type'] == 'progress':
            print(f"Progress: {update['attempts']} attempts, {update['correct_digits']}/{update['total_digits']} correct")
        elif update['type'] == 'complete':
            print(f"Complete! {update['attempts']} total attempts in {update['time_taken']}ms")
```

**Authentication Errors:**

Missing API Key (401):
```json
{
    "error": "Unauthorized: API key required",
    "message": "Please provide API key in X-API-Key header"
}
```

Invalid API Key (401):
```json
{
    "error": "Unauthorized: Invalid API key"
}
```

## Running Tests

The project includes comprehensive test suites for both backend (Python/pytest) and frontend (Angular/Jasmine).

**Test Summary:**
- ✅ **Backend**: 39 Python tests (Flask endpoints, authentication, safe cracker logic, streaming)
- ✅ **Frontend**: 40 Angular tests (service, component, form validation, progress tracking)
- ✅ **Total**: 79 comprehensive unit tests

### Backend Tests (Python/pytest)

All test commands should be run from the `server/` directory.

#### Install Test Dependencies

Test dependencies are included in `requirements.txt`. If you've already run `pip install -r requirements.txt`, you're all set!

#### Run All Backend Tests

```bash
cd server
pytest
```

#### Run Tests with Verbose Output

```bash
pytest -v
```

#### Run Tests with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

This will show which lines of code are covered by tests.

#### Run Specific Test Files

Test only the safe cracker logic:
```bash
pytest tests/services/test_safe_cracker.py
```

Test only the Flask endpoints:
```bash
pytest tests/test_app.py
```

Test only authentication:
```bash
pytest tests/test_authentication.py
```

Test only streaming functionality:
```bash
pytest tests/test_streaming.py
```

#### Run Specific Test Classes or Methods

Run a specific test class:
```bash
pytest tests/services/test_safe_cracker.py::TestCrackSafe
```

Run a specific test method:
```bash
pytest tests/test_authentication.py::TestAuthentication::test_crack_safe_with_valid_api_key
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

- **test_authentication.py**: Tests for API authentication
  - Tests API key validation
  - Tests missing/invalid API key scenarios
  - Tests authentication doesn't break existing functionality
  - Tests case sensitivity and edge cases
  - Tests multiple requests with same key
  - 13 comprehensive test cases

- **test_streaming.py**: Tests for real-time streaming functionality ✨ NEW
  - Tests `crack_safe_streaming()` generator function
  - Tests streaming endpoint returns NDJSON format
  - Tests progress updates occur every 10 attempts
  - Tests authentication on streaming endpoint
  - Tests streaming with various combinations
  - Tests progress shows increasing attempts
  - Tests streaming final result matches regular endpoint
  - 10 comprehensive streaming test cases

### Frontend Tests (Angular/Jasmine)

The Angular client includes unit tests for services and components:

- **safe-cracker.service.spec.ts**: Tests for the SafeCrackerService
  - Tests HTTP requests to backend API
  - Tests API key inclusion in headers
  - Tests error handling
  - Tests streaming functionality with progress callbacks
  - Tests NDJSON parsing
  - 12 comprehensive service tests

- **safe-cracker.component.spec.ts**: Tests for the SafeCrackerComponent
  - Tests form validation (10 digits, numeric only)
  - Tests form submission with valid/invalid data
  - Tests loading states
  - Tests progress tracking during cracking
  - Tests reset functionality
  - Tests UI state management
  - 25+ comprehensive component tests

### Run Frontend Tests

Navigate to the client directory and run:

```bash
cd client

# Run tests once
ng test --watch=false --browsers=ChromeHeadless

# Run tests in watch mode (for development)
ng test

# Run tests with code coverage
ng test --code-coverage --watch=false --browsers=ChromeHeadless
```

**View Coverage Report:**
After running with `--code-coverage`, open `client/coverage/index.html` in your browser to see detailed coverage reports.

**Test Results:**
- Service Tests: 12 tests covering API communication and streaming
- Component Tests: 25+ tests covering form validation, submission, and UI state
- Total Frontend Tests: 37+ comprehensive unit tests

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
- **Secure API Calls**: Automatically includes API key in all requests

## Security

### API Key Authentication

The application uses **API key authentication** which is generic and location-independent:

✅ **Works from any IP address** - No IP-based restrictions  
✅ **Works from any domain** - When properly configured  
✅ **Works in any environment** - Development, staging, production  
✅ **Works globally** - No geographic restrictions  

#### How It Works

1. **Backend Protection**: All `/api/crack_safe/` requests require a valid API key in the `X-API-Key` header
2. **Environment-based Configuration**: API keys are stored in `.env` files (not committed to git)
3. **Frontend Integration**: The Angular app automatically includes the API key in all API requests
4. **CORS Control**: Origins are configurable per environment via `ALLOWED_ORIGINS`

#### Production Deployment

When deploying to production:

1. **Generate a strong API key**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update backend** (`server/.env`):
   ```bash
   API_KEY=your-secure-production-key
   ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

3. **Update frontend** (`client/src/environments/environment.prod.ts`):
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://your-api-domain.com',
     apiKey: 'your-secure-production-key'  // Same as backend
   };
   ```

4. **Both frontend and backend must use the same API key**

### Security Best Practices

- **Never commit API keys**: The `.env` file is in `.gitignore`
- **Use strong API keys**: Generate random keys with `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- **Different keys for environments**: Use different API keys for development, testing, and production
- **HTTPS in production**: Always use HTTPS when deploying to production
- **CORS configuration**: Only allow requests from trusted origins

### Changing API Keys

To change your API key:

1. **Backend**: Update `API_KEY` in `server/.env`
2. **Frontend**: Update `apiKey` in `client/src/environments/environment.ts`
3. **Restart both servers** for changes to take effect

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
