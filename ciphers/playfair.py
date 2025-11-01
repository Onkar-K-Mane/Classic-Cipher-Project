"""
Playfair cipher implementation.
Uses a 5x5 key matrix (I/J sharing a cell) for digraph substitution.
"""

def _build_playfair_matrix(key: str):
    """Build 5x5 Playfair key matrix from given key."""
    key = key.replace(' ', '').upper()
    result = []
    for c in key:
        if c == 'J':
            c = 'I'
        if c not in result and c.isalpha():
            result.append(c)
    
    # Fill remaining letters (A-Z except J)
    flag = 0
    for i in range(65, 91):
        ch = chr(i)
        if ch not in result:
            if i == 73 and chr(74) not in result:
                result.append('I')
                flag = 1
            elif flag == 0 and (i == 73 or i == 74):
                pass
            else:
                result.append(ch)
    
    # Convert to 5x5 matrix
    matrix = [result[i*5:(i+1)*5] for i in range(5)]
    return matrix


def _locindex(matrix, f):
    """Find coordinates of letter in Playfair matrix."""
    if f == 'J':
        f = 'I'
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == f:
                return (r, c)
    return None


def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt text using Playfair cipher with given key.
    Maps J->I, splits double letters with X, pads if needed.
    """
    if not key or not any(ch.isalpha() for ch in key):
        raise ValueError('Playfair key must contain letters')
    
    matrix = _build_playfair_matrix(key)
    msg = ''.join(ch for ch in plaintext.upper() if ch.isalpha())
    
    # replace J -> I
    msg = msg.replace('J', 'I')
    
    # insert X between double letters in pair
    i = 0
    pairs = []
    while i < len(msg):
        a = msg[i]
        b = msg[i+1] if i+1 < len(msg) else 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    
    if pairs and pairs[-1][1] == '':
        pairs[-1] = (pairs[-1][0], 'X')
    
    out = []
    for a, b in pairs:
        loc = _locindex(matrix, a)
        loc1 = _locindex(matrix, b)
        if loc is None or loc1 is None:
            raise ValueError('Only letters A-Z allowed in Playfair message')
        
        if loc[0] == loc1[0]:  # same row
            out.append(matrix[loc[0]][(loc[1] + 1) % 5])
            out.append(matrix[loc1[0]][(loc1[1] + 1) % 5])
        elif loc[1] == loc1[1]:  # same column
            out.append(matrix[(loc[0] + 1) % 5][loc[1]])
            out.append(matrix[(loc1[0] + 1) % 5][loc1[1]])
        else:  # rectangle case
            out.append(matrix[loc[0]][loc1[1]])
            out.append(matrix[loc1[0]][loc[1]])
    
    return ''.join(out)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt text using Playfair cipher with given key.
    Maps J->I, processes digraphs according to Playfair rules.
    """
    if not key or not any(ch.isalpha() for ch in key):
        raise ValueError('Playfair key must contain letters')
    
    matrix = _build_playfair_matrix(key)
    msg = ''.join(ch for ch in ciphertext.upper() if ch.isalpha())
    
    out = []
    i = 0
    while i < len(msg):
        a = msg[i]
        b = msg[i+1] if i+1 < len(msg) else 'X'
        loc = _locindex(matrix, a)
        loc1 = _locindex(matrix, b)
        if loc is None or loc1 is None:
            raise ValueError('Only letters A-Z allowed in Playfair message')
        
        if loc[0] == loc1[0]:  # same row
            out.append(matrix[loc[0]][(loc[1] - 1) % 5])
            out.append(matrix[loc1[0]][(loc1[1] - 1) % 5])
        elif loc[1] == loc1[1]:  # same column
            out.append(matrix[(loc[0] - 1) % 5][loc[1]])
            out.append(matrix[(loc1[0] - 1) % 5][loc1[1]])
        else:  # rectangle case
            out.append(matrix[loc[0]][loc1[1]])
            out.append(matrix[loc1[0]][loc[1]])
        i += 2
    
    return ''.join(out)