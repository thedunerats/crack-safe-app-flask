import time


def count_correct_digits(attempt, actual):
    """
    Count how many digits in the attempt match the actual combination at the same position.
    
    Args:
        attempt (str): The attempted combination
        actual (str): The actual combination
    
    Returns:
        int: Number of digits that match at the same position
    """
    return sum(1 for i in range(len(attempt)) if i < len(actual) and attempt[i] == actual[i])


def crack_safe(actual_combination, progress_callback=None):
    """
    Attempts to crack a safe using an intelligent digit-by-digit approach.
    Uses feedback about correct digit positions to efficiently find the combination.
    
    Args:
        actual_combination (str): The actual combination to crack (e.g., '08066666')
        progress_callback (callable, optional): Function to call with progress updates.
            Called with dict: {'attempts': int, 'current_attempt': str, 'correct_digits': int}
    
    Returns:
        dict: A dictionary containing:
            - attempts (int): Number of combination attempts needed
            - time_taken (float): Time taken in milliseconds
    """
    start_time = time.time()
    attempts = 0
    
    combination_length = len(actual_combination)
    cracked_combination = ['0'] * combination_length
    
    print(f"\n🔓 Starting safe cracking process...")
    print(f"   Target combination length: {combination_length} digits\n")
    
    # Crack digit by digit from left to right
    for position in range(combination_length):
        best_digit = '0'
        best_score = 0
        
        # Try each digit 0-9 at the current position
        for digit in '0123456789':
            attempts += 1
            cracked_combination[position] = digit
            current_attempt = ''.join(cracked_combination)
            
            # Count how many digits are correct
            correct_digits = count_correct_digits(current_attempt, actual_combination)
            
            # Log progress every 10 attempts
            if attempts % 10 == 0:
                print(f"   Attempt {attempts}: Testing '{current_attempt}' → {correct_digits}/{combination_length} digits correct")
                if progress_callback:
                    progress_callback({
                        'attempts': attempts,
                        'current_attempt': current_attempt,
                        'correct_digits': correct_digits,
                        'total_digits': combination_length
                    })
            
            # If this digit gives us more correct positions, it's likely the right one
            if correct_digits > best_score:
                best_score = correct_digits
                best_digit = digit
            
            # If we've cracked it completely, we're done!
            if current_attempt == actual_combination:
                end_time = time.time()
                time_taken_seconds = end_time - start_time
                time_taken_ms = time_taken_seconds * 1000
                
                print(f"\n✅ Safe cracked successfully!")
                print(f"   Final combination: {current_attempt}")
                print(f"   Total attempts: {attempts}")
                print(f"   Time taken: {round(time_taken_ms, 2)}ms\n")
                
                return {
                    'attempts': attempts,
                    'time_taken': round(time_taken_ms, 2)
                }
        
        # Lock in the best digit for this position
        cracked_combination[position] = best_digit
        print(f"   🔒 Position {position + 1} locked: '{best_digit}' (Current: {''.join(cracked_combination)})\n")
    
    # Final result
    end_time = time.time()
    time_taken_seconds = end_time - start_time
    time_taken_ms = time_taken_seconds * 1000
    
    return {
        'attempts': attempts,
        'time_taken': round(time_taken_ms, 2)
    }


def crack_safe_streaming(actual_combination):
    """
    Generator version of crack_safe that yields progress updates.
    Yields progress every 10 attempts and final result at the end.
    
    Args:
        actual_combination (str): The actual combination to crack
    
    Yields:
        dict: Progress updates with 'type': 'progress' or 'complete'
    """
    progress_data = []
    
    def progress_callback(data):
        progress_data.append(data)
    
    # Run the cracking algorithm with progress callback
    result = crack_safe(actual_combination, progress_callback=progress_callback)
    
    # Yield all progress updates
    for progress in progress_data:
        yield {
            'type': 'progress',
            'attempts': progress['attempts'],
            'current_attempt': progress['current_attempt'],
            'correct_digits': progress['correct_digits'],
            'total_digits': progress['total_digits']
        }
    
    # Yield final result
    yield {
        'type': 'complete',
        'attempts': result['attempts'],
        'time_taken': result['time_taken']
    }
