"""
Autokey cipher implementation.
A polyalphabetic substitution cipher that uses the plaintext itself as part of the key.
"""

def prepare_key(plaintext: str, key: str) -> str:
    """
    Generate the full autokey by combining the key with the plaintext.
    """
    # Remove spaces and convert to uppercase
    plaintext = ''.join(plaintext.split()).upper()
    key = ''.join(key.split()).upper()
    
    if not key:
        return plaintext
        
    # Filter out non-alphabetic characters from both key and plaintext
    key = ''.join(c for c in key if c.isalpha())
    filtered_plaintext = ''.join(c for c in plaintext if c.isalpha())
    
    # Combine key with plaintext to create autokey
    return (key + filtered_plaintext)[:len(filtered_plaintext)]


def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt text using Autokey cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Initial key (will be combined with plaintext)
    """
    if not key:
        return plaintext
        
    # Remove spaces and convert to uppercase
    plaintext = ''.join(plaintext.split()).upper()
    
    # Generate full autokey
    autokey = prepare_key(plaintext, key)
    
    result = []
    key_pos = 0
    
    for char in plaintext:
        if char.isalpha():
            # Perform Vigenère-style encryption using autokey
            shift = ord(autokey[key_pos]) - ord('A')
            encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(encrypted)
            key_pos += 1
        else:
            result.append(char)
            
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt text using Autokey cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Initial key used for encryption
    """
    if not key:
        return ciphertext
        
    # Remove spaces and convert to uppercase
    ciphertext = ''.join(ciphertext.split()).upper()
    key = ''.join(key.split()).upper()
    
    result = []
    partial_key = key
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Get the current key character
            if i < len(key):
                key_char = key[i]
            else:
                # Use previously decrypted character
                key_char = result[i - len(key)]
                
            # Perform Vigenère-style decryption
            shift = ord(key_char) - ord('A')
            decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            result.append(decrypted)
        else:
            result.append(char)
            
    return ''.join(result)