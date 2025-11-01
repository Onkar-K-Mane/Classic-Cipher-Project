# Classic Ciphers Project

Collection of classical cipher implementations with a simple Tkinter GUI interface.

## Features

- Modular cipher implementations in the `ciphers` package, each exposing `encrypt()` and `decrypt()`:
  - **Caesar cipher** (`caesar.py`) - Shift cipher with integer key
  - **Vigenere cipher** (`vigenere.py`) - Polyalphabetic substitution with keyword
  - **Hill cipher** (`hill.py`) - 2x2 matrix-based encryption
  - **Playfair cipher** (`playfair.py`) - 5x5 matrix digraph substitution
  - **Atbash cipher** (`atbash.py`) - Simple reverse-alphabet substitution (no key)
  - **Rail Fence cipher** (`rail_fence.py`) - Zigzag transposition with configurable rails
  - **ADFGVX cipher** (`adfgvx.py`) - Polybius square (A-Z + 0-9) + columnar transposition
  - **Columnar transposition** (`columnar.py`) - Key-ordered columnar transposition
  - **Autokey cipher** (`autokey.py`) - Vigenère-like cipher using plaintext to extend the key

- Interactive Tkinter GUI (`gui.py`) to try encryption/decryption with quick key instructions
- Pure Python implementation using only the standard library

## Project structure

```
Ceasar-Cipher-Project/
├── ciphers/               # Cipher implementations
│   ├── __init__.py        # Package initialization
│   ├── adfgvx.py          # ADFGVX (Polybius + Columnar)
│   ├── autokey.py         # Autokey cipher
│   ├── atbash.py          # Atbash cipher
│   ├── caesar.py          # Caesar shift cipher
│   ├── columnar.py        # Columnar transposition
│   ├── hill.py            # Hill cipher (2x2 matrix)
│   ├── playfair.py        # Playfair cipher
│   ├── rail_fence.py      # Rail Fence cipher
│   └── vigenere.py        # Vigenere cipher
├── gui.py                 # Tkinter GUI interface
├── README.md              # This file
└── (other docs/tests...)
```

## Quick start

Requirements:
- Python 3.8+ (Tkinter should be included with standard Python installs)

Run the GUI (PowerShell):
```powershell
python "v:\\Ceasar-Cipher-Project\\gui.py"
```

## Key formats and quick instructions

The GUI provides short key instructions below the key field. Summary here:

- Caesar: integer shift (e.g. 3). Positive shifts move forward in the alphabet.
- Vigenere: alphabetic keyword (e.g. KEY). Non-letters in the key are ignored.
- Hill: exactly 4 letters to form a 2x2 matrix key (e.g. HILL). Must be invertible mod 26 for decryption.
- Playfair: word or phrase to build a 5x5 key square (e.g. MONARCHY). Uses I/J convention.
- Atbash: no key needed — leave empty. Substitutes A↔Z, B↔Y, etc.
- Rail Fence: integer number of rails (e.g. 3). Use the same number for decrypting.
- ADFGVX: two keys separated by a comma: polybius-key,columnar-key (e.g. SECRET,ORDER). Polybius arranges A–Z and 0–9; columnar key orders columns.
- Columnar: a word used to determine column ordering (e.g. KEY). Use same key for decrypting.
- Autokey: initial alphabetic key (e.g. SECRET). The plaintext is appended to the key during encryption.

Examples (entered into the GUI):

- Caesar encrypt plaintext "HELLO" with key `3` -> "KHOOR"
- Rail Fence encrypt plaintext "WEAREDISCOVERED" with key `3` -> ciphertext displayed by the GUI
- ADFGVX encrypt plaintext "ATTACKATDAWN" with key `SECRET,ORDER` -> produces ADFGVX-style output

## Developer notes

- All ciphers live in `ciphers/` and expose `encrypt(text, key...)` and `decrypt(text, key...)` where the key signature may vary by algorithm.
- The GUI (`gui.py`) was updated to include the new ciphers and shows contextual key instructions.
- The project uses only the Python standard library; no extra install is required.


