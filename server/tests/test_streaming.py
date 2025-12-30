import pytest
import json
from src.app import app
from src.services.safe_cracker import crack_safe_streaming


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_headers():
    """Headers with valid API key"""
    import os
    return {
        'Content-Type': 'application/json',
        'X-API-Key': os.environ.get('API_KEY', 'dev-safe-cracker-key-12345')
    }


class TestStreaming:
    """Test cases for streaming functionality"""
    
    def test_crack_safe_streaming_generator(self):
        """Test that crack_safe_streaming yields progress and final result"""
        combination = '1234567890'
        updates = list(crack_safe_streaming(combination))
        
        # Should have at least one progress update and one complete update
        assert len(updates) > 1
        
        # All updates except last should be progress updates
        for update in updates[:-1]:
            assert update['type'] == 'progress'
            assert 'attempts' in update
            assert 'current_attempt' in update
            assert 'correct_digits' in update
            assert 'total_digits' in update
        
        # Last update should be complete
        final_update = updates[-1]
        assert final_update['type'] == 'complete'
        assert 'attempts' in final_update
        assert 'time_taken' in final_update
    
    def test_streaming_endpoint_with_valid_key(self, client, valid_headers):
        """Test streaming endpoint returns NDJSON stream"""
        response = client.post(
            '/api/crack_safe/stream',
            data=json.dumps({'actual_combination': '0123456789'}),
            headers=valid_headers
        )
        
        assert response.status_code == 200
        assert response.content_type == 'application/x-ndjson'
        
        # Parse NDJSON response
        lines = response.data.decode('utf-8').strip().split('\n')
        updates = [json.loads(line) for line in lines if line]
        
        # Should have multiple updates
        assert len(updates) > 1
        
        # Check progress updates
        progress_updates = [u for u in updates if u['type'] == 'progress']
        assert len(progress_updates) > 0
        
        # Check final update
        complete_updates = [u for u in updates if u['type'] == 'complete']
        assert len(complete_updates) == 1
        
        final = complete_updates[0]
        assert final['attempts'] > 0
        assert final['time_taken'] > 0
    
    def test_streaming_endpoint_without_api_key(self, client):
        """Test streaming endpoint requires API key"""
        response = client.post(
            '/api/crack_safe/stream',
            data=json.dumps({'actual_combination': '0123456789'}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        assert 'API key required' in data['error']
    
    def test_streaming_endpoint_with_invalid_key(self, client):
        """Test streaming endpoint rejects invalid API key"""
        response = client.post(
            '/api/crack_safe/stream',
            data=json.dumps({'actual_combination': '0123456789'}),
            headers={
                'Content-Type': 'application/json',
                'X-API-Key': 'invalid-key'
            }
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid API key' in data['error']
    
    def test_streaming_endpoint_missing_combination(self, client, valid_headers):
        """Test streaming endpoint requires actual_combination"""
        response = client.post(
            '/api/crack_safe/stream',
            data=json.dumps({}),
            headers=valid_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'actual_combination is required' in data['error']
    
    def test_progress_updates_every_10_attempts(self):
        """Test that progress updates are sent approximately every 10 attempts"""
        combination = '5555555555'
        updates = list(crack_safe_streaming(combination))
        
        progress_updates = [u for u in updates if u['type'] == 'progress']
        
        # Check that attempts in progress updates are multiples of 10
        for update in progress_updates:
            assert update['attempts'] % 10 == 0
    
    def test_streaming_with_different_combinations(self, client, valid_headers):
        """Test streaming works with various combinations"""
        test_cases = ['0000000000', '9999999999', '1357924680']
        
        for combination in test_cases:
            response = client.post(
                '/api/crack_safe/stream',
                data=json.dumps({'actual_combination': combination}),
                headers=valid_headers
            )
            
            assert response.status_code == 200
            
            lines = response.data.decode('utf-8').strip().split('\n')
            updates = [json.loads(line) for line in lines if line]
            
            # Should have final complete update
            complete = [u for u in updates if u['type'] == 'complete'][0]
            assert complete['attempts'] > 0
    
    def test_streaming_progress_shows_increasing_attempts(self):
        """Test that progress updates show monotonically increasing attempts"""
        combination = '1234567890'
        updates = list(crack_safe_streaming(combination))
        
        progress_updates = [u for u in updates if u['type'] == 'progress']
        
        # Attempts should be increasing
        for i in range(1, len(progress_updates)):
            assert progress_updates[i]['attempts'] > progress_updates[i-1]['attempts']
    
    def test_streaming_complete_matches_regular_endpoint(self, client, valid_headers):
        """Test that streaming final result matches regular endpoint result"""
        combination = '0123456789'
        
        # Get streaming result
        stream_response = client.post(
            '/api/crack_safe/stream',
            data=json.dumps({'actual_combination': combination}),
            headers=valid_headers
        )
        stream_lines = stream_response.data.decode('utf-8').strip().split('\n')
        stream_updates = [json.loads(line) for line in stream_lines if line]
        stream_final = [u for u in stream_updates if u['type'] == 'complete'][0]
        
        # Get regular result
        regular_response = client.post(
            '/api/crack_safe/',
            data=json.dumps({'actual_combination': combination}),
            headers=valid_headers
        )
        regular_result = json.loads(regular_response.data)
        
        # Attempts should match (time may vary slightly)
        assert stream_final['attempts'] == regular_result['attempts']
