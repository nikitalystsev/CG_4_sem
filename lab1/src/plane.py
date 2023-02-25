from task import *
import tkinter as tk
from tkinter import messagebox

CONST_SCALE = 5

ORANGE = "#FFA500"
RED = "#FF0000"
DARKCYAN = "DarkCyan"
GREEN = "#008000"
BLUE = "#0000FF"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"
BLACK = "#000000"
Aquamarine = "#7FFFD4"
LightCyan = "#E0FFFF"


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, y_min, y_max, x_min, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param y_min: желаемая минимальная ордината
        :param y_max: желаемая максимальная ордината
        :param x_min: желаемая минимальная абсцисса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = self.get_x_max()
        self.axis_space = 10
        self.set1 = []
        self.set2 = []
        self.other_points = []
        self.km = self.get_km()
        self.task = Task()

    def get_x_max(self) -> float:
        """
        Метод получает максимальное значение абсциссы
        в зависимости от максимальной ординаты
        (для соблюдения правильного масштаба)
        :return: максимальное значение абсциссы
        """
        axis_coef = self.width / self.height
        x_max = axis_coef * self.y_max

        return x_max

    def get_km(self) -> float:
        """
        Функция вычисляет коэффициент масштабирования
        :return: None
        """
        if self.x_max - self.x_min != 0 and self.y_max - self.y_min != 0:
            kx = (self.width - 0) / (self.x_max - self.x_min)
            ky = (self.height - 0) / (self.y_max - self.y_min)
        else:
            kx = ky = self.km

        return min(kx, ky)

    def scaling(self) -> None:
        """
        Метод масштабирует плоскость
        :return: None
        """
        x_s = [x for x, _ in self.task.set1]
        x_s.extend([x for x, _ in self.task.set2])
        x_s.extend([x for x, _ in self.task.other_points])

        y_s = [y for _, y in self.task.set1]
        y_s.extend([y for _, y in self.task.set2])
        y_s.extend([y for _, y in self.task.other_points])

        if len(x_s) == 0 or len(y_s) == 0:
            self.y_max, self.y_min = 10, 0
            self.x_max, self.x_min = 14.3, 0
        else:
            self.y_max = max(y_s) + CONST_SCALE
            self.y_min = min(y_s) - CONST_SCALE
            self.x_max = max(x_s) + CONST_SCALE
            self.x_min = min(x_s) - CONST_SCALE

        self.km = self.get_km()

    def draw_axis(self) -> None:
        """
        Метод строит координатные оси на плоскости
        :return: None
        """
        for i in range(0, self.height, 50):
            self.create_line(7, self.height - i, 13, self.height - i, width=2)
            if i != 0:
                origin_y = self.to_origin_y(self.height - i + self.axis_space)
                text = str(round(origin_y, 2))
                self.create_text(14, self.height - i, text=text, anchor='w')

        for i in range(0, self.width, 50):
            self.create_line(i, self.height - 7, i, self.height - 13, width=2)
            if i != 0:
                origin_x = self.to_origin_x(i - self.axis_space)
                text = str(round(origin_x, 2))
                self.create_text(i, self.height - 20, text=text)

        # горизонтальная линия - ось абсцисс
        self.create_line(0, self.height - self.axis_space, self.width,
                         self.height - self.axis_space, width=2, arrow=tk.LAST)
        # вертикальная линия - ось ординат
        self.create_line(self.axis_space, self.height,
                         self.axis_space, 0, width=2, arrow=tk.LAST)

    def to_origin_x(self, canvas_x: float) -> float:
        """
        Метод преобразует абсциссу точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_x: абсцисса холста
        :return: оригинальная абсцисса
        """
        origin_x = (canvas_x - 0) / self.km + self.x_min

        return origin_x

    def to_origin_y(self, canvas_y: float) -> float:
        """
        Метод преобразует ординату точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_y:  ордината холста
        :return: оригинальная ордината
        """
        origin_y = self.y_max - (canvas_y - 0) / self.km

        return origin_y

    def to_origin_coords(self, canvas_x: float, canvas_y: float) \
            -> (float, float):
        """
        Метод преобразует координаты точки, ранее преобразованные
        для отображения на холсте, в оригинальные значения
        :param canvas_x: абсцисса холста
        :param canvas_y: ордината холста
        :return: оригинальные координаты
        """

        return self.to_origin_x(canvas_x), self.to_origin_y(canvas_y)

    def to_canvas_x(self, origin_x: float) -> float:
        """
        Метод преобразует полученную с поля ввода абсциссу
        для отображения на холсте
        :param origin_x: оригинальная абсцисса
        :return: абсцисса холста.
        """
        canvas_x = int(0 + (origin_x - self.x_min) * self.km)

        return canvas_x + self.axis_space

    def to_canvas_y(self, origin_y: float) -> float:
        """
        Метод преобразует полученную с поля ввода ординату
        для отображения на холсте
        :param origin_y: оригинальная ордината
        :return: ордината холста
        """
        canvas_y = int(0 + (self.y_max - origin_y) * self.km)

        return canvas_y - self.axis_space

    def to_canvas_coords(self, x: float, y: float) -> (float, float):
        """
        Метод преобразует полученные с поля ввода координаты
        для отображения на холсте
        :param x: оригинальная абсцисса
        :param y: оригинальная ордината
        :return: координаты точки для холста
        """

        return self.to_canvas_x(x), self.to_canvas_y(y)

    def draw_list_points(self, list_coords, list_points, color) -> None:
        """
        Метод отображает список точек на холсте
        :param list_coords: список координат точек
        :param list_points: список точек
        :param color: цвет точек
        :return: None
        """
        for i, point in enumerate(list_coords):
            canvas_x, canvas_y = self.to_canvas_coords(point[0], point[1])
            text = f"{i + 1}.({round(point[0], 2)};{round(point[1], 2)})"
            point = self.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3,
                                     canvas_y + 3, fill=color, outline=color)
            self.create_text(canvas_x + 5, canvas_y - 10, text=text,
                             fill=color, font=("Courier New", 5))
            list_points[i] = point

    def draw_set_points(self) -> None:
        """
        Метод отображает введенные точки на плоскости
        :return: None
        """
        # отображение первого множества точек
        self.draw_list_points(self.task.set1, self.set1, BLUE)
        # отображение второго множества точек
        self.draw_list_points(self.task.set2, self.set2, RED)
        # отображение прочих точек
        self.draw_list_points(self.task.other_points,
                              self.other_points, DARKCYAN)

    def draw_point(self, origin_x: float, origin_y: float, color: str) -> None:
        """
        Метод отображает точку на плоскости
        :param origin_x: оригинальная абсцисса
        :param origin_y: оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        self.delete(tk.ALL)  # очищаю весь холст

        # добавляю точку ко множеству точек (первому или второму)
        if color == BLUE:  # первое множество точек
            self.task.set1.append((origin_x, origin_y))
            self.set1.append(0)
        elif color == RED:  # второе множество точек
            self.task.set2.append((origin_x, origin_y))
            self.set2.append(0)
        else:  # прочие точки
            if len(self.other_points) == 2:
                self.other_points = []
                self.task.other_points = []
            self.task.other_points.append((origin_x, origin_y))
            self.other_points.append(0)

        self.scaling()  # выполняется масштабирование
        # рисуются координатные оси, с промежуточными значениями,
        # соответствующими масштабу
        self.draw_axis()
        self.draw_set_points()  # отображаю имеющиеся точки

    def change_point(self, n: int, new_origin_x: float,
                     new_origin_y: float, color: str) -> None:
        """
        Метод изменяет точку
        :param n: номер точки
        :param new_origin_x: новая оригинальная абсцисса
        :param new_origin_y: новая оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        # удаляю старую точку
        self.del_point(n, color)

        # Изменяю данные точки (первого или второго множества)
        if color == BLUE:
            self.task.set1.insert(n - 1, (new_origin_x, new_origin_y))
            self.set1.insert(n - 1, 0)
        else:
            self.task.set2.insert(n - 1, (new_origin_x, new_origin_y))
            self.set2.insert(n - 1, 0)

        self.other_points = []
        self.task.other_points = []

        self.task.default_task_param()

        self.delete(tk.ALL)  # очищаю холст
        self.scaling()  # выполняется масштабирование
        # рисуются координатные оси, с промежуточными значениями,
        # соответствующими масштабу
        self.draw_axis()
        self.draw_set_points()  # отображаю имеющиеся точки

    def del_point(self, n: int, color: str) -> None:
        """
        Метод удаляет точку
        :param n: номер точки
        :param color: цвет точки
        :return: None
        """
        # удаляю точку с холста
        self.delete(self.set1[n - 1]) if color == BLUE else \
            self.delete(self.set2[n - 1])
        # удаляю точку со списка с координатами
        self.task.set1.pop(n - 1) if color == BLUE else \
            self.task.set2.pop(n - 1)
        # удаляю точку со списка с тегами точек для холста
        self.set1.pop(n - 1) if color == BLUE else self.set2.pop(n - 1)

        self.other_points = []
        self.task.other_points = []

        self.task.default_task_param()

        self.delete(tk.ALL)  # очищаю холст
        self.scaling()  # выполняется масштабирование
        # рисуются координатные оси, с промежуточными значениями,
        # соответствующими масштабу
        self.draw_axis()
        self.draw_set_points()  # отображаем неудаленные точки

    def draw_triangle(self, point1, point2, point3, color: str) -> None:
        """
        Метод строит треугольник по трем точкам
        :param point1: первая точка
        :param point2: вторая точка
        :param point3: третья точка
        :param color: цвет треугольника
        :return: None
        """
        x1, y1 = self.to_canvas_coords(point1[0], point1[1])
        x2, y2 = self.to_canvas_coords(point2[0], point2[1])
        x3, y3 = self.to_canvas_coords(point3[0], point3[1])

        self.create_line(x1, y1, x2, y2, width=2, fill=color, smooth=True)
        self.create_line(x2, y2, x3, y3, width=2, fill=color, smooth=True)
        self.create_line(x3, y3, x1, y1, width=2, fill=color, smooth=True)

    @staticmethod
    def get_nums_vertex(num_vertex: int):
        """
        Метод определит вершины для стороны, к которой будет проведена высота
        :param num_vertex: номер вершины, из которой будет проведена высота
        :return: три номера вершины по порядку
        """
        num_vertex -= 1  # для индексов

        if num_vertex == 0:
            return 0, 1, 2
        if num_vertex == 1:
            return 1, 0, 2
        if num_vertex == 2:
            return 2, 0, 1

    def draw_height(self, triangle, num_vertex, canvas_ph, color) -> None:
        """
        Метод отображает высоту треугольника,
        проведенную из вершины с номером num_vertex
        :param color: цвет высоты
        :param canvas_ph: точка пересечения высот треугольника
        :param triangle: треугольник
        :param num_vertex: номер вершины
        :return: None
        """
        n, m, k = self.get_nums_vertex(num_vertex)
        canvas_x_ph, canvas_y_ph = canvas_ph[0], canvas_ph[1]
        # находим коэф-ты уравнения стороны, к которой проведем высоту
        a_side, b_side, c_side = Task.get_coef_side(triangle[m], triangle[k])
        # находим коэф-ты уравнения высоты по известным коэф-там стороны,
        # и вершины
        a_h, b_h, c_h = Task.get_coef_h((a_side, b_side, c_side), triangle[n])
        # находим точку пересечения стороны и высоты
        x_p, y_p = Task.find_point_intersection(
            (a_side, b_side, c_side), (a_h, b_h, c_h))
        # переводим координаты в координаты холста
        canvas_x_p, canvas_y_p = self.to_canvas_coords(x_p, y_p)
        # строим высоту от точки пересечения высоты со стороной
        # до точки пересечения высот
        self.create_line(canvas_x_p, canvas_y_p, canvas_x_ph, canvas_y_ph,
                         width=2, fill=color)

    def draw_heights(self, triangle, canvas_ph, color) -> None:
        """
        Метод рисует все высоты треугольника
        :param color:
        :param triangle: треугольник
        :param canvas_ph: точка пересечения высот треугольника
        :return: None
        """
        self.draw_height(triangle, 1, canvas_ph, color)
        self.draw_height(triangle, 2, canvas_ph, color)
        self.draw_height(triangle, 3, canvas_ph, color)

    def get_solve(self):
        """
        Метод находит решение задачи
        :return: количество рассмотренных вариантов
        """

        # генерируются всевозможные валидные треугольники
        triangles1 = Task.generate_triangles(self.task.set1)
        triangles2 = Task.generate_triangles(self.task.set2)

        # найдем коэфф-ты для уравнения оси абсцисс (y = 0, A=C=0, By=0 => y=0)
        a_x, b_x, c_x = Task.get_coef_side((0, 0), (1, 0))  # точки оси абсцисс

        for tr1 in triangles1:
            for tr2 in triangles2:
                self.task.count += 1
                # находит точки пересечения высот обоих треугольников
                ph1 = self.task.find_inters_heights(tr1)
                ph2 = self.task.find_inters_heights(tr2)

                # найдем коэффициенты прямой,
                # проходящей через точки пересечения высот двух треугольников
                a, b, c = Task.get_coef_side(ph1, ph2)

                # находим угол между прямыми
                angle = Task.find_angle((a, b, c), (a_x, b_x, c_x))

                # определяем минимальный угол
                if angle < self.task.min_angle:
                    self.task.min_angle = angle
                    self.task.triangle1, self.task.triangle2 = tr1, tr2
                    self.task.ph1, self.task.ph2 = ph1, ph2

        return

    def error_processing(self) -> bool:
        """
        Метод обрабатывает возможные ошибки при получении решения задачи
        :return: True, если ошибок нет, False - иначе
        """

        if len(self.set1) == 0 and len(self.set2) == 0:
            messagebox.showwarning("", "Плоскость пустая!\nДобавьте точек, чтобы получить решение задачи!")
            return False
        elif len(self.set1) == 0:
            messagebox.showwarning("", f"На плоскости отсутствуют точки первого множества!\n"
                                       "Добавьте их, чтобы решить задачу!")
            return False
        elif len(self.set2) == 0:
            messagebox.showwarning("", f"На плоскости отсутствуют точки второго множества!\n"
                                       "Добавьте их, чтобы решить задачу!")
            return False
        elif 0 < len(self.set1) < 3 and 0 < len(self.set2) < 3:
            messagebox.showwarning("", "Точек обеих множеств недостаточно для построения треугольников!\n"
                                       "Для построения треугольника нужно не менее 3-х точек каждого множества!\n"
                                       "Добавьте точек, чтобы получить решение задачи!")
            return False
        elif len(self.set1) < 3:
            messagebox.showwarning("", "Точек первого множества недостаточно для построения треугольника!\n"
                                       "Для построения треугольника нужно не менее 3-х точек!\n"
                                       "Добавьте точек, чтобы получить решение задачи!")
            return False
        elif len(self.set2) < 3:
            messagebox.showwarning("", "Точек второго множества недостаточно для построения треугольника!\n"
                                       "Для построения треугольника нужно не менее 3-х точек!\n"
                                       "Добавьте точек, чтобы получить решение задачи!")
            return False

        triangles1 = Task.generate_triangles(self.task.set1)
        triangles2 = Task.generate_triangles(self.task.set2)

        if len(triangles1) == 0 and len(triangles2) == 0:
            messagebox.showwarning("", "Точки каждого множества лежат на одной прямой!\n"
                                       "Добавьте других точек, чтобы получить решение задачи!")
            return False
        elif len(triangles1) == 0:
            messagebox.showwarning("", "Точки первого множества лежат на одной прямой!\n"
                                       "Добавьте других точек, чтобы получить решение задачи!")
            return False
        elif len(triangles2) == 0:
            messagebox.showwarning("", "Точки второго множества лежат на одной прямой!\n"
                                       "Добавьте других точек, чтобы получить решение задачи!")
            return False

        return True

    def draw_solve(self):
        """
        Функция отображает найденное перебором решение
        :return:
        """

        if not self.error_processing():
            return

        self.get_solve()

        # # отображаю точки пересечения высот
        self.draw_point(self.task.ph1[0], self.task.ph1[1], DARKCYAN)
        self.draw_point(self.task.ph2[0], self.task.ph2[1], DARKCYAN)

        # получаю координаты холста
        # для точек пересечения высот найденных треугольников
        canvas_x_ph1, canvas_y_ph1 = self.to_canvas_coords(self.task.ph1[0], self.task.ph1[1])
        canvas_x_ph2, canvas_y_ph2 = self.to_canvas_coords(self.task.ph2[0], self.task.ph2[1])

        # отображаю найденные треугольники
        self.draw_triangle(self.task.triangle1[0],
                           self.task.triangle1[1], self.task.triangle1[2], BLUE)
        self.draw_triangle(self.task.triangle2[0], self.task.triangle2[1], self.task.triangle2[2], RED)

        # отображаю прямую,
        # соединяющую точку пересечения высот 2-х треугольников
        self.create_line(canvas_x_ph1, canvas_y_ph1,
                         canvas_x_ph2, canvas_y_ph2, width=2, fill=DARKCYAN)

        # первый треугольник
        # ---------------------------------------------------------------------
        self.draw_heights(self.task.triangle1, (canvas_x_ph1, canvas_y_ph1), GREEN)

        # второй треугольник
        # ---------------------------------------------------------------------
        self.draw_heights(self.task.triangle2, (canvas_x_ph2, canvas_y_ph2), GREEN)

        self.text_solve()

    def text_solve(self) -> None:
        """
        Метод отображает результаты в текстовом формате
        :return: None
        """

        win = tk.Toplevel()
        win.grab_set()
        textbox = tk.Text(win, width=60, height=10, state=tk.DISABLED, borderwidth=5,
                          wrap="word", font=("Courier New", 14), fg=BLACK, bg=LightCyan)
        textbox.pack()

        text = f"Всего было рассмотрено {self.task.count} вариантов\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("1.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Треугольник первого множества был построен на след. точках:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("2.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"1.({round(self.task.triangle1[0][0], 2)};{round(self.task.triangle1[0][1], 2)}), " \
               f"2.({round(self.task.triangle1[1][0], 2)};{round(self.task.triangle1[1][1], 2)})," \
               f"3.({round(self.task.triangle1[2][0], 2)};{round(self.task.triangle1[2][1], 2)})\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("3.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Треугольник второго множества был построен на след. точках:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("4.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"1.({round(self.task.triangle2[0][0], 2)};{round(self.task.triangle2[0][1], 2)}), " \
               f"2.({round(self.task.triangle2[1][0], 2)};{round(self.task.triangle2[1][1], 2)})," \
               f"3.({round(self.task.triangle2[2][0], 2)};{round(self.task.triangle2[2][1], 2)})\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("5.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Точки пересечения высот имеют след. координаты:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("6.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"1.({round(self.task.ph1[0], 2)};{round(self.task.ph1[1], 2)}), " \
               f"2.({round(self.task.ph2[0], 2)};{round(self.task.ph2[1], 2)})\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("7.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Искомое минимальное значение угла между прямой,\n" \
               "соединяющей точки пересечения высот 2-х треугольников:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("8.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"angle = {round(self.task.min_angle, 3)} градуса"
        textbox.config(state=tk.NORMAL)
        textbox.insert("10.0", text)
        textbox.config(state=tk.DISABLED)
