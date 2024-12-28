import tkinter as tk
from tkinter import filedialog

from fractional import fractional_back
from fractional.fractional_back import save_file, execute_winrm_command


class App:
    def __init__(self, master):
        self.master = master
        master.title("Disk Info Collector")

        self.label = tk.Label(master, text="Введите имя хоста:", font=("Arial", 12))
        self.label.pack(padx=5, pady=5)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=5, pady=5)

        self.execute_button = tk.Button(master, text="Получить информацию о дисках", command=self.execute_remote_host,
                                         relief=tk.RIDGE, borderwidth=2, height=1, width=40, font=("Arial", 12))
        self.execute_button.pack(padx=5, pady=5)

        self.save_button = tk.Button(master, text="Сохранить данные в файл", command=None,
                                     relief=tk.RIDGE, borderwidth=2, height=1, width=40, font=("Arial", 12))
        self.save_button.pack(padx=5, pady=5)

        self.directory = None
        self.hostname = None
        self.status_label = tk.Label(master, text="", font=("Arial", 12))
        self.status_label.pack(padx=5, pady=5)

        self.info_text = tk.Text(master, width=300, height=300)
        self.info_text.pack(padx=5, pady=5)

    def execute_remote_host(self):
        self.hostname = self.entry.get()
        execute_winrm_command(self.hostname, self.display_info)

    def display_info(self, result):
        if result.startswith("Ошибка:"):
            self.status_label.config(text="Ошибка")
        else:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, result)

            self.save_button.config(command=lambda: self.ask_directory_and_save_file(self.hostname, result))

    def ask_directory_and_save_file(self, hostname, result):
        self.directory = filedialog.askdirectory()
        if self.directory:
            try:
                save_file(hostname, self.directory, result)
                self.status_label.config(text=f"Файл сохранен. Путь: {self.directory}")
            except Exception as e:
                self.status_label.config(text="Ошибка")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()