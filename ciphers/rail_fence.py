"""
Rail Fence cipher implementation.
A transposition cipher that writes text in a zigzag pattern across 'rails'
and reads off the resulting cipher text by rows.
"""

def _create_fence(height: int, length: int) -> list[list[None | str]]:
    """Create an empty rail fence with given height and length."""
    return [[None] * length for _ in range(height)]


def _traverse_fence(height: int, length: int) -> list[tuple[int, int]]:
    """Generate zigzag coordinates for rail fence traversal."""
    rail = 0
    going_down = True
    coords = []
    
    for col in range(length):
        coords.append((rail, col))
        if rail == 0:
            going_down = True
        elif rail == height - 1:
            going_down = False
            
        rail += 1 if going_down else -1
        
    return coords


def encrypt(plaintext: str, rails: int) -> str:
    """
    Encrypt text using Rail Fence cipher with specified number of rails.
    """
    if rails < 2:
        return plaintext
        
    # Remove any spaces and convert to uppercase for consistent encryption
    plaintext = ''.join(plaintext.split()).upper()
    
    # Create the fence
    fence = _create_fence(rails, len(plaintext))
    
    # Place text in zigzag pattern
    coords = _traverse_fence(rails, len(plaintext))
    for (rail, col), char in zip(coords, plaintext):
        fence[rail][col] = char
        
    # Read off by rows to get ciphertext
    return ''.join(char for row in fence for char in row if char is not None)


def decrypt(ciphertext: str, rails: int) -> str:
    """
    Decrypt text using Rail Fence cipher with specified number of rails.
    """
    if rails < 2:
        return ciphertext
        
    # Create the fence
    fence = _create_fence(rails, len(ciphertext))
    
    # Mark zigzag pattern
    coords = _traverse_fence(rails, len(ciphertext))
    
    # Place markers in fence
    for rail, col in coords:
        fence[rail][col] = ''
        
    # Fill the fence with ciphertext
    pos = 0
    for rail in range(rails):
        for col in range(len(ciphertext)):
            if fence[rail][col] == '':
                fence[rail][col] = ciphertext[pos]
                pos += 1
                
    # Read off in zigzag pattern
    coords = _traverse_fence(rails, len(ciphertext))
    return ''.join(fence[rail][col] for rail, col in coords)