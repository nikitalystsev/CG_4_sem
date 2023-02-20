from tkinter import ttk
from tkinter import *


class ListPoints(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        style_head = ttk.Style()
        style_head.configure("Treeview.Heading", font=("Courier New", 12))
        style_head.configure("Treeview", font=("Courier New", 9))
        self.heading(column="number", text="№")
        self.heading(column="point", text="Точка")
        self.column("#1", width=30, anchor='center')
        self.column("#2", width=148, anchor='center')

    def is_valid_number(self, n) -> bool:
        for k in self.get_children(""):
            if int(self.set(k, 0)) == int(n):
                return True
        return False

    def add_point(self, point):
        index = len(self.get_children()) + 1
        self.insert("", END, values=(index, str(point)))

    def del_point(self, n):
        for k in self.get_children(""):
            if int(self.set(k, 0)) == n:
                self.delete(k)
        self.recalc_index()

    def change_point(self, n, new_x, new_y):
        for k in self.get_children(""):
            if int(self.set(k, 0)) == int(n):
                self.item(k, values=(n, str((float(new_x), float(new_y)))))

    def recalc_index(self):
        i = 1
        for k in self.get_children(""):
            self.set(k, 0, i)
            i += 1

    def clear_points(self):
        for item in self.get_children():
            self.delete(item)
