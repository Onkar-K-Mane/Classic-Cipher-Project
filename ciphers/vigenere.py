"""
Vigenere cipher implementation.
Polyalphabetic substitution cipher using a repeating key word.
"""

def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt text using Vigenere cipher with given key.
    Key must contain letters; non-letters are stripped.
    Preserves case and non-letter characters in plaintext.
    """
    key = ''.join([k for k in key if k.isalpha()])
    if not key:
        raise ValueError("Key must contain letters for Vigenere")
    result = []
    ki = 0
    for ch in plaintext:
        if ch.isalpha():
            k = key[ki % len(key)]
            shift = ord(k.lower()) - 97
            if ch.isupper():
                result.append(chr((ord(ch) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(ch) - 97 + shift) % 26 + 97))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt text using Vigenere cipher with given key.
    Key must contain letters; non-letters are stripped.
    Preserves case and non-letter characters in ciphertext.
    """
    key = ''.join([k for k in key if k.isalpha()])
    if not key:
        raise ValueError("Key must contain letters for Vigenere")
    result = []
    ki = 0
    for ch in ciphertext:
        if ch.isalpha():
            k = key[ki % len(key)]
            shift = ord(k.lower()) - 97
            if ch.isupper():
                result.append(chr((ord(ch) - 65 - shift) % 26 + 65))
            else:
                result.append(chr((ord(ch) - 97 - shift) % 26 + 97))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)