import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


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


def get_index(treeview: ttk.Treeview) -> int:
    """
    Функция возвращает индекс для следующей добавляемой точки
    :param treeview: окно
    :return: индекс
    """
    count = 1
    for _ in treeview.get_children(""):
        count += 1

    return count


def add_point_to_desired(
        string_var: tk.StringVar,
        entry_x: tk.Entry,
        entry_y: tk.Entry,
        first_set: ttk.Treeview,
        second_set: ttk.Treeview) -> None:
    """
    Функция вставляет в поле в зависимости от выбора множества
    :param string_var: первое или второе множество
    :param entry_x: поле ввода абсциссы
    :param entry_y: поле ввода ординаты
    :param first_set: поле отображения точек первого множества
    :param second_set: поле отображения точек второго множества
    :return: None
    """
    x, y = get_point(entry_x, entry_y)

    if check_input_point((x, y)):
        x, y = float(x), float(y)
        if string_var.get() == "Первое множество":
            c = get_index(first_set)
            first_set.insert("", tk.END, values=(c, str((x, y))))
        else:
            c = get_index(second_set)
            second_set.insert("", tk.END, values=(c, str((x, y))))


def is_int(x: str) -> bool:
    """
    Функция проверяет, является ли строка целым числом
    :param x: строка
    :return: True, если целое число, False иначе
    """
    try:
        x = int(x)
    except (ValueError, TypeError):
        messagebox.showwarning(
            "Некорректный ввод!",
            "Введены некорректные данные для номера точки!"
        )
        return False

    return True


def is_valid_number(treeview: ttk.Treeview, num: int) -> bool:
    """
    Функция проверяет, является ли номер точки валидным для удаления
    :param treeview: окно
    :param num: номер точки
    :return: True, если валидный номер, False иначе
    """
    for k in treeview.get_children(""):
        if int(treeview.set(k, 0)) == num:
            return True

    return False


def recalculation_index(treeview: ttk.Treeview) -> None:
    """
    Функция пересчитывает индексы номеров точек
    после очередного удаления
    :param treeview:
    :return:
    """
    i = 1
    for k in treeview.get_children(""):
        treeview.set(k, 0, i)
        i += 1


def del_if_valid_num(treeview: ttk.Treeview, num: int) -> None:
    """
    Функция удаляет точку по валидному номеру
    :param treeview: окно
    :param num: номер точки
    :return: None
    """
    if is_valid_number(treeview, num):
        for k in treeview.get_children(""):
            if int(treeview.set(k, 0)) == num:
                treeview.delete(k)

        recalculation_index(treeview)
    else:
        messagebox.showwarning("Неверный номер точки!",
                               "Точки с введенным номером не существует!")


def del_point_by_number(
        string_var: tk.StringVar,
        entry_n: tk.Entry,
        first_set: ttk.Treeview,
        second_set: ttk.Treeview) -> None:
    """
    Функция удаляет из поля точку в зависимости от выбора множества
    :param string_var: первое или второе множество
    :param entry_n: поле ввода номера
    :param first_set: поле отображения точек первого множества
    :param second_set: поле отображения точек второго множества
    :return: None
    """
    n = entry_n.get()

    if is_int(n):
        n = int(n)
        if string_var.get() == "Первое множество":
            del_if_valid_num(first_set, n)
        else:
            del_if_valid_num(second_set, n)
