#!/usr/bin/env python3
"""
Simple Tkinter GUI for classic ciphers in this repository.

Supports:
- Caesar cipher (shift key integer)
- Vigenere cipher (alphabetic key)
- Hill cipher (2x2 matrix)
- Playfair cipher (5x5 key square)
- Atbash cipher (no key needed)
- Rail Fence cipher (number of rails as key)
- ADFGVX cipher (two keys: polybius key and columnar key, separated by comma)
- Columnar cipher (ordering key)
- Autokey cipher (initial key, rest derived from plaintext)

Run: python gui.py
"""
import string
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from ciphers import (
    caesar, vigenere, hill, playfair,
    atbash, rail_fence, adfgvx, columnar, autokey
)


class CipherGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Classic Ciphers - GUI")
        self.geometry("700x580")  # Made taller to accommodate instructions
        self._build()

    def update_key_instructions(self, event=None):
        instructions = {
            "Caesar": "Enter an integer number for the shift (e.g. 3)",
            "Vigenere": "Enter any word or phrase using letters only (e.g. KEY)",
            "Hill": "Enter exactly 4 letters to form a 2x2 matrix key",
            "Playfair": "Enter a word or phrase using letters only (creates 5x5 key square)",
            "Atbash": "No key needed (leave empty) - reverses the alphabet",
            "Rail Fence": "Enter the number of rails (e.g. 3)",
            "ADFGVX": "Enter two keys separated by comma: polybius square key,columnar key (e.g. SECRET,ORDER)",
            "Columnar": "Enter a word to determine column ordering (e.g. KEY)",
            "Autokey": "Enter an initial key word (will be combined with plaintext)"
        }
        cipher = self.cipher_var.get()
        self.key_instructions.config(text=f"Key format: {instructions.get(cipher, '')}")

    def _build(self):
        pad = 8
        frm = ttk.Frame(self, padding=pad)
        frm.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frm)
        top.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(top, text="Cipher:").pack(side=tk.LEFT)
        self.cipher_var = tk.StringVar(value="Caesar")
        cipher_cb = ttk.Combobox(top, textvariable=self.cipher_var, state="readonly",
                                values=["Caesar", "Vigenere", "Hill", "Playfair",
                                       "Atbash", "Rail Fence", "ADFGVX", "Columnar", "Autokey"])
        cipher_cb.pack(side=tk.LEFT, padx=(6, 12))

        self.mode_var = tk.StringVar(value="Encrypt")
        ttk.Radiobutton(top, text="Encrypt", variable=self.mode_var, value="Encrypt").pack(side=tk.LEFT)
        ttk.Radiobutton(top, text="Decrypt", variable=self.mode_var, value="Decrypt").pack(side=tk.LEFT)

        keyfrm = ttk.Frame(frm)
        keyfrm.pack(fill=tk.X)
        ttk.Label(keyfrm, text="Key:").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(keyfrm)
        self.key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        # Key instructions
        self.key_instructions = ttk.Label(frm, text="", wraplength=680)
        self.key_instructions.pack(fill=tk.X, pady=(4, 0))
        
        # Update key instructions when cipher is changed
        cipher_cb.bind('<<ComboboxSelected>>', self.update_key_instructions)
        self.update_key_instructions()

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
                    out = caesar.encrypt(text, k)
                else:
                    out = caesar.decrypt(text, k)
            elif cipher == "Vigenere":
                if not key or not any(ch.isalpha() for ch in key):
                    raise ValueError("Vigenere key must contain letters")
                if mode == "Encrypt":
                    out = vigenere.encrypt(text, key)
                else:
                    out = vigenere.decrypt(text, key)
            elif cipher == "Hill":
                # Hill expects a 4-letter key
                if not key or not key.isalpha() or len(key) != 4:
                    raise ValueError("Hill key must be 4 letters (2x2 matrix)")
                if mode == "Encrypt":
                    out = hill.encrypt(text, key)
                else:
                    out = hill.decrypt(text, key)
            elif cipher == "Playfair":
                if not key or not any(ch.isalpha() for ch in key):
                    raise ValueError("Playfair key must contain letters")
                if mode == "Encrypt":
                    out = playfair.encrypt(text, key)
                else:
                    out = playfair.decrypt(text, key)
            elif cipher == "Atbash":
                # Atbash doesn't need a key
                if mode == "Encrypt":
                    out = atbash.encrypt(text)
                else:
                    out = atbash.decrypt(text)
            elif cipher == "Rail Fence":
                if not key:
                    raise ValueError("Enter number of rails")
                try:
                    rails = int(key)
                    if rails < 2:
                        raise ValueError
                except ValueError:
                    raise ValueError("Rail Fence key must be an integer greater than 1")
                if mode == "Encrypt":
                    out = rail_fence.encrypt(text, rails)
                else:
                    out = rail_fence.decrypt(text, rails)
            elif cipher == "ADFGVX":
                if not key or ',' not in key:
                    raise ValueError("ADFGVX requires two keys separated by comma")
                polybius_key, columnar_key = map(str.strip, key.split(',', 1))
                if not columnar_key:
                    raise ValueError("Columnar key is required for ADFGVX")
                if mode == "Encrypt":
                    out = adfgvx.encrypt(text, polybius_key, columnar_key)
                else:
                    out = adfgvx.decrypt(text, polybius_key, columnar_key)
            elif cipher == "Columnar":
                if not key:
                    raise ValueError("Enter a key for columnar transposition")
                if mode == "Encrypt":
                    out = columnar.encrypt(text, key)
                else:
                    out = columnar.decrypt(text, key)
            elif cipher == "Autokey":
                if not key:
                    raise ValueError("Enter an initial key for Autokey cipher")
                if mode == "Encrypt":
                    out = autokey.encrypt(text, key)
                else:
                    out = autokey.decrypt(text, key)
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