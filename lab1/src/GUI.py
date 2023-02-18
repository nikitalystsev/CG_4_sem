import tkinter as tk


def change_param_root(root: tk.Tk) -> None:
    """
    Функция изменяет параметры окна
    :param root: окно
    :return: None
    """
    root.title("Лабораторная №1")
    root_width = root.winfo_screenwidth()
    root_height = root.winfo_screenheight() - 70
    root.geometry(f"{root_width}x{root_height}+0+0")
    root.resizable(width=True, height=True)
    # root.minsize(400, 500)
    # root.maxsize(1280, 1024)

    # root.config(bg="#7FFFD4")


def create_frame_plane(root: tk.Tk) -> tk.Frame:
    """
    Функция создает фрейм для плоскости (plane)
    :param root: окно
    :return: фрейм для плоскости
    """
    frame_plane_width = root.winfo_screenwidth() - 200
    frame_plane_height = root.winfo_screenheight()

    frame_plane = tk.Frame(
        root,
        width=frame_plane_width,
        height=frame_plane_height
    )

    return frame_plane


def create_frame_widgets(root: tk.Tk) -> tk.Frame:
    """
    Функция создает фрейм для виджетов (plane)
    :param root: окно
    :return: фрейм для виджетов
    """
    frame_widgets_width = 400
    frame_widgets_height = root.winfo_screenheight()

    frame_widgets = tk.Frame(
        root,
        width=frame_widgets_width,
        height=frame_widgets_height

    )

    return frame_widgets


def change_param_frame_widgets(frame_widgets: tk.Frame) -> None:
    """
    Функция изменяет параметры фрейма для виджетов
    :param frame_widgets: фрейм для виджетов
    :return: None
    """
    for i in range(4):
        frame_widgets.columnconfigure(index=i, weight=1, minsize=99)

    frame_widgets.config(bg="#C0C0C0")


def draw_canvas_plane(frame_plane: tk.Frame) -> tk.Canvas:
    """
    Функция размещает холст (canvas) для плоскости (plane) на главном окне
    :param frame_plane: окно
    :return: холст
    """
    canvas_plane_width = frame_plane.winfo_screenwidth() - 400
    canvas_plane_height = frame_plane.winfo_screenheight()

    canvas_plane = tk.Canvas(
        frame_plane,
        width=canvas_plane_width,
        height=canvas_plane_height,
        bg='#40E0D0'
    )

    return canvas_plane


def draw_label(frame: tk.Frame, text: str) -> tk.Label:
    """
    Функция создает виджет текста (label)
    :param frame: окно
    :param text: строка текста
    :return: виджет текста
    """
    label = tk.Label(
        frame,
        text=text,
        font=("Courier New", 14, 'bold'),
    )

    return label


def draw_entry(frame: tk.Frame) -> tk.Entry:
    """
    Функция создает виджет однострочного поля ввода (entry)
    :param frame: окно
    :return: виджет однострочного поля ввода
    """
    entry = tk.Entry(
        frame,
        width=15,
        relief=tk.SUNKEN,
        borderwidth=5,
        justify=tk.RIGHT,
        font=("Courier New", 14)
    )

    return entry


def draw_button(frame: tk.Frame, text: str) -> tk.Button:
    """
    Функция создает виджет кнопки (button)
    :param frame: окно
    :param text:  текст
    :return: виджет кнопки
    """
    button = tk.Button(
        frame,
        text=text,
        font=("Courier New", 12),
        relief=tk.RAISED
    )

    button.config(bg="#C0C0C0")

    return button


def draw_radiobutton(frame: tk.Frame, triangle_set, text: str) -> tk.Radiobutton:
    """
    Функция создает переключатель 2-х множеств треугольника для ввода
    :param frame: окно
    :param triangle_set: переменная tkinter
    :param text: значение переключателя
    :return: переключатель 2-х множеств треугольника для ввода
    """
    rbt = tk.Radiobutton(
        frame,
        text=text,
        value=text,
        variable=triangle_set,
        font=("Courier New", 12, 'bold')
    )

    return rbt


def draw_listbox(frame: tk.Frame) -> tk.Listbox:
    """
    Функция создаем виджет списка для отображения ранее введенных точек
    :param frame: окно
    :return: виджет списка
    """

    list_box_set = tk.Listbox(
        frame,
        width=35,
        height=23,
        borderwidth=5
    )

    return list_box_set


def build_interface() -> None:
    """
    Функция строит интерфейс
    :return: None
    """
    root = tk.Tk()

    change_param_root(root)

    # создали фреймы
    # -----------------------------------------------
    frame_plane = create_frame_plane(root)
    frame_plane.pack(side=tk.RIGHT)

    frame_widgets = create_frame_widgets(root)
    frame_widgets.pack()
    # -----------------------------------------------

    canvas_plane = draw_canvas_plane(frame_plane)
    canvas_plane.pack()

    change_param_frame_widgets(frame_widgets)

    lbl_add_point = draw_label(frame_widgets, "Добавить точку")
    lbl_add_point.grid(row=0, column=0, columnspan=4, sticky='wens')

    label_x = draw_label(frame_widgets, "X:")
    label_x.grid(row=1, column=0, sticky='wens')

    entry_x = draw_entry(frame_widgets)
    entry_x.grid(row=1, column=1, sticky='wens')

    label_y = draw_label(frame_widgets, "Y:")
    label_y.grid(row=1, column=2, sticky='wens')

    entry_y = draw_entry(frame_widgets)
    entry_y.grid(row=1, column=3, sticky='wens')

    btn_add_point = draw_button(frame_widgets, "Добавить точку")
    btn_add_point.grid(row=2, column=0, columnspan=4, sticky='wens')

    values = "Первое множество", "Второе множество"
    rbt_var = tk.StringVar(value=values[0])

    rbt = draw_radiobutton(frame_widgets, rbt_var, values[0])
    rbt.grid(row=3, column=0, columnspan=2, sticky='wens')

    rbt = draw_radiobutton(frame_widgets, rbt_var, values[1])
    rbt.grid(row=3, column=2, columnspan=2, sticky='wens')

    lbl_del_point = draw_label(frame_widgets, "Удалить точку")
    lbl_del_point.grid(row=4, column=0, columnspan=4, sticky='wens')

    label_n = draw_label(frame_widgets, "Номер точки:")
    label_n.grid(row=5, column=0, sticky='wens', columnspan=2)

    entry_n = draw_entry(frame_widgets)
    entry_n.grid(row=5, column=2, sticky='wens', columnspan=2)

    btn_del_point = draw_button(frame_widgets, "Удалить точку")
    btn_del_point.grid(row=6, column=0, columnspan=4, sticky='wens')

    empty_lbl = draw_label(frame_widgets, "")
    empty_lbl.grid(row=7, column=0, columnspan=4, sticky='wens')

    lbl_del_point = draw_label(frame_widgets, "Изменить точку")
    lbl_del_point.grid(row=8, column=0, columnspan=4, sticky='wens')

    label_n = draw_label(frame_widgets, "Номер точки:")
    label_n.grid(row=9, column=0, sticky='wens', columnspan=2)

    entry_n = draw_entry(frame_widgets)
    entry_n.grid(row=9, column=2, sticky='wens', columnspan=2)

    label_x = draw_label(frame_widgets, " New X:")
    label_x.grid(row=10, column=0, sticky='wens')

    entry_x = draw_entry(frame_widgets)
    entry_x.grid(row=10, column=1, sticky='wens')

    label_y = draw_label(frame_widgets, "New Y:")
    label_y.grid(row=10, column=2, sticky='wens')

    entry_y = draw_entry(frame_widgets)
    entry_y.grid(row=10, column=3, sticky='wens')

    btn_del_point = draw_button(frame_widgets, "Изменить точку")
    btn_del_point.grid(row=11, column=0, columnspan=4, sticky='wens')

    lbl_first_set = draw_label(frame_widgets, "Первое множество")
    lbl_first_set.grid(row=12, column=0, sticky='wens', columnspan=2)

    lbl_second_set = draw_label(frame_widgets, "Второе множество")
    lbl_second_set.grid(row=12, column=2, sticky='wens', columnspan=2)

    list_box_first_set = draw_listbox(frame_widgets)
    list_box_first_set.grid(row=13, column=0, columnspan=2, sticky='wens')

    list_box_second_set = draw_listbox(frame_widgets)
    list_box_second_set.grid(row=13, column=2, columnspan=2, sticky='wens')

    root.mainloop()
