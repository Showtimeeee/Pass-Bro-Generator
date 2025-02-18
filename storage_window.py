import customtkinter as ctk
import json
import pyperclip
from tkinter import messagebox, Menu

def show_storage():
    # новое окно
    storage_window = ctk.CTkToplevel()
    storage_window.title("Хранилище паролей")
    storage_window.geometry("500x400")

    # загружаем пароли из файла
    try:
        with open("saved_passwords.json", "r", encoding="utf-8") as file:
            passwords = json.load(file)
    except FileNotFoundError:
        passwords = []

    # текстовое поле для отображения паролей
    text_area = ctk.CTkTextbox(master=storage_window, wrap="none")
    text_area.pack(pady=20, padx=20, fill="both", expand=True)

    # вставить пароли в текстовое поле
    for entry in passwords:
        text_area.insert("end", f"Имя: {entry['name']}\nПароль: {entry['password']}\n\n")

    # текстовое поле нередактируемое
    text_area.configure(state="disabled")

    # для копирования выделенного текста
    def copy_text(event=None):
        try:
            # редактирование для копирования
            text_area.configure(state="normal")
            selected_text = text_area.get("sel.first", "sel.last")  # получить выделенный текст
            if selected_text:
                pyperclip.copy(selected_text)
                messagebox.showinfo("Скопировано", "Текст скопирован в буфер обмена")
            # текстовое поле в состояние "disabled"
            text_area.configure(state="disabled")
        except:
            messagebox.showerror("Ошибка", "Ничего не выделено")

    # Ctrl + C к функции copy_text
    text_area.bind("<Control-c>", copy_text)

    # Ctrl + C для текстового поля
    def enable_ctrl_c(event):
        if event.state == 4 and event.keysym.lower() == 'c':  # Проверяем, что нажаты Ctrl + C
            copy_text()

    text_area.bind("<Control-KeyPress>", enable_ctrl_c)

    # функция для вставки текста
    def paste_text(event=None):
        try:
            text = storage_window.clipboard_get()
            text_area.configure(state="normal")
            text_area.insert("insert", text)
            text_area.configure(state="disabled")
        except:
            pass

    # Ctrl + V к функции paste_text
    text_area.bind("<Control-v>", paste_text)

    # для очистки списка паролей
    def clear_passwords():
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить хранилище?")
        if confirm:
            # Очищаем файл saved_passwords.json
            with open("saved_passwords.json", "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
            # Очищаем текстовое поле
            text_area.configure(state="normal")
            text_area.delete("1.0", "end")
            text_area.configure(state="disabled")
            messagebox.showinfo("Успех", "Хранилище очищено")

    # кнопка для очистки хранилища
    clear_button = ctk.CTkButton(master=storage_window, text="Очистить", command=clear_passwords)
    clear_button.pack(pady=10)

    # контекстное меню для копирования
    def copy_text_menu(event):
        copy_text()

    # контекстное меню с использованием tkinter.Menu
    context_menu = Menu(storage_window, tearoff=0)
    context_menu.add_command(label="Копировать", command=copy_text)

    # привязываем контекстное меню к текстовому полю
    def show_context_menu(event):
        context_menu.tk_popup(event.x_root, event.y_root)

    text_area.bind("<Button-3>", show_context_menu)  # Windows/Linux
    text_area.bind("<Button-2>", show_context_menu)  # macOS