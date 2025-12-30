import pytest
import os
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Set test API key
    os.environ['API_KEY'] = 'test-api-key-12345'
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Clean up
    if 'API_KEY' in os.environ:
        del os.environ['API_KEY']


@pytest.fixture
def valid_headers():
    """Return valid authentication headers."""
    return {'X-API-Key': 'test-api-key-12345'}


@pytest.fixture
def invalid_headers():
    """Return invalid authentication headers."""
    return {'X-API-Key': 'wrong-api-key'}


class TestAuthentication:
    """Test suite for API authentication."""
    
    def test_home_endpoint_no_auth_required(self, client):
        """Test that home endpoint works without authentication."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'connected'
    
    def test_crack_safe_without_api_key(self, client):
        """Test that crack_safe endpoint rejects requests without API key."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers={}
        )
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'API key required' in data['error'] or 'API key required' in data.get('message', '')
    
    def test_crack_safe_with_invalid_api_key(self, client, invalid_headers):
        """Test that crack_safe endpoint rejects requests with invalid API key."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers=invalid_headers
        )
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid API key' in data['error']
    
    def test_crack_safe_with_valid_api_key(self, client, valid_headers):
        """Test that crack_safe endpoint accepts requests with valid API key."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '0000000000'},
            headers=valid_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'attempts' in data
        assert 'time_taken' in data
    
    def test_api_key_case_sensitive(self, client):
        """Test that API key validation is case-sensitive."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers={'X-API-Key': 'TEST-API-KEY-12345'}  # Wrong case
        )
        assert response.status_code == 401
    
    def test_missing_api_key_header(self, client):
        """Test response when X-API-Key header is missing entirely."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 401
        data = response.get_json()
        assert 'Unauthorized' in data['error']
    
    def test_empty_api_key(self, client):
        """Test that empty API key is rejected."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers={'X-API-Key': ''}
        )
        assert response.status_code == 401
    
    def test_api_key_with_spaces(self, client):
        """Test that API key with extra spaces doesn't match."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers={'X-API-Key': ' test-api-key-12345 '}
        )
        assert response.status_code == 401
    
    def test_no_api_key_configured(self, client):
        """Test server response when API key is not configured."""
        # Remove API key from environment
        if 'API_KEY' in os.environ:
            del os.environ['API_KEY']
        
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers={'X-API-Key': 'any-key'}
        )
        assert response.status_code == 500
        data = response.get_json()
        assert 'configuration error' in data['error'].lower()
        
        # Restore API key for other tests
        os.environ['API_KEY'] = 'test-api-key-12345'
    
    def test_valid_request_with_all_fields(self, client, valid_headers):
        """Test complete valid request with authentication and proper payload."""
        response = client.post(
            '/api/crack_safe/',
            json={'actual_combination': '1234567890'},
            headers=valid_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data['attempts'], int)
        assert isinstance(data['time_taken'], (int, float))
        assert data['attempts'] > 0
        assert data['time_taken'] >= 0
    
    def test_authentication_preserves_error_handling(self, client, valid_headers):
        """Test that authentication doesn't break existing error handling."""
        # Test with missing combination field
        response = client.post(
            '/api/crack_safe/',
            json={},
            headers=valid_headers
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'actual_combination is required' in data['error']
    
    def test_multiple_requests_same_key(self, client, valid_headers):
        """Test that the same API key works for multiple requests."""
        for _ in range(3):
            response = client.post(
                '/api/crack_safe/',
                json={'actual_combination': '0000000000'},
                headers=valid_headers
            )
            assert response.status_code == 200
