"""
Hill cipher implementation (2x2 matrix).
Uses a 2x2 matrix of letters as key for encryption/decryption.
"""

def _find_multiplicative_inverse(determinant: int) -> int:
    """Find multiplicative inverse mod 26 of the given determinant."""
    determinant %= 26
    for i in range(26):
        if (determinant * i) % 26 == 1:
            return i
    return -1


def _make_key_matrix_from_string(key: str):
    """Convert 4-letter key to 2x2 matrix [[a,b],[c,d]]."""
    key = key.strip()
    if len(key) != 4 or not key.isalpha():
        raise ValueError("Hill key must be 4 letters (2x2 matrix)")
    nums = [ord(c.upper()) - 65 for c in key]
    return [[nums[0], nums[1]], [nums[2], nums[3]]]


def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt text using Hill cipher with given 4-letter key.
    Key forms a 2x2 matrix that must be invertible modulo 26.
    Pads odd-length messages with 'X'.
    """
    k = _make_key_matrix_from_string(key)
    det = (k[0][0] * k[1][1] - k[0][1] * k[1][0]) % 26
    if _find_multiplicative_inverse(det) == -1:
        raise ValueError("Hill key matrix is not invertible modulo 26")
    
    # remove spaces per original script
    p = ''.join(ch for ch in plaintext if ch != ' ')
    # pad with X if odd
    if len(p) % 2 != 0:
        p += 'X'
    
    out = []
    for i in range(0, len(p), 2):
        a = ord(p[i].upper()) - 65
        b = ord(p[i+1].upper()) - 65
        c0 = (k[0][0] * a + k[0][1] * b) % 26
        c1 = (k[1][0] * a + k[1][1] * b) % 26
        out.append(chr(c0 + 65))
        out.append(chr(c1 + 65))
    return ''.join(out)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt text using Hill cipher with given 4-letter key.
    Key must form an invertible 2x2 matrix modulo 26.
    Removes trailing padding 'X' if present.
    """
    k = _make_key_matrix_from_string(key)
    det = (k[0][0] * k[1][1] - k[0][1] * k[1][0]) % 26
    inv = _find_multiplicative_inverse(det)
    if inv == -1:
        raise ValueError("Hill key matrix is not invertible modulo 26")
    
    # compute adjugate * inv mod 26
    a, b = k[0][0], k[0][1]
    c, d = k[1][0], k[1][1]
    adj = [[d * inv % 26, (-b) * inv % 26], 
           [(-c) * inv % 26, a * inv % 26]]
    
    p = ''.join(ch for ch in ciphertext if ch != ' ')
    out = []
    for i in range(0, len(p), 2):
        x = ord(p[i].upper()) - 65
        y = ord(p[i+1].upper()) - 65
        m0 = (adj[0][0] * x + adj[0][1] * y) % 26
        m1 = (adj[1][0] * x + adj[1][1] * y) % 26
        out.append(chr(m0 + 65))
        out.append(chr(m1 + 65))
    
    # remove trailing padding X if present (best-effort)
    result = ''.join(out)
    if result.endswith('X'):
        result = result[:-1]
    return result