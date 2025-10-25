import tkinter as tk
from tkinter import filedialog

# --- Сохранение и открытие ---
def save_to_file():
    text = textbox.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        lbl.config(text=f"Сохранено: {file_path}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        textbox.delete("1.0", "end")
        textbox.insert("1.0", content)
        lbl.config(text=f"Открыто: {file_path}")

# --- Мини-калькулятор ---
hint = None

def check_expression(event=None):
    global hint
    line = textbox.get("insert linestart", "insert lineend")
    if "=" in line:
        try:
            expr = line.split("=")[0].strip()  # убираем пробелы
            answer = eval(expr)                # считаем результат
            hint = str(answer)
            lbl.config(text=f"Подсказка: {hint}, нажми TAB, чтобы вставить ответ")
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
        return "break"


# --- Окно ---
window = tk.Tk()
window.title("fastNote")
window.geometry("700x600")
window.config(bg="#f9f9f9")

# --- Панель кнопок ---
toolbar = tk.Frame(window, bg="#cff1ff")
toolbar.pack(fill='x', side='top')

save_btn = tk.Button(toolbar, text="💾 Сохранить", command=save_to_file)
save_btn.pack(side='right', padx=4, pady=4)

open_btn = tk.Button(toolbar, text="📂 Открыть", command=open_file)
open_btn.pack(side='right', padx=4, pady=4)

# --- Текстовое поле ---
textbox = tk.Text(window, padx=10, pady=10, font=("Consolas", 12), bg="#f9f9f9", fg="#333")
textbox.pack(expand=True, fill="both", padx=8, pady=8)

# --- Label для подсказок ---
lbl = tk.Label(window, text="", bg="#f9f9f9", fg="#555")
lbl.pack(pady=(0, 8))

# --- Привязка событий ---
textbox.bind("<KeyRelease>", check_expression)
textbox.bind("<Tab>", insert_hint)

# --- Автосохранение каждые 10 секунд ---
def autosave():
    text = textbox.get("1.0", "end-1c")
    with open("autosave.txt", "w", encoding="utf-8") as f:
        f.write(text)
    window.after(10000, autosave)

autosave()

icon = tk.PhotoImage(file=r"C:\Users\hamzi\OneDrive\Desktop\fastNote\icon.png")
window.iconphoto(False, icon)

window.mainloop()


