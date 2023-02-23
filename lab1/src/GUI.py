from GUI_processing import *
from plane import *
from listpoints import *


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


def create_frame_plane(root: tk.Tk) -> tk.Frame:
    """
    Функция создает фрейм для плоскости (plane)
    :param root: окно
    :return: фрейм для плоскости
    """
    frame_plane_width = root.winfo_screenwidth() - 400
    frame_plane_height = root.winfo_screenheight() - 70

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

    frame_widgets = tk.Frame(
        root,
        width=frame_widgets_width,
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


def draw_plane(frame_plane: tk.Frame) -> PlaneCanvas:
    """
    Функция размещает холст (canvas) для плоскости (plane) на главном окне
    :param frame_plane: окно
    :return: холст
    """
    plane_width = frame_plane.winfo_screenwidth() - 400
    plane_height = frame_plane.winfo_screenheight() - 70

    plane = PlaneCanvas(
        y_min=0,
        y_max=10,
        x_min=0,
        master=frame_plane,
        width=plane_width,
        height=plane_height,
        bg="#FFFFFF"
    )

    return plane


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

    button.config(bg="#FFFFFF")

    return button


def draw_radiobutton(
        frame: tk.Frame,
        triangle_set: tk.StringVar,
        text: str) -> tk.Radiobutton:
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


def draw_listpoints(frame: tk.Frame, columns: tuple[str, str]) -> ListPoints:
    """
    Функция создает таблицу для отображения точек
    :param frame: окно
    :param columns: заголовки таблицы
    :return: фрейм
    """
    listpoints = ListPoints(
        frame,
        columns=columns,
        show="headings",
        height=14
    )

    return listpoints


def draw_set_scrollbar(frame: tk.Frame, listpoints: ListPoints) -> ttk.Scrollbar:
    """
    Функция создает полосу прокрутки для отображенных точек
    :param frame: окно
    :param listpoints: поле отображенных точек
    :return: полосу прокрутки
    """
    scrollbar = ttk.Scrollbar(frame, command=listpoints.yview)
    listpoints.config(yscrollcommand=scrollbar.set)

    return scrollbar


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

    plane = draw_plane(frame_plane)
    plane.pack()

    change_param_frame_widgets(frame_widgets)

    # виджеты для добавления точки
    # -----------------------------------------------
    lbl_add_point = draw_label(frame_widgets, "Добавить точку")
    lbl_add_point.grid(row=0, column=0, columnspan=4, sticky='wens')

    lbl_add_x = draw_label(frame_widgets, "X:")
    lbl_add_x.grid(row=1, column=0, sticky='wens')

    entry_add_x = draw_entry(frame_widgets)
    entry_add_x.grid(row=1, column=1, sticky='wens')

    lbl_add_y = draw_label(frame_widgets, "Y:")
    lbl_add_y.grid(row=1, column=2, sticky='wens')

    entry_add_y = draw_entry(frame_widgets)
    entry_add_y.grid(row=1, column=3, sticky='wens')

    btn_add_point = draw_button(frame_widgets, "Добавить точку")
    btn_add_point.config(
        command=lambda: add_point_to_listpoints(rbt_var, entry_add_x, entry_add_y,
                                                listpoints_set1, listpoints_set2, plane))
    btn_add_point.grid(row=2, column=0, columnspan=4, sticky='wens')
    # -----------------------------------------------

    # виджет переключения множеств
    # -----------------------------------------------
    values = "Первое множество", "Второе множество"
    rbt_var = tk.StringVar(value=values[0])

    rbt_set1 = draw_radiobutton(frame_widgets, rbt_var, values[0])
    rbt_set1.grid(row=3, column=0, columnspan=2, sticky='wens')

    rbt_set2 = draw_radiobutton(frame_widgets, rbt_var, values[1])
    rbt_set2.grid(row=3, column=2, columnspan=2, sticky='wens')
    # -----------------------------------------------

    # виджет удаления точки по номеру
    # -----------------------------------------------
    lbl_del_point = draw_label(frame_widgets, "Удалить точку")
    lbl_del_point.grid(row=4, column=0, columnspan=4, sticky='wens')

    lbl_n_del = draw_label(frame_widgets, "Номер точки:")
    lbl_n_del.grid(row=5, column=0, sticky='wens', columnspan=2)

    entry_n_del = draw_entry(frame_widgets)
    entry_n_del.grid(row=5, column=2, sticky='wens', columnspan=2)

    btn_del_point = draw_button(frame_widgets, "Удалить точку")
    btn_del_point.config(
        command=lambda: del_point_by_number(rbt_var, entry_n_del,
                                            listpoints_set1, listpoints_set2, plane))
    btn_del_point.grid(row=6, column=0, columnspan=4, sticky='wens')
    # -----------------------------------------------

    # виджеты изменения точки
    # -----------------------------------------------
    lbl_change_point = draw_label(frame_widgets, "Изменить точку")
    lbl_change_point.grid(row=7, column=0, columnspan=4, sticky='wens')

    lbl_n_change = draw_label(frame_widgets, "Номер точки:")
    lbl_n_change.grid(row=8, column=0, sticky='wens', columnspan=2)

    entry_n_change = draw_entry(frame_widgets)
    entry_n_change.grid(row=8, column=2, sticky='wens', columnspan=2)

    lbl_new_x = draw_label(frame_widgets, " New X:")
    lbl_new_x.grid(row=9, column=0, sticky='wens')

    entry_new_x = draw_entry(frame_widgets)
    entry_new_x.grid(row=9, column=1, sticky='wens')

    lbl_new_y = draw_label(frame_widgets, "New Y:")
    lbl_new_y.grid(row=9, column=2, sticky='wens')

    entry_new_y = draw_entry(frame_widgets)
    entry_new_y.grid(row=9, column=3, sticky='wens')

    btn_change_point = draw_button(frame_widgets, "Изменить точку")
    btn_change_point.config(
        command=lambda: change_point_by_number(rbt_var, entry_n_change,
                                               entry_new_x, entry_new_y,
                                               listpoints_set1, listpoints_set2, plane))
    btn_change_point.grid(row=10, column=0, columnspan=4, sticky='wens')
    # -----------------------------------------------

    # виджеты отображения точек
    # -----------------------------------------------
    lbl_set1 = draw_label(frame_widgets, "Первое множество")
    lbl_set1.grid(row=11, column=0, sticky='wens', columnspan=2)

    lbl_set2 = draw_label(frame_widgets, "Второе множество")
    lbl_set2.grid(row=11, column=2, sticky='wens', columnspan=2)

    columns = "number", "point"

    frame_sets = tk.Frame(root, bg="#800080")
    frame_sets.pack()

    frame_set1 = tk.Frame(frame_sets, bg="#FF0000")
    frame_set1.pack(side=tk.LEFT, fill=tk.Y)

    frame_set2 = tk.Frame(frame_sets, bg="#FF0000")
    frame_set2.pack(side=tk.RIGHT)

    listpoints_set1 = draw_listpoints(frame_set1, columns)
    listpoints_set1.pack(side=tk.LEFT, fill=tk.Y)

    scroll_set1 = draw_set_scrollbar(frame_set1, listpoints_set1)
    scroll_set1.pack(side=tk.RIGHT, fill=tk.Y)

    listpoints_set2 = draw_listpoints(frame_set2, columns)
    listpoints_set2.pack(side=tk.LEFT)

    scroll_set2 = draw_set_scrollbar(frame_set2, listpoints_set2)
    scroll_set2.pack(side=tk.RIGHT, fill=tk.Y)

    # -----------------------------------------------

    frame_tasks = create_frame_widgets(root)
    frame_tasks.pack()

    change_param_frame_widgets(frame_tasks)

    btn_clean = draw_button(frame_tasks, "Очистить все поля")
    btn_clean.grid(row=0, column=0, columnspan=2, sticky='wens')

    btn_build_trian = draw_button(frame_tasks, "Построить треуг-к")
    btn_build_trian.grid(row=0, column=2, columnspan=2, sticky='wens')

    btn_print_res = draw_button(frame_tasks, "Вывести результаты")
    btn_print_res.grid(row=1, column=0, columnspan=2, sticky='wens')

    btn_task = draw_button(frame_tasks, "Условие задачи")
    btn_task.grid(row=1, column=2, columnspan=2, sticky='wens')
    # -----------------------------------------------

    # работа с plane
    # -----------------------------------------------
    plane.draw_axis()

    root.mainloop()
