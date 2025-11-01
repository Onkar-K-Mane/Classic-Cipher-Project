# GUI for Classic Ciphers

A Tkinter-based GUI for trying various classical ciphers interactively.

## Supported Ciphers

- **Caesar Cipher**
  - Key: integer (e.g., `3`)
  - Shifts each letter by the key value
  - Preserves case and non-letter characters
  
- **Vigenere Cipher**
  - Key: any text (e.g., `secret`)
  - Uses repeating key letters to shift plaintext
  - Non-letters in key are ignored
  - Preserves input case and punctuation
  
- **Hill Cipher (2x2)**
  - Key: exactly 4 letters (e.g., `HILL`)
  - Forms a 2x2 matrix where A=0, B=1, ..., Z=25
  - Key matrix must be invertible modulo 26
  - Pads odd-length input with 'X'
  - Outputs uppercase text
  
- **Playfair Cipher**
  - Key: any text (e.g., `playfair example`)
  - Creates 5x5 matrix (I/J share cell)
  - Encrypts letter pairs with special rules
  - Splits double letters with 'X'
  - Outputs uppercase text

## Quick Start

Requirements:
- Python 3.x (Windows)
- Tkinter (included with standard Python)

Run the GUI:
```powershell
python "v:\Ceasar-Cipher-Project\gui.py"
```

## Usage Guide

1. Select a cipher from the dropdown
2. Enter the appropriate key (see below)
3. Type or paste your input text
4. Choose Encrypt or Decrypt
5. Click Run to see the result
6. Use "Copy Output" to copy the result

## Key Format Examples

Caesar:
- Valid: `3`, `12`, `-5`
- Note: Use positive numbers to shift right, negative to shift left

Vigenere:
- Valid: `LEMON`, `secret`, `Key Phrase 123`
- Note: Numbers and spaces are ignored, only letters are used

Hill:
- Valid: `HILL`, `GYBN`, `CODE`
- Must be exactly 4 letters
- Not all 4-letter combinations work (matrix must be invertible mod 26)
- Common working keys: `GYBN`, `HILL`

Playfair:
- Valid: `PLAYFAIR EXAMPLE`, `monarchy`, `secret message`
- Longer keys give better security
- J is converted to I in the key grid

## Troubleshooting

Common issues:
1. **"Hill key matrix is not invertible modulo 26"**
   - Try a known working key like `GYBN` or `HILL`
   - Not all 4-letter combinations form valid keys

2. **"Key must contain letters"**
   - Vigenere/Playfair keys must include at least one letter
   - Numbers and spaces alone are not valid keys

3. **GUI doesn't appear**
   - Ensure Python includes Tkinter (standard with python.org downloads)
   - Try running from command prompt to see error messages

## Implementation Notes

- The ciphers are implemented in separate modules in the `ciphers/` package
- Each cipher preserves its classical behavior while adding some modern conveniences
- Error messages explain exactly what went wrong
- Copy button makes it easy to paste results elsewhere

