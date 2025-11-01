#!/usr/bin/env python3
"""
Simple Tkinter GUI for classic ciphers in this repository.

Supports:
- Caesar cipher (shift key integer)
- Vigenere cipher (alphabetic key)

This is intentionally self-contained so it doesn't rely on the other repository files
which are present without .py extensions and expect interactive console input.

Run: python gui.py
"""
import string
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


def caesar_encrypt(plaintext: str, key: int) -> str:
    result = []
    for ch in plaintext:
        if ch.isupper():
            result.append(chr((ord(ch) - 65 + key) % 26 + 65))
        elif ch.islower():
            result.append(chr((ord(ch) - 97 + key) % 26 + 97))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    return caesar_encrypt(ciphertext, -key)


def vigenere_encrypt(plaintext: str, key: str) -> str:
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


def vigenere_decrypt(ciphertext: str, key: str) -> str:
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


# ---- Hill cipher (2x2) ----
def _find_multiplicative_inverse(determinant: int) -> int:
    determinant %= 26
    for i in range(26):
        if (determinant * i) % 26 == 1:
            return i
    return -1


def _make_key_matrix_from_string(key: str):
    key = key.strip()
    if len(key) != 4 or not key.isalpha():
        raise ValueError("Hill key must be 4 letters (2x2 matrix)")
    nums = [ord(c.upper()) - 65 for c in key]
    # return as [[a,b],[c,d]]
    return [[nums[0], nums[1]], [nums[2], nums[3]]]


def hill_encrypt(plaintext: str, key: str) -> str:
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


def hill_decrypt(ciphertext: str, key: str) -> str:
    k = _make_key_matrix_from_string(key)
    det = (k[0][0] * k[1][1] - k[0][1] * k[1][0]) % 26
    inv = _find_multiplicative_inverse(det)
    if inv == -1:
        raise ValueError("Hill key matrix is not invertible modulo 26")
    # compute adjugate * inv mod 26
    a, b = k[0][0], k[0][1]
    c, d = k[1][0], k[1][1]
    adj = [[d * inv % 26, (-b) * inv % 26], [(-c) * inv % 26, a * inv % 26]]
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


# ---- Playfair cipher ----
def _build_playfair_matrix(key: str):
    key = key.replace(' ', '').upper()
    result = []
    for c in key:
        if c == 'J':
            c = 'I'
        if c not in result and c.isalpha():
            result.append(c)
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
    # build 5x5
    matrix = [result[i*5:(i+1)*5] for i in range(5)]
    return matrix


def _locindex(matrix, f):
    if f == 'J':
        f = 'I'
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == f:
                return (r, c)
    return None


def playfair_encrypt(plaintext: str, key: str) -> str:
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
        if loc[0] == loc1[0]:
            out.append(matrix[loc[0]][(loc[1] + 1) % 5])
            out.append(matrix[loc1[0]][(loc1[1] + 1) % 5])
        elif loc[1] == loc1[1]:
            out.append(matrix[(loc[0] + 1) % 5][loc[1]])
            out.append(matrix[(loc1[0] + 1) % 5][loc1[1]])
        else:
            out.append(matrix[loc[0]][loc1[1]])
            out.append(matrix[loc1[0]][loc[1]])
    return ''.join(out)


def playfair_decrypt(ciphertext: str, key: str) -> str:
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
        if loc[0] == loc1[0]:
            out.append(matrix[loc[0]][(loc[1] - 1) % 5])
            out.append(matrix[loc1[0]][(loc1[1] - 1) % 5])
        elif loc[1] == loc1[1]:
            out.append(matrix[(loc[0] - 1) % 5][loc[1]])
            out.append(matrix[(loc1[0] - 1) % 5][loc1[1]])
        else:
            out.append(matrix[loc[0]][loc1[1]])
            out.append(matrix[loc1[0]][loc[1]])
        i += 2
    return ''.join(out)


class CipherGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Classic Ciphers - GUI")
        self.geometry("700x520")
        self._build()

    def _build(self):
        pad = 8
        frm = ttk.Frame(self, padding=pad)
        frm.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frm)
        top.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(top, text="Cipher:").pack(side=tk.LEFT)
        self.cipher_var = tk.StringVar(value="Caesar")
        cipher_cb = ttk.Combobox(top, textvariable=self.cipher_var, state="readonly",
                                 values=["Caesar", "Vigenere", "Hill", "Playfair"])
        cipher_cb.pack(side=tk.LEFT, padx=(6, 12))

        self.mode_var = tk.StringVar(value="Encrypt")
        ttk.Radiobutton(top, text="Encrypt", variable=self.mode_var, value="Encrypt").pack(side=tk.LEFT)
        ttk.Radiobutton(top, text="Decrypt", variable=self.mode_var, value="Decrypt").pack(side=tk.LEFT)

        keyfrm = ttk.Frame(frm)
        keyfrm.pack(fill=tk.X)
        ttk.Label(keyfrm, text="Key:").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(keyfrm)
        self.key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        mid = ttk.Frame(frm)
        mid.pack(fill=tk.BOTH, expand=True, pady=(8, 8))

        left = ttk.Frame(mid)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(left, text="Input:").pack(anchor=tk.W)
        self.input_text = ScrolledText(left, height=12)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        right = ttk.Frame(mid)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        ttk.Label(right, text="Output:").pack(anchor=tk.W)
        self.output_text = ScrolledText(right, height=12)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        btnfrm = ttk.Frame(frm)
        btnfrm.pack(fill=tk.X, pady=(8, 0))
        run_btn = ttk.Button(btnfrm, text="Run", command=self.on_run)
        run_btn.pack(side=tk.LEFT)

        copy_btn = ttk.Button(btnfrm, text="Copy Output", command=self.copy_output)
        copy_btn.pack(side=tk.LEFT, padx=(6, 0))

        clear_btn = ttk.Button(btnfrm, text="Clear", command=self.clear_all)
        clear_btn.pack(side=tk.RIGHT)

    def on_run(self):
        cipher = self.cipher_var.get()
        mode = self.mode_var.get()
        key = self.key_entry.get().strip()
        text = self.input_text.get("1.0", tk.END).rstrip('\n')
        try:
            if cipher == "Caesar":
                if not key:
                    raise ValueError("Enter integer key for Caesar cipher")
                try:
                    k = int(key)
                except ValueError:
                    raise ValueError("Caesar key must be an integer")
                if mode == "Encrypt":
                    out = caesar_encrypt(text, k)
                else:
                    out = caesar_decrypt(text, k)
            elif cipher == "Vigenere":
                if not key or not any(ch.isalpha() for ch in key):
                    raise ValueError("Vigenere key must contain letters")
                if mode == "Encrypt":
                    out = vigenere_encrypt(text, key)
                else:
                    out = vigenere_decrypt(text, key)
            elif cipher == "Hill":
                # Hill expects a 4-letter key for 2x2 matrix
                if not key or not key.isalpha() or len(key) != 4:
                    raise ValueError("Hill key must be 4 letters (2x2 matrix)")
                if mode == "Encrypt":
                    out = hill_encrypt(text, key)
                else:
                    out = hill_decrypt(text, key)
            elif cipher == "Playfair":
                if not key or not any(ch.isalpha() for ch in key):
                    raise ValueError("Playfair key must contain letters")
                if mode == "Encrypt":
                    out = playfair_encrypt(text, key)
                else:
                    out = playfair_decrypt(text, key)
            else:
                raise ValueError("Unsupported cipher")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, out)

    def copy_output(self):
        out = self.output_text.get("1.0", tk.END).rstrip('\n')
        self.clipboard_clear()
        self.clipboard_append(out)
        messagebox.showinfo("Copied", "Output copied to clipboard")

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.key_entry.delete(0, tk.END)


def main():
    app = CipherGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
