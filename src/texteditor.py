import tkinter as tk
from tkinter import filedialog, messagebox, font


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                content = text_area.get(1.0, tk.END)
                file.write(content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")


def find_text():
    text_area.tag_remove('highlight', '1.0', tk.END)
    search_word = search_entry.get()
    if search_word:
        start_pos = '1.0'
        while True:
            start_pos = text_area.search(search_word, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_word)}c"
            text_area.tag_add('highlight', start_pos, end_pos)
            text_area.tag_config('highlight', background='yellow', foreground='black')
            start_pos = end_pos


def undo():
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass


def redo():
    try:
        text_area.edit_redo()
    except tk.TclError:
        pass


def cut():
    text_area.event_generate("<<Cut>>")


def copy():
    text_area.event_generate("<<Copy>>")


def paste():
    text_area.event_generate("<<Paste>>")


def select_all():
    text_area.tag_add('sel', '1.0', tk.END)


# Создание основного окна
root = tk.Tk()
root.title("Текстовый редактор с поиском")
root.geometry("900x650")
root.configure(bg="#f0f0f0")

# Шрифт для текста
text_font = font.Font(family="Consolas", size=12)

# Меню
menu_bar = tk.Menu(root)

# Меню Файл
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Открыть", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Сохранить", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)
menu_bar.add_cascade(label="Файл", menu=file_menu)

# Меню Правка
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Отменить", command=undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Повторить", command=redo, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Вырезать", command=cut, accelerator="Ctrl+X")
edit_menu.add_command(label="Копировать", command=copy, accelerator="Ctrl+C")
edit_menu.add_command(label="Вставить", command=paste, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Выделить всё", command=select_all, accelerator="Ctrl+A")
menu_bar.add_cascade(label="Правка", menu=edit_menu)

root.config(menu=menu_bar)

# Поиск
search_frame = tk.Frame(root, bg="#d9d9d9", pady=8, padx=8)
search_frame.pack(fill='x')

search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.pack(side='left', padx=(0, 10), pady=4, fill='x', expand=True)

search_button = tk.Button(search_frame, text="Найти", command=find_text, bg="#4caf50", fg="white",
                          font=("Arial", 11, "bold"), activebackground="#45a049", padx=10, pady=5)
search_button.pack(side='right')

# Текстовое поле с полосой прокрутки
text_frame = tk.Frame(root)
text_frame.pack(expand=1, fill='both', padx=10, pady=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side='right', fill='y')

text_area = tk.Text(text_frame, wrap='word', undo=True, font=text_font, yscrollcommand=scrollbar.set, bg="white",
                    fg="black", selectbackground="#c0c0ff", relief=tk.FLAT, bd=2)
text_area.pack(expand=1, fill='both')

scrollbar.config(command=text_area.yview)

# Горячие клавиши
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-f>', lambda event: find_text())
root.bind('<Control-z>', lambda event: undo())
root.bind('<Control-y>', lambda event: redo())
root.bind('<Control-x>', lambda event: cut())
root.bind('<Control-c>', lambda event: copy())
root.bind('<Control-v>', lambda event: paste())
root.bind('<Control-a>', lambda event: select_all())

root.mainloop()