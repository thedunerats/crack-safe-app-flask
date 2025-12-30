import pytest
import json
import os
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_headers():
    """Headers with valid API key"""
    return {
        'Content-Type': 'application/json',
        'X-API-Key': os.environ.get('API_KEY', 'dev-safe-cracker-key-12345')
    }


class TestHomeEndpoint:
    """Test suite for the home endpoint (GET /)."""
    
    def test_home_endpoint_success(self, client):
        """Test that the home endpoint returns success."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_home_endpoint_response_structure(self, client):
        """Test that the home endpoint returns the correct structure."""
        response = client.get('/')
        data = json.loads(response.data)
        
        assert 'status' in data
        assert 'message' in data
        assert 'endpoints' in data
        assert data['status'] == 'connected'
        assert data['message'] == 'Safe Cracking API is running'
    
    def test_home_endpoint_lists_crack_safe(self, client):
        """Test that the home endpoint lists the crack_safe endpoint."""
        response = client.get('/')
        data = json.loads(response.data)
        
        assert 'crack_safe' in data['endpoints']
        assert '/api/crack_safe/' in data['endpoints']['crack_safe']


class TestCrackSafeEndpoint:
    """Test suite for the crack_safe endpoint (POST /api/crack_safe/)."""
    
    def test_crack_safe_endpoint_success(self, client, valid_headers):
        """Test successful safe cracking request."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'actual_combination': '1234'}),
            headers=valid_headers
        )
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_crack_safe_endpoint_response_structure(self, client, valid_headers):
        """Test that the response has the correct structure."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'actual_combination': '0000'}),
            headers=valid_headers
        )
        data = json.loads(response.data)
        
        assert 'attempts' in data
        assert 'time_taken' in data
        assert isinstance(data['attempts'], int)
        assert isinstance(data['time_taken'], (int, float))
    
    def test_crack_safe_endpoint_missing_combination(self, client, valid_headers):
        """Test request without actual_combination field."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({}),
            headers=valid_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'actual_combination is required' in data['error']
    
    def test_crack_safe_endpoint_no_json_body(self, client, valid_headers):
        """Test request without JSON body."""
        response = client.post('/api/crack_safe/', headers=valid_headers)
        
        # Flask returns 400 for invalid JSON
        assert response.status_code == 400
        # Response may be HTML error page, so just verify it's a bad request

    
    def test_crack_safe_endpoint_with_simple_combination(self, client, valid_headers):
        """Test cracking a simple combination."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'actual_combination': '0000'}),
            headers=valid_headers
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['attempts'] > 0
        assert data['time_taken'] >= 0
    
    def test_crack_safe_endpoint_with_complex_combination(self, client, valid_headers):
        """Test cracking a more complex combination."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'actual_combination': '08066666'}),
            headers=valid_headers
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['attempts'] > 0
        assert data['attempts'] <= 80  # Maximum expected attempts
        assert data['time_taken'] >= 0
    
    def test_crack_safe_endpoint_with_single_digit(self, client, valid_headers):
        """Test cracking a single digit combination."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'actual_combination': '5'}),
            headers=valid_headers
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['attempts'] <= 10
        assert data['time_taken'] >= 0
    
    def test_crack_safe_endpoint_invalid_json(self, client, valid_headers):
        """Test request with invalid JSON."""
        response = client.post(
            '/api/crack_safe/',
            data='invalid json',
            headers=valid_headers
        )
        
        assert response.status_code == 400
    
    def test_crack_safe_endpoint_wrong_field_name(self, client, valid_headers):
        """Test request with wrong field name."""
        response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'combination': '1234'}),
            headers=valid_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
