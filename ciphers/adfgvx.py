"""
ADFGVX cipher implementation.
A combination of a substitution cipher using a Polybius square
followed by a columnar transposition.
"""

import string
import random


def create_polybius_square(keyword: str = '') -> str:
    """
    Create a Polybius square with optional keyword.
    Uses A-Z and 0-9 as the character set.
    """
    # Create character set (A-Z + 0-9)
    chars = string.ascii_uppercase + string.digits
    
    # If keyword provided, remove duplicates and add remaining chars
    if keyword:
        keyword = keyword.upper()
        # Remove duplicates while preserving order
        seen = set()
        square = ''.join(c for c in keyword if c in chars and not (c in seen or seen.add(c)))
        # Add remaining characters
        square += ''.join(c for c in chars if c not in square)
    else:
        # Use default ordering if no keyword
        square = chars
        
    return square


def encrypt(plaintext: str, polybius_key: str = '', columnar_key: str = '') -> str:
    """
    Encrypt text using ADFGVX cipher.
    
    Args:
        plaintext: Text to encrypt
        polybius_key: Optional key for Polybius square arrangement
        columnar_key: Key for columnar transposition
    """
    if not columnar_key:
        return plaintext
        
    # Step 1: Create Polybius square
    square = create_polybius_square(polybius_key)
    substitution_chars = 'ADFGVX'
    
    # Step 2: Convert text to ADFGVX representation
    intermediate = []
    for char in plaintext.upper():
        if char in square:
            pos = square.index(char)
            row, col = divmod(pos, 6)
            intermediate.append(substitution_chars[row] + substitution_chars[col])
    
    intermediate_text = ''.join(intermediate)
    
    # Step 3: Apply columnar transposition
    # Prepare columns
    num_cols = len(columnar_key)
    num_rows = (len(intermediate_text) + num_cols - 1) // num_cols
    grid = [[''] * num_cols for _ in range(num_rows)]
    
    # Fill grid
    pos = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if pos < len(intermediate_text):
                grid[row][col] = intermediate_text[pos]
                pos += 1
                
    # Sort columns by key
    col_order = sorted(range(num_cols), key=lambda x: columnar_key[x])
    
    # Read off columns in order
    result = []
    for col in col_order:
        for row in range(num_rows):
            if grid[row][col]:
                result.append(grid[row][col])
                
    return ''.join(result)


def decrypt(ciphertext: str, polybius_key: str = '', columnar_key: str = '') -> str:
    """
    Decrypt text using ADFGVX cipher.
    
    Args:
        ciphertext: Text to decrypt
        polybius_key: Optional key for Polybius square arrangement
        columnar_key: Key for columnar transposition
    """
    if not columnar_key:
        return ciphertext
        
    # Step 1: Reverse columnar transposition
    num_cols = len(columnar_key)
    num_rows = (len(ciphertext) + num_cols - 1) // num_cols
    
    # Calculate column lengths (last row might be incomplete)
    col_lengths = [num_rows] * num_cols
    short_cols = num_cols * num_rows - len(ciphertext)
    for i in sorted(range(num_cols), key=lambda x: columnar_key[x])[num_cols-short_cols:]:
        col_lengths[i] -= 1
        
    # Create inverse column order mapping
    col_order = sorted(range(num_cols), key=lambda x: columnar_key[x])
    inverse_order = [0] * num_cols
    for i, col in enumerate(col_order):
        inverse_order[col] = i
        
    # Read columns back into grid
    grid = [[''] * num_cols for _ in range(num_rows)]
    pos = 0
    for col in range(num_cols):
        orig_col = inverse_order[col]
        for row in range(col_lengths[orig_col]):
            if pos < len(ciphertext):
                grid[row][orig_col] = ciphertext[pos]
                pos += 1
                
    # Read off rows to get intermediate text
    intermediate = []
    for row in grid:
        intermediate.extend(ch for ch in row if ch)
    intermediate_text = ''.join(intermediate)
    
    # Step 2: Create Polybius square
    square = create_polybius_square(polybius_key)
    substitution_chars = 'ADFGVX'
    
    # Step 3: Convert ADFGVX pairs back to letters
    result = []
    for i in range(0, len(intermediate_text), 2):
        if i + 1 < len(intermediate_text):
            row = substitution_chars.index(intermediate_text[i])
            col = substitution_chars.index(intermediate_text[i + 1])
            pos = row * 6 + col
            if pos < len(square):
                result.append(square[pos])
                
    return ''.join(result)