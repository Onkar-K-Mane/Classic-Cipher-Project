"""
Columnar Transposition cipher implementation.
A transposition cipher that rearranges text into columns based on a key.
"""

def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt text using Columnar Transposition cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Keyword for determining column order
    """
    if not key:
        return plaintext
        
    # Remove spaces and convert to uppercase for consistent encryption
    plaintext = ''.join(plaintext.split()).upper()
    
    # Calculate dimensions
    num_cols = len(key)
    num_rows = (len(plaintext) + num_cols - 1) // num_cols
    
    # Create grid and fill with text
    grid = [[''] * num_cols for _ in range(num_rows)]
    pos = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if pos < len(plaintext):
                grid[row][col] = plaintext[pos]
                pos += 1
                
    # Get column order based on key
    col_order = sorted(range(num_cols), key=lambda x: key[x])
    
    # Read off columns in order determined by key
    result = []
    for col in col_order:
        for row in range(num_rows):
            if grid[row][col]:
                result.append(grid[row][col])
                
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt text using Columnar Transposition cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Keyword used for encryption
    """
    if not key:
        return ciphertext
        
    num_cols = len(key)
    num_rows = (len(ciphertext) + num_cols - 1) // num_cols
    
    # Calculate column lengths (some columns might be shorter)
    col_lengths = [num_rows] * num_cols
    short_cols = num_cols * num_rows - len(ciphertext)
    for i in sorted(range(num_cols), key=lambda x: key[x])[num_cols-short_cols:]:
        col_lengths[i] -= 1
        
    # Create inverse column order mapping
    col_order = sorted(range(num_cols), key=lambda x: key[x])
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
                
    # Read off rows to get plaintext
    result = []
    for row in grid:
        result.extend(ch for ch in row if ch)
        
    return ''.join(result)