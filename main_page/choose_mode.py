import tkinter as tk
import os
import sys
import entirely.entirely_front as entirely_front
import fractional.fractional_front as fractional_front


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



def run_fractional():
    fractional_front.App(root)
    fractional_button.config(state='disabled')

def run_entirely():
    entirely_front.App(root)
    entirely_button.config(state='disabled')

root = tk.Tk()
root.title("Запуск файлов")

root.maxsize(1000, 1000)
root.minsize(400, 400)

button_frame = tk.Frame(root)
button_frame.pack()

fractional_button = tk.Button(button_frame, text="Ввод вручную", command=run_fractional, relief=tk.RIDGE, borderwidth=2, height=1, width=40, font=("Arial", 12))
fractional_button.pack(pady=(0, 10))

entirely_button = tk.Button(button_frame, text="Ввод из файла", command=run_entirely, relief=tk.RIDGE, borderwidth=2, height=1, width=40, font=("Arial", 12))
entirely_button.pack(pady=(10, 0))

root.mainloop()