import tkinter as tk
from tkinter import filedialog

from entirely import entirely_back


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Disk Info Collector")

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hosts_file_frame = tk.Frame(self)
        self.hosts_file_frame.pack()

        self.hosts_file_label = tk.Label(self.hosts_file_frame, text="Взять имена хостов из:", font=("Arial", 12))
        self.hosts_file_label.pack(side=tk.LEFT)

        self.hosts_file_entry = tk.Entry(self.hosts_file_frame, width=40, font=("Arial", 12))
        self.hosts_file_entry.pack(side=tk.LEFT)

        self.browse_hosts_file_button = tk.Button(self.hosts_file_frame, relief=tk.RIDGE, borderwidth=2)
        self.browse_hosts_file_button["text"] = "Выбрать файл"
        self.browse_hosts_file_button["command"] = self.browse_hosts_file
        self.browse_hosts_file_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.browse_hosts_file_button.config(height=1, width=20, font=("Arial", 12))

        self.output_folder_frame = tk.Frame(self)
        self.output_folder_frame.pack()

        self.output_folder_label = tk.Label(self.output_folder_frame, text="Сохранить в :", font=("Arial", 12))
        self.output_folder_label.pack(side=tk.LEFT)

        self.output_folder_entry = tk.Entry(self.output_folder_frame, width=40, font=("Arial", 12))
        self.output_folder_entry.pack(side=tk.LEFT)

        self.browse_output_folder_button = tk.Button(self.output_folder_frame, relief=tk.RIDGE, borderwidth=2)
        self.browse_output_folder_button["text"] = "Выбрать папку"
        self.browse_output_folder_button["command"] = self.browse_output_folder
        self.browse_output_folder_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.browse_output_folder_button.config(height=1, width=20, font=("Arial", 12))

        self.run_button = tk.Button(self, relief=tk.RIDGE, borderwidth=2)
        self.run_button["text"] = "Начать"
        self.run_button["command"] = self.check_and_run
        self.run_button.pack(pady=10)
        self.run_button.config(height=1, width=10, font=("Arial", 12))
        self.run_button.config(state="disabled")

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack()

    def browse_hosts_file(self):
        filename = filedialog.askopenfilename()
        self.hosts_file_entry.delete(0, tk.END)
        self.hosts_file_entry.insert(0, filename)
        self.check_entries()

    def browse_output_folder(self):
        foldername = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, foldername)
        self.check_entries()

    def check_entries(self):
        if self.hosts_file_entry.get() and self.output_folder_entry.get():
            self.run_button.config(state="normal")
        else:
            self.run_button.config(state="disabled")

    def check_and_run(self):
        if not self.hosts_file_entry.get() or not self.output_folder_entry.get():
            self.status_label["text"] = "Выберите файл и папку!"
            return

        try:
            entirely_back.run(self.hosts_file_entry.get(), self.output_folder_entry.get())
            self.status_label["text"] = "Файлы сформированы!"
        except Exception as e:
            print(f"Error: {e}")
            self.status_label["text"] = "Ошибка при формировании файлов"

def main(root):
    app = App(root)
    root.mainloop()
