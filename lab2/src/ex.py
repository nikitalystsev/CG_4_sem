import tkinter as tk
from tkinter import messagebox


def show_message():
    message = tk.messagebox.Message(root, text="Текст сообщения", icon="info", parent=root, type="ok", bitmap="")
    message.show()


root = tk.Tk()
button = tk.Button(root, text="Нажми меня!", command=show_message)
button.pack()
root.mainloop()
