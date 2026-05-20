import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyperclip  # pip install pyperclip - for copy button

def translate_text():
    try:
        # 1. Get input text
        src_text = input_box.get("1.0", tk.END).strip()
        if not src_text:
            messagebox.showwarning("Empty Input", "Please enter text to translate!")
            return

        # 2. Get source & target language codes
        src_lang = lang_codes[source_lang.get()]
        dest_lang = lang_codes[target_lang.get()]
        
        if src_lang == dest_lang:
            messagebox.showinfo("Same Language", "Source and target languages are the same!")
            return

        # 3. Send to API and get response
        translator = Translator()
        translated = translator.translate(src_text, src=src_lang, dest=dest_lang)
        
        # 4. Display translated text clearly
        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", translated.text)
        output_box.config(state='disabled')
        
        # Update detected language if auto-detect used
        if src_lang == 'auto':
            detected = LANGUAGES.get(translated.src, 'Unknown')
            source_lang.set(detected.capitalize())

    except Exception as e:
        messagebox.showerror("Translation Error", f"Sixth Sheikh error: {e}\nCheck internet connection.")

def copy_text():
    """Optional: Copy translated text to clipboard"""
    text = output_box.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Translated text copied to clipboard!")
    else:
        messagebox.showwarning("Empty", "Nothing to copy!")

def clear_text():
    """Clear both boxes"""
    input_box.delete("1.0", tk.END)
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.config(state='disabled')

def swap_languages():
    """Swap source and target languages"""
    src = source_lang.get()
    dest = target_lang.get()
    source_lang.set(dest)
    target_lang.set(src)

# ===== UI SETUP =====
root = tk.Tk()
root.title("TASK 1: Language Translation Tool")
root.geometry("600x550")
root.resizable(False, False)

# Language dictionary: Name -> Code
lang_codes = {name.capitalize(): code for code, name in LANGUAGES.items()}
lang_codes['Auto Detect'] = 'auto'
lang_list = sorted(lang_codes.keys())

# Title
tk.Label(root, text="Language Translation Tool", font=("Arial", 16, "bold")).pack(pady=10)

# Language Selection Frame
lang_frame = tk.Frame(root)
lang_frame.pack(pady=10)

tk.Label(lang_frame, text="From:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
source_lang = ttk.Combobox(lang_frame, values=lang_list, width=15, state="readonly")
source_lang.set("Auto Detect")
source_lang.grid(row=0, column=1, padx=5)

tk.Button(lang_frame, text="⇄", command=swap_languages, width=3).grid(row=0, column=2, padx=10)

tk.Label(lang_frame, text="To:", font=("Arial", 11)).grid(row=0, column=3, padx=5)
target_lang = ttk.Combobox(lang_frame, values=lang_list, width=15, state="readonly")
target_lang.set("Hindi")
target_lang.grid(row=0, column=4, padx=5)

# Input Text
tk.Label(root, text="Enter Text:", font=("Arial", 12)).pack(anchor='w', padx=20)
input_box = tk.Text(root, height=6, width=65, font=("Arial", 11))
input_box.pack(pady=5)
input_box.insert("1.0", "Type the text you wanna translate")  # Default test

# Translate Button
tk.Button(root, text="Translate", command=translate_text, 
          bg="#4285F4", fg="white", font=("Arial", 12, "bold"), 
          width=15, height=1).pack(pady=15)

# Output Text
tk.Label(root, text="Translated Text:", font=("Arial", 12)).pack(anchor='w', padx=20)
output_box = tk.Text(root, height=6, width=65, font=("Arial", 11), state='disabled', bg="#f0f0f0")
output_box.pack(pady=5)

# Optional: Button Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Copy Output", command=copy_text, width=12).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Clear All", command=clear_text, width=12).grid(row=0, column=1, padx=10)

# Footer
tk.Label(root, text="Uses Google Translate API via googletrans library", 
         font=("Arial", 8), fg="gray").pack(side=tk.BOTTOM, pady=5)

root.mainloop()