from plane import *
from listpoints import *
from checks import *


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()
        self.title("Лабораторная №2")

        root_width = self.winfo_screenwidth()
        root_height = self.winfo_screenheight() - 65
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # создал фреймы для всего
        # -----------------------------------------------
        self.frame_plane = self.create_frame_plane()
        self.frame_plane.pack(side=tk.RIGHT)
        self.frame_widgets = self.create_frame_widgets()
        self.frame_widgets.pack()
        # -----------------------------------------------
        self.plane = self.draw_plane()
        self.plane.pack()

        # виджеты для переноса изображения
        # -----------------------------------------------
        self.lbl_image_transfer = self.draw_label("Перенос изображения")
        self.lbl_image_transfer.grid(row=0, column=0, columnspan=4, sticky='wens')

        self.lbl_get_dx = self.draw_label("dx:")
        self.lbl_get_dx.grid(row=1, column=0, sticky='wens')

        self.entry_get_dx = self.draw_entry()
        self.entry_get_dx.grid(row=1, column=1, sticky='wens')

        self.lbl_get_dy = self.draw_label("dy:")
        self.lbl_get_dy.grid(row=1, column=2, sticky='wens')

        self.entry_get_dy = self.draw_entry()
        self.entry_get_dy.grid(row=1, column=3, sticky='wens')

        self.btn_image_transfer = self.draw_button("Переместить изображение")
        # self.btn_add_point.config(command=lambda: self.add_point_to_listpoints())
        self.btn_image_transfer.grid(row=2, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджет масштабирования
        # -----------------------------------------------
        self.lbl_scaling = self.draw_label("Масштабирование")
        self.lbl_scaling.grid(row=3, column=0, columnspan=4, sticky='wens')

        self.lbl_get_kx = self.draw_label("kx:")
        self.lbl_get_kx.grid(row=4, column=0, sticky='wens')

        self.entry_get_kx = self.draw_entry()
        self.entry_get_kx.grid(row=4, column=1, sticky='wens')

        self.lbl_get_ky = self.draw_label("ky:")
        self.lbl_get_ky.grid(row=4, column=2, sticky='wens')

        self.entry_get_ky = self.draw_entry()
        self.entry_get_ky.grid(row=4, column=3, sticky='wens')

        self.lbl_get_scal_xc = self.draw_label("x_c:")
        self.lbl_get_scal_xc.grid(row=5, column=0, sticky='wens')

        self.entry_get_scal_xc = self.draw_entry()
        self.entry_get_scal_xc.grid(row=5, column=1, sticky='wens')

        self.lbl_get_scal_yc = self.draw_label("y_c:")
        self.lbl_get_scal_yc.grid(row=5, column=2, sticky='wens')

        self.entry_get_scal_yc = self.draw_entry()
        self.entry_get_scal_yc.grid(row=5, column=3, sticky='wens')

        self.btn_scaling = self.draw_button("Масштабировать")
        # self.btn_del_point.config(command=lambda: self.del_point_by_number())
        self.btn_scaling.grid(row=6, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты поворота изображения
        # -----------------------------------------------
        self.lbl_image_rotate = self.draw_label("Поворот изображения")
        self.lbl_image_rotate.grid(row=7, column=0, columnspan=4, sticky='wens')

        self.lbl_get_rot_xc = self.draw_label("x_c:")
        self.lbl_get_rot_xc.grid(row=8, column=0, sticky='wens')

        self.entry_get_rot_xc = self.draw_entry()
        self.entry_get_rot_xc.grid(row=8, column=1, sticky='wens')

        self.lbl_get_rot_yc = self.draw_label("y_c:")
        self.lbl_get_rot_yc.grid(row=8, column=2, sticky='wens')

        self.entry_get_rot_yc = self.draw_entry()
        self.entry_get_rot_yc.grid(row=8, column=3, sticky='wens')

        self.lbl_get_angle = self.draw_label(" Angle:")
        self.lbl_get_angle.grid(row=9, column=0, sticky='wens', columnspan=2)

        self.entry_get_angle = self.draw_entry()
        self.entry_get_angle.grid(row=9, column=2, sticky='wens', columnspan=2)

        self.btn_image_rotate = self.draw_button("Повернуть изображение")
        # self.btn_change_point.config(command=lambda: self.change_point_by_number())
        self.btn_image_rotate.grid(row=10, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # работа с plane
        # -----------------------------------------------
        self.plane.draw_axis()

    def create_frame_plane(self) -> tk.Frame:
        """
        Метод создает фрейм для плоскости (plane)
        :return: фрейм для плоскости
        """
        frame_plane_width = self.winfo_screenwidth() - 400
        frame_plane_height = self.winfo_screenheight() - 70

        frame_plane = tk.Frame(
            self,
            width=frame_plane_width,
            height=frame_plane_height
        )

        return frame_plane

    def create_frame_widgets(self) -> tk.Frame:
        """
        Метод создает фрейм для виджетов (plane)
        :return: фрейм для виджетов
        """
        frame_widgets_width = 400

        frame_widgets = tk.Frame(
            self,
            width=frame_widgets_width,
        )

        for i in range(4):
            frame_widgets.columnconfigure(index=i, weight=1, minsize=99)

        frame_widgets.config(bg=LightCyan)

        return frame_widgets

    def draw_plane(self) -> PlaneCanvas:
        """
        Метод размещает холст (canvas) для плоскости (plane) на главном окне
        :return: холст
        """
        plane_width = self.frame_plane.winfo_screenwidth() - 400
        plane_height = self.frame_plane.winfo_screenheight() - 70

        plane = PlaneCanvas(
            y_min=0,
            y_max=10,
            x_min=0,
            master=self.frame_plane,
            width=plane_width,
            height=plane_height,
            bg="#FFFFFF"
        )

        return plane

    def draw_label(self, text: str) -> tk.Label:
        """
        Метод создает виджет текста (label)
        :param text: строка текста
        :return: виджет текста
        """
        label = tk.Label(
            self.frame_widgets,
            text=text,
            font=("Courier New", 14, 'bold'),
        )

        return label

    def draw_entry(self) -> tk.Entry:
        """
        Метод создает виджет однострочного поля ввода (entry)
        :return: виджет однострочного поля ввода
        """
        entry = tk.Entry(
            self.frame_widgets,
            width=15,
            relief=tk.SUNKEN,
            borderwidth=5,
            justify=tk.RIGHT,
            font=("Courier New", 14)
        )

        return entry

    def draw_button(self, text: str) -> tk.Button:
        """
        Метод создает виджет кнопки (button)
        :param text:  текст
        :return: виджет кнопки
        """
        button = tk.Button(
            self.frame_widgets,
            text=text,
            font=("Courier New", 12),
            relief=tk.RAISED
        )

        button.config(bg="#FFFFFF")

        return button

    def draw_radiobutton(self, text: str) -> tk.Radiobutton:
        """
        Метод создает переключатель 2-х множеств треугольника для ввода
        :param text: значение переключателя
        :return: переключатель 2-х множеств треугольника для ввода
        """
        rbt = tk.Radiobutton(
            self.frame_widgets,
            text=text,
            value=text,
            variable=self.rbt_var,
            font=("Courier New", 12, 'bold')
        )

        return rbt

    def draw_listpoints(self, frame: tk.Frame) -> ListPoints:
        """
        Метод создает таблицу для отображения точек
        :param frame: окно
        :return: фрейм
        """
        listpoints = ListPoints(
            frame,
            columns=self.columns,
            show="headings",
            height=14
        )

        return listpoints

    def draw_set_scrollbars(self) -> (ttk.Scrollbar, ttk.Scrollbar):
        """
        Метод создает полосу прокрутки для отображенных точек
        :return: полосу прокрутки
        """
        set1_scrollbar = ttk.Scrollbar(self.frame_set1, command=self.listpoints_set1.yview)
        self.listpoints_set1.config(yscrollcommand=set1_scrollbar.set)

        set2_scrollbar = ttk.Scrollbar(self.frame_set2, command=self.listpoints_set2.yview)
        self.listpoints_set2.config(yscrollcommand=set2_scrollbar.set)

        return set1_scrollbar, set2_scrollbar

    @staticmethod
    def get_point(entry_x: tk.Entry, entry_y: tk.Entry) -> (str, str):
        """
        Метод получает точку с однострочных полей ввода координат
        :param entry_x: поле ввода абсциссы
        :param entry_y: поле вода ординаты
        :return:
        """
        x = entry_x.get()
        y = entry_y.get()

        return x, y

    @staticmethod
    def is_int(x: str) -> bool:
        """
        Метод проверяет, является ли строка целым числом
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

    @staticmethod
    def is_float(x: str) -> bool:
        """
        Метод проверяет, число ли переданный параметр.
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

    def check_input_point(self, x: str, y: str) -> bool:
        """
        Метод проверяет введенную точку на корректность
        :param x: абсцисса точки
        :param y: ордината точки
        :return: True, если точка валидная, False иначе
        """
        if not self.is_float(x) or not self.is_float(y):
            return False

        return True

    def add_point_to_listpoints(self) -> None:
        """
        Метод вставляет в поле в зависимости от выбора множества
        :return: None
        """
        x, y = self.get_point(self.entry_add_x, self.entry_add_y)

        if self.check_input_point(x, y):
            x, y = float(x), float(y)
            if self.rbt_var.get() == "Первое множество":
                self.listpoints_set1.add_point((x, y))
                self.plane.draw_point(x, y, color=BLUE)
            else:
                self.listpoints_set2.add_point((x, y))
                self.plane.draw_point(x, y, color=RED)

    def del_if_valid_num(self, table: ListPoints, n: int, color: str) -> None:
        """
        Метод удаляет точку по валидному номеру
        :param table: таблица точек
        :param n: номер точки
        :param color: цвет точки
        :return: None
        """
        if table.is_valid_number(n):
            table.del_point(n)
            self.plane.del_point(n, color=color)
            return

        messagebox.showwarning("Неверный номер точки!",
                               "Точки с введенным номером не существует!")

    def del_point_by_number(self) -> None:
        """
        Метод удаляет из поля точку в зависимости от выбора множества
        :return: None
        """
        n = self.entry_n_del.get()

        if self.is_int(n):
            n = int(n)
            if self.rbt_var.get() == "Первое множество":
                self.del_if_valid_num(self.listpoints_set1, n, color=BLUE)
            else:
                self.del_if_valid_num(self.listpoints_set2, n, color=RED)

    def change_if_valid_num(self, table: ListPoints,
                            num: int,
                            new_x: float,
                            new_y: float,
                            color: str) -> None:
        """
        Метод изменяет точку по валидному номеру
        :param table: окно
        :param num: номер точки
        :param new_x: новая абсцисса точки
        :param new_y: новая ордината точки
        :param color: цвет точки
        :return: None
        """
        if table.is_valid_number(num):
            table.change_point(num, new_x, new_y)
            self.plane.change_point(num, new_x, new_y, color=color)
            return

        messagebox.showwarning("Неверный номер точки!",
                               "Точки с введенным номером не существует!")

    def change_point_by_number(self) -> None:
        """
        Метод изменяет точку в одном из множеств
        :return: None
        """
        n = self.entry_n_change.get()
        x, y = self.get_point(self.entry_new_x, self.entry_new_y)

        if self.is_int(n) and self.check_input_point(x, y):
            n, x, y = int(n), float(x), float(y)
            if self.rbt_var.get() == "Первое множество":
                self.change_if_valid_num(self.listpoints_set1, n, x, y, color=BLUE)
            else:
                self.change_if_valid_num(self.listpoints_set2, n, x, y, color=RED)
