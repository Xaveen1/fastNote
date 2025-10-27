import tkinter as tk
from tkinter import filedialog

# --- Сохранение и открытие ---
def save_to_file():
    text = textbox.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        lbl.config(text=f"💾 Сохранено: {file_path}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        textbox.delete("1.0", "end")
        textbox.insert("1.0", content)
        lbl.config(text=f"📂 Открыто: {file_path}")

# --- Автонумерация ---
def handle_enter(event):
    text = textbox.get("1.0", tk.END).strip().split("\n")
    if text:
        last_line = text[-1]
        if last_line.split('.')[0].isdigit():
            next_number = int(last_line.split('.')[0]) + 1
            textbox.insert(tk.END, f"\n{next_number}. ")
            return "break"

# --- Мини-калькулятор ---
hint = None

def check_expression(event=None):
    global hint
    line = textbox.get("insert linestart", "insert lineend")
    if "=" in line:
        try:
            expr = line.split("=")[0].strip()
            answer = eval(expr)
            hint = str(answer)
            lbl.config(text=f"Подсказка: {hint}  •  Нажми TAB, чтобы вставить")
        except:
            hint = None
            lbl.config(text="")
    else:
        hint = None
        lbl.config(text="")

def insert_hint(event=None):
    global hint
    if hint:
        textbox.insert("insert", hint)
        hint = None
        return "break"

# --- Автосохранение ---
def autosave():
    text = textbox.get("1.0", "end-1c")
    with open("autosave.txt", "w", encoding="utf-8") as f:
        f.write(text)
    window.after(10000, autosave)

# --- Интерфейс ---
window = tk.Tk()
window.title("fastNote 0.16")
window.geometry("750x600")
window.config(bg="#1e1e1e")

# Панель
toolbar = tk.Frame(window, bg="#2b2b2b")
toolbar.pack(fill='x', side='top')

save_btn = tk.Button(toolbar, text="💾 Сохранить", command=save_to_file, bg="#3a3a3a", fg="white", relief="flat")
save_btn.pack(side='right', padx=6, pady=4)

open_btn = tk.Button(toolbar, text="📂 Открыть", command=open_file, bg="#3a3a3a", fg="white", relief="flat")
open_btn.pack(side='right', padx=6, pady=4)

# Текстовое поле
textbox = tk.Text(
    window,
    padx=12,
    pady=12,
    font=("JetBrains Mono", 18),
    bg="#1e1e1e",
    fg="#e0e0e0",
    insertbackground="#00ff88",  # зелёный курсор
    relief="flat",
)
textbox.pack(expand=True, fill="both", padx=8, pady=8)

# Нижняя строка
lbl = tk.Label(window, text="", bg="#1e1e1e", fg="#aaaaaa", anchor="w")
lbl.pack(fill='x', padx=10, pady=(0, 10))

# Привязки
textbox.bind("<KeyRelease>", check_expression)
textbox.bind("<Tab>", insert_hint)
textbox.bind("<Return>", handle_enter)

autosave()

try:
    icon = tk.PhotoImage(file=r"C:\Users\hamzi\OneDrive\Desktop\fastNote\icon.png")
    window.iconphoto(False, icon)
except:
    pass

window.mainloop()
