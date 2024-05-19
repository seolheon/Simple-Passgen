import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
import random
import string

def generate_password(length=12, complexity='medium'):
    if complexity == 'low':
        characters = string.ascii_letters
    elif complexity == 'medium':
        characters = string.ascii_letters + string.digits
    elif complexity == 'high':
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        raise ValueError("Некорректная сложность пароля")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        self.style = Style("darklygreen")

        self.main_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.password_length_label = ttk.Label(self.main_frame, text="Длина пароля:")
        self.password_length_label.grid(row=0, column=0, pady=(10, 0), sticky="w")

        self.password_length_value = 12  # Добавим атрибут для хранения текущей длины пароля

        self.length_label = ttk.Label(self.main_frame, text=f"Текущая длина: { self.password_length_value}")
        self.length_label.grid(row=2, column=0, pady=(0, 10), sticky="w")

        self.password_length_slider = ttk.Scale(self.main_frame, from_=6, to=20, orient="horizontal", length=14 * 20, command=self.update_length_label)
        self.password_length_slider.set(12)
        self.password_length_slider.grid(row=1, column=0, pady=0, sticky="ew")

        self.password_complexity_label = ttk.Label(self.main_frame, text="Сложность:")
        self.password_complexity_label.grid(row=3, column=0, pady=(10, 0), sticky="w")

        self.password_complexity_combobox = ttk.Combobox(self.main_frame, values=["low", "medium", "high"], state="readonly")
        self.password_complexity_combobox.set("medium")
        self.password_complexity_combobox.grid(row=4, column=0, pady=0, sticky="ew")

        self.generate_button = ttk.Button(self.main_frame, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_button.grid(row=5, column=0, pady=10, sticky="ew")

        self.generated_password_label = ttk.Label(self.main_frame, text="Сгенерированный пароль:")
        self.generated_password_label.grid(row=6, column=0, pady=(10, 0), sticky="w")

        self.generated_password_entry = ttk.Entry(self.main_frame, state="readonly")
        self.generated_password_entry.grid(row=7, column=0, pady=0, sticky="ew")

        self.copy_button = ttk.Button(self.main_frame, text="Копировать в буфер", command=self.copy_to_clipboard)
        self.copy_button.grid(row=8, column=0, pady=10, sticky="ew")

        self.save_button = ttk.Button(self.main_frame, text="Сохранить в файл", command=self.save_to_file)
        self.save_button.grid(row=9, column=0, pady=10, sticky="ew")

        self.clear_button = ttk.Button(self.main_frame, text="Очистить поле", command=self.clear_generated_passwords)
        self.clear_button.grid(row=10, column=0, pady=(10, 0), sticky="ew")

        self.generated_passwords_text = tk.Text(self.main_frame, height=5, state="disabled", wrap="word")
        self.generated_passwords_text.grid(row=11, column=0, pady=0, sticky="ew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(11, weight=1)

    def update_length_label(self, value):
        self.password_length_value = int(float(value))
        self.length_label.configure(text=f"Текущая длина: {self.password_length_value}")

    def generate_password(self):
        length = self.password_length_value
        complexity = self.password_complexity_combobox.get()
        password = generate_password(length, complexity)
        self.generated_password_entry.configure(state="normal")
        self.generated_password_entry.delete(0, "end")
        self.generated_password_entry.insert(0, password)
        self.generated_password_entry.configure(state="readonly")

        self.generated_passwords_text.configure(state="normal")
        self.generated_passwords_text.insert("end", password + "\n")
        self.generated_passwords_text.configure(state="disabled")

    def copy_to_clipboard(self):
        password = self.generated_password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Копирование в буфер", "Пароль скопирован в буфер обмена.")

    def save_to_file(self):
        passwords = self.generated_passwords_text.get("1.0", "end-1c")
        if passwords:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(passwords)
                messagebox.showinfo("Сохранение в файл", f"Пароли сохранены в файл: {file_path}")
        else:
            messagebox.showinfo("Сохранение в файл", "Нет сгенерированных паролей для сохранения.")

    def clear_generated_passwords(self):
        self.generated_passwords_text.configure(state="normal")
        self.generated_passwords_text.delete("1.0", "end")
        self.generated_passwords_text.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
