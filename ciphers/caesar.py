"""
Caesar cipher implementation (shift cipher).
Simple substitution cipher that shifts letters by a fixed amount.
"""

def encrypt(plaintext: str, key: int) -> str:
    """
    Encrypt text using Caesar cipher with given shift key.
    Preserves case and non-letter characters.
    """
    result = []
    for ch in plaintext:
        if ch.isupper():
            result.append(chr((ord(ch) - 65 + key) % 26 + 65))
        elif ch.islower():
            result.append(chr((ord(ch) - 97 + key) % 26 + 97))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypt text using Caesar cipher with given shift key.
    Preserves case and non-letter characters.
    """
    return encrypt(ciphertext, -key)  # decryption is encryption with negative key