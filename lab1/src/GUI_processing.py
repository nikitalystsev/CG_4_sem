import tkinter as tk
from tkinter import messagebox


def is_float(x: str) -> bool:
    """
    Функция проверяет, число ли переданный параметр.
    :param x:
    :return: True, если число, False иначе
    """
    try:
        x = float(x)
    except (ValueError, TypeError):
        messagebox.showwarning(
            "Некорректный ввод!",
            "Введены недопустимые символы!"
        )
        return False

    return True


def check_input_point(point: tuple[str, str]) -> bool:
    """
    Функция проверяет введенную точку на корректность
    :param point: точка
    :return: True, если точка валидная, False иначе
    """
    x, y = point[0], point[1]

    if not is_float(x) or not is_float(y):
        return False

    return True


def get_point(entry_x: tk.Entry, entry_y: tk.Entry) -> (str, str):
    """
    Функция получает точку с однострочных полей ввода координат
    :param entry_x: поле ввода абсциссы
    :param entry_y: поле вода ординаты
    :return:
    """
    x = entry_x.get()
    y = entry_y.get()

    return x, y


def add_point_to_listbox(
        entry_x: tk.Entry,
        entry_y: tk.Entry,
        listbox: tk.Listbox) -> None:
    """
    Функция добавляет точку в listbox
    :param entry_x: поле ввода абсциссы
    :param entry_y: поле ввода ординаты
    :param listbox: поле, куда добавится точка
    :return:
    """
    x, y = get_point(entry_x, entry_y)

    if check_input_point((x, y)):
        listbox.insert(0, str((float(x), float(y))))
