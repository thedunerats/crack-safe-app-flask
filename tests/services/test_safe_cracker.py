import pytest
import time
from src.services.safe_cracker import count_correct_digits, crack_safe


class TestCountCorrectDigits:
    """Test suite for count_correct_digits function."""
    
    def test_all_digits_correct(self):
        """Test when all digits match."""
        assert count_correct_digits('12345678', '12345678') == 8
    
    def test_no_digits_correct(self):
        """Test when no digits match."""
        assert count_correct_digits('00000000', '11111111') == 0
    
    def test_some_digits_correct(self):
        """Test when some digits match."""
        assert count_correct_digits('12340000', '12345678') == 4
    
    def test_partial_match_at_end(self):
        """Test when only end digits match."""
        assert count_correct_digits('00005678', '12345678') == 4
    
    def test_single_digit_correct(self):
        """Test when only one digit matches."""
        assert count_correct_digits('10000000', '12345678') == 1
    
    def test_different_lengths(self):
        """Test when strings have different lengths."""
        assert count_correct_digits('123', '12345678') == 3
        assert count_correct_digits('12345678', '123') == 3


class TestCrackSafe:
    """Test suite for crack_safe function."""
    
    def test_crack_safe_simple_combination(self):
        """Test cracking a simple combination."""
        result = crack_safe('0000')
        
        assert 'attempts' in result
        assert 'time_taken' in result
        assert result['attempts'] == 1  # Should find '0000' immediately
        assert result['time_taken'] >= 0
    
    def test_crack_safe_all_zeros(self):
        """Test cracking all zeros (should be immediate)."""
        result = crack_safe('00000000')
        
        assert result['attempts'] == 1
        assert result['time_taken'] >= 0
    
    def test_crack_safe_single_digit(self):
        """Test cracking a single digit combination."""
        result = crack_safe('5')
        
        assert 'attempts' in result
        assert 'time_taken' in result
        assert result['attempts'] <= 10  # Should find within 10 attempts
        assert result['time_taken'] >= 0
    
    def test_crack_safe_medium_combination(self):
        """Test cracking a 4-digit combination."""
        result = crack_safe('1234')
        
        assert 'attempts' in result
        assert 'time_taken' in result
        # Maximum 10 tries per digit * 4 digits = 40 attempts
        assert result['attempts'] <= 40
        assert result['time_taken'] >= 0
    
    def test_crack_safe_long_combination(self):
        """Test cracking an 8-digit combination."""
        result = crack_safe('08066666')
        
        assert 'attempts' in result
        assert 'time_taken' in result
        # Maximum 10 tries per digit * 8 digits = 80 attempts
        assert result['attempts'] <= 80
        assert result['time_taken'] >= 0
    
    def test_crack_safe_all_nines(self):
        """Test cracking a combination with all 9s (worst case per digit)."""
        result = crack_safe('9999')
        
        assert 'attempts' in result
        assert 'time_taken' in result
        # Should find it within 10 * 4 = 40 attempts
        assert result['attempts'] <= 40
        assert result['time_taken'] >= 0
    
    def test_crack_safe_returns_correct_structure(self):
        """Test that the return structure is correct."""
        result = crack_safe('123')
        
        assert isinstance(result, dict)
        assert len(result) == 2
        assert 'attempts' in result
        assert 'time_taken' in result
        assert isinstance(result['attempts'], int)
        assert isinstance(result['time_taken'], float)
    
    def test_crack_safe_attempts_positive(self):
        """Test that attempts is always positive."""
        result = crack_safe('42')
        
        assert result['attempts'] > 0
    
    def test_crack_safe_time_taken_reasonable(self):
        """Test that time_taken is reasonable."""
        result = crack_safe('555')
        
        # Should complete in under 1 second for small combinations
        assert result['time_taken'] < 1000  # Less than 1 second (1000ms)
