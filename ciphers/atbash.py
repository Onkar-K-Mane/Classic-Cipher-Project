"""
Atbash cipher implementation.
A simple substitution cipher that reverses the alphabet (A->Z, B->Y, etc.).
"""

def encrypt(plaintext: str) -> str:
    """
    Encrypt text using Atbash cipher.
    Preserves case and non-letter characters.
    """
    result = []
    for ch in plaintext:
        if ch.isupper():
            # A=65->Z=90, B=66->Y=89, etc.
            result.append(chr(90 - (ord(ch) - 65)))
        elif ch.islower():
            # a=97->z=122, b=98->y=121, etc.
            result.append(chr(122 - (ord(ch) - 97)))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(ciphertext: str) -> str:
    """
    Decrypt text using Atbash cipher.
    Since Atbash is its own inverse, this is the same as encrypt.
    """
    return encrypt(ciphertext)  # Atbash is reciprocal