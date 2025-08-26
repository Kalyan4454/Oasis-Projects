import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    length = int(length_var.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()
    
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    if not characters:
        messagebox.showerror("Error", "Select at least one character set!")
        return
    
    password = "".join(random.choice(characters) for _ in range(length))
    password_var.set(password)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# --- GUI Setup ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")
root.configure(bg="#1e1e2f")  # Dark background

# Variables
length_var = tk.IntVar(value=12)
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
password_var = tk.StringVar()

# Style options
label_fg = "#ffffff"    # white text
button_bg = "#4caf50"   # green button
button_fg = "#ffffff"   # white button text
entry_bg = "#2d2d44"    # dark entry background
entry_fg = "#00ffcc"    # cyan text

# Widgets
tk.Label(root, text="Password Length:", bg="#1e1e2f", fg=label_fg).pack(pady=5)
tk.Spinbox(root, from_=4, to=50, textvariable=length_var, bg=entry_bg, fg=entry_fg,
           insertbackground="white", justify="center").pack()

tk.Checkbutton(root, text="Include Letters", variable=letters_var, bg="#1e1e2f", fg=label_fg, selectcolor="#333").pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var, bg="#1e1e2f", fg=label_fg, selectcolor="#333").pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var, bg="#1e1e2f", fg=label_fg, selectcolor="#333").pack(anchor="w", padx=20)

tk.Button(root, text="Generate Password", command=generate_password,
          bg=button_bg, fg=button_fg, activebackground="#45a049").pack(pady=10)

tk.Entry(root, textvariable=password_var, width=40, justify="center",
         bg=entry_bg, fg=entry_fg, insertbackground="white").pack()

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard,
          bg="#2196f3", fg=button_fg, activebackground="#1976d2").pack(pady=5)

root.mainloop()
