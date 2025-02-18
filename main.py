# main.py
import customtkinter as ctk
from password_generator import generate_password
import json
from tkinter import messagebox
import pyperclip
from storage_window import show_storage

def main():
    # Инициализация главного окна
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Генератор паролей")

    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Устанавливаем размер окна
    window_width = 420
    window_height = 500

    # Вычисляем координаты для центрирования окна
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Устанавливаем геометрию окна
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Конфигурация layout
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Ввод длины пароля
    length_label = ctk.CTkLabel(master=frame, text="Длина пароля:")
    length_label.grid(row=0, column=0, pady=10, padx=10)
    length_entry = ctk.CTkEntry(master=frame)
    length_entry.grid(row=0, column=1, pady=10, padx=10)
    length_entry.insert(0, "14")

    # Обработка Ctrl + V для вставки текста в поле длины пароля
    def paste_length(event=None):
        try:
            text = root.clipboard_get()
            length_entry.insert("insert", text)
        except:
            pass

    length_entry.bind("<Control-v>", paste_length)

    # Чекбоксы для опций пароля
    uppercase_var = ctk.BooleanVar(value=True)
    digits_var = ctk.BooleanVar(value=True)
    special_var = ctk.BooleanVar(value=True)

    uppercase_check = ctk.CTkCheckBox(master=frame, text="Использовать заглавные буквы", variable=uppercase_var)
    uppercase_check.grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky="w")

    digits_check = ctk.CTkCheckBox(master=frame, text="Использовать цифры", variable=digits_var)
    digits_check.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="w")

    special_check = ctk.CTkCheckBox(master=frame, text="Использовать специальные символы", variable=special_var)
    special_check.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="w")

    # кнопка для генерации пароля
    def generate():
        try:
            length = int(length_entry.get())
            use_uppercase = uppercase_var.get()
            use_digits = digits_var.get()
            use_special_chars = special_var.get()

            password = generate_password(length, use_uppercase, use_digits, use_special_chars)
            password_entry.delete(0, ctk.END)
            password_entry.insert(0, password)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректная длина пароля")

    generate_button = ctk.CTkButton(master=frame, text="Сгенерировать", command=generate)
    generate_button.grid(row=4, column=0, columnspan=2, pady=20, padx=10)

    # вывод сгенерированного пароля
    password_label = ctk.CTkLabel(master=frame, text="Сгенерированный пароль:")
    password_label.grid(row=5, column=0, pady=10, padx=10)
    password_entry = ctk.CTkEntry(master=frame)
    password_entry.grid(row=5, column=1, pady=10, padx=10)

    # Ctrl + C для копирования пароля
    def copy_password(event=None):
        password = password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Скопировано", "Пароль скопирован в буфер обмена")
        else:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте пароль")

    # Ctrl + C к функции copy_password
    password_entry.bind("<Control-c>", copy_password)

    # стандартное поведение Ctrl + C для текстового поля
    def enable_ctrl_c(event):
        if event.state == 4 and event.keysym.lower() == 'c':
            password_entry.event_generate("<<Copy>>")

    password_entry.bind("<Control-KeyPress>", enable_ctrl_c)

    # кнопка для копирования пароля
    copy_button = ctk.CTkButton(master=frame, text="", width=20, height=20, command=copy_password)
    copy_button.grid(row=5, column=2, pady=10, padx=10)

    # ввод имени пароля
    name_label = ctk.CTkLabel(master=frame, text="Имя пароля:")
    name_label.grid(row=6, column=0, pady=10, padx=10)
    name_entry = ctk.CTkEntry(master=frame)
    name_entry.grid(row=6, column=1, pady=10, padx=10)

    # Ctrl + V для вставки текста в поле имени пароля
    def paste_name(event=None):
        try:
            text = root.clipboard_get()
            name_entry.insert("insert", text)
        except:
            pass

    name_entry.bind("<Control-v>", paste_name)

    # кнопка для сохранения пароля
    def save_password():
        password = password_entry.get()
        name = name_entry.get()
        if password and name:
            # загрузить существующие пароли
            try:
                with open("saved_passwords.json", "r", encoding="utf-8") as file:
                    passwords = json.load(file)
            except FileNotFoundError:
                passwords = []

            # добавить новый пароль
            passwords.append({"name": name, "password": password})

            # сохранить обновленные пароли с отключенным ensure_ascii
            with open("saved_passwords.json", "w", encoding="utf-8") as file:
                json.dump(passwords, file, indent=4, ensure_ascii=False)

            messagebox.showinfo("Сохранено", f"Пароль сохранен с именем: {name}")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите имя и сгенерируйте пароль")

    save_button = ctk.CTkButton(master=frame, text="Сохранить", command=save_password)
    save_button.grid(row=7, column=0, pady=20, padx=10)  # кнопка "Сохранить" в столбце 0

    # кнопка для открытия хранилища паролей
    storage_button = ctk.CTkButton(master=frame, text="Хранилище", command=show_storage)
    storage_button.grid(row=7, column=1, pady=20, padx=10)  # кнопка "Хранилище" в столбце 1

    root.mainloop()

if __name__ == '__main__':
    main()