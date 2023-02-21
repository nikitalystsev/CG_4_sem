import tkinter as tk
from tkinter import messagebox
from plane import *
from listpoints import *
from checks import *


def is_int(x: str) -> bool:
    """
    Функция проверяет, является ли строка целым числом
    :param x: строка
    :return: True, если целое число, False иначе
    """
    if check_int(x):
        return True

    messagebox.showwarning(
        "Некорректный ввод!",
        "Введены некорректные данные для номера точки!"
    )

    return False


def is_float(x: str) -> bool:
    """
    Функция проверяет, число ли переданный параметр.
    :param x:
    :return: True, если число, False иначе
    """
    if check_float(x):
        return True

    messagebox.showwarning(
        "Некорректный ввод!",
        "Введены недопустимые символы!"
    )

    return False


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


def add_point_to_listpoints(
        string_var: tk.StringVar, entry_x: tk.Entry,
        entry_y: tk.Entry, set1: ListPoints,
        set2: ListPoints, plane: PlaneCanvas) -> None:
    """
    Функция вставляет в поле в зависимости от выбора множества
    :param string_var: первое или второе множество
    :param entry_x: поле ввода абсциссы
    :param entry_y: поле ввода ординаты
    :param set1: поле отображения точек первого множества
    :param set2: поле отображения точек второго множества
    :param plane: плоскость
    :return: None
    """
    x, y = get_point(entry_x, entry_y)

    if check_input_point((x, y)):
        x, y = float(x), float(y)
        if string_var.get() == "Первое множество":
            set1.add_point((x, y))
            plane.draw_point(x, y)
        else:
            set2.add_point((x, y))
            plane.draw_point(x, y)


def del_if_valid_num(table: ListPoints, plane: PlaneCanvas, n) -> None:
    """
    Функция удаляет точку по валидному номеру
    :param table: таблица точек
    :param plane: плоскость
    :param n: номер точки
    :return: None
    """
    if table.is_valid_number(n):
        table.del_point(n)
        plane.del_point(n)
        return

    messagebox.showwarning("Неверный номер точки!",
                           "Точки с введенным номером не существует!")


def del_point_by_number(
        string_var: tk.StringVar,
        entry_n: tk.Entry,
        set1: ListPoints,
        set2: ListPoints,
        plane: PlaneCanvas) -> None:
    """
    Функция удаляет из поля точку в зависимости от выбора множества
    :param string_var: первое или второе множество
    :param entry_n: поле ввода номера
    :param set1: поле отображения точек первого множества
    :param set2: поле отображения точек второго множества
    :param plane: плоскость
    :return: None
    """
    n = entry_n.get()

    if is_int(n):
        n = int(n)
        if string_var.get() == "Первое множество":
            del_if_valid_num(set1, plane, n)
        else:
            del_if_valid_num(set2, plane, n)


def change_if_valid_num(
        table: ListPoints,
        num: int,
        new_x: float,
        new_y: float,
        plane: PlaneCanvas) -> None:
    """
    Функция изменяет точку по валидному номеру
    :param table: окно
    :param num: номер точки
    :param new_x: новая абсцисса точки
    :param new_y: новая ордината точки
    :param plane: плоскость
    :return: None
    """
    if table.is_valid_number(num):
        table.change_point(num, new_x, new_y)
        plane.change_point(num, new_x, new_y)
        return

    messagebox.showwarning("Неверный номер точки!",
                           "Точки с введенным номером не существует!")


def change_point_by_number(
        string_var: tk.StringVar, entry_n: tk.Entry,
        entry_x: tk.Entry, entry_y: tk.Entry,
        set1: ListPoints, set2: ListPoints, plane: PlaneCanvas) -> None:
    """
    Функция изменяет точку в одном из множеств
    :param string_var: первое или второе множество
    :param entry_n: поле ввода номера
    :param entry_x: поле ввода новой абсциссы точки
    :param entry_y: поле ввода новой ординаты точки
    :param set1: поле отображения точек первого множества
    :param set2: поле отображения точек второго множества
    :param plane: плоскость
    :return: None
    """
    n = entry_n.get()
    x, y = get_point(entry_x, entry_y)

    if is_int(n) and check_input_point((x, y)):
        n, x, y = int(n), float(x), float(y)
        if string_var.get() == "Первое множество":
            change_if_valid_num(set1, n, x, y, plane)
        else:
            change_if_valid_num(set2, n, x, y, plane)
