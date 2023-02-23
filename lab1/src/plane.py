from tkinter import *
from tkinter import messagebox


class PlaneCanvas(Canvas):
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
        self.km = self.get_km()

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
        x_s = [x for _, x, _ in self.set1]
        x_s.extend([x for _, x, _ in self.set2])

        y_s = [y for _, _, y in self.set1]
        y_s.extend([y for _, _, y in self.set2])

        self.y_max, self.y_min = max(y_s), min(y_s)
        self.x_max, self.x_min = max(x_s), min(x_s)

        self.km = self.get_km()

    def get_x_max(self) -> float:
        """
        Метод получает максимальное значение абсциссы в зависимости от максимальной ординаты
        (для соблюдения правильного масштаба)
        :return: максимальное значение абсциссы
        """
        axis_coef = self.width / self.height
        x_max = axis_coef * self.y_max

        return x_max

    def draw_axis(self) -> None:
        """
        Метод строит координатные оси на плоскости
        :return: None
        """
        self.create_line(0, self.axis_space, self.width, self.axis_space, fill="#ADFF2F")
        self.create_line(self.width - self.axis_space, 0, self.width - self.axis_space, self.height, fill="#ADFF2F")

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
        self.create_line(0, self.height - self.axis_space, self.width, self.height - self.axis_space, width=2,
                         arrow=LAST)
        # вертикальная линия - ось ординат
        self.create_line(self.axis_space, self.height, self.axis_space, 0, width=2, arrow=LAST)

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

    def to_origin_coords(self, canvas_x: float, canvas_y: float) -> (float, float):
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

    def draw_set_points(self) -> None:
        """
        Метод отображает введенные точки на плоскости
        :return: None
        """
        oval_size = 3
        for i in range(len(self.set1)):
            canvas_x, canvas_y = self.to_canvas_coords(self.set1[i][1], self.set1[i][2])
            point = self.create_oval(canvas_x - oval_size, canvas_y - oval_size, canvas_x + oval_size,
                                     canvas_y + oval_size, fill="#006400")
            self.set1[i] = point, self.set1[i][1], self.set1[i][2]

        for i in range(len(self.set2)):
            canvas_x, canvas_y = self.to_canvas_coords(self.set2[i][1], self.set2[i][2])
            point = self.create_oval(canvas_x - oval_size, canvas_y - oval_size, canvas_x + oval_size,
                                     canvas_y + oval_size, fill="#8B0000")
            self.set2[i] = point, self.set2[i][1], self.set2[i][2]

    def draw_point(self, origin_x: float, origin_y: float, color='red') -> None:
        """
        Метод отображает точку на плоскости
        :param origin_x: оригинальная абсцисса
        :param origin_y: оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        self.delete(ALL)  # очищаю весь холст
        # добавляю точку ко множеству точек (первому или второму)
        self.set1.append((0, origin_x, origin_y)) if color == "#006400" else self.set2.append((0, origin_x, origin_y))
        # self.scaling()  # выполняется масштабирование
        self.draw_axis()  # рисуются координатные оси, с промежуточными значениями, соответствующими масштабу

        self.draw_set_points()

        # messagebox.showinfo("", f"self.find_all() = {self.find_all()}")

    def change_point(self, n: int, new_origin_x: float, new_origin_y: float, color: str) -> None:
        """
        Метод изменяет точку
        :param n: номер точки
        :param new_origin_x: новая оригинальная абсцисса
        :param new_origin_y: новая оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        self.delete(ALL)
        # удаляю старую точку
        self.del_point(n, color)
        # Изменяю данные точки
        if color == "#006400":
            self.set1.insert(n - 1, (0, new_origin_x, new_origin_y))
        else:
            self.set2.insert(n - 1, (0, new_origin_x, new_origin_y))

        # self.scaling()  # выполняется масштабирование
        self.draw_axis()  # рисуются координатные оси, с промежуточными значениями, соответствующими масштабу

        self.draw_set_points()

    def del_point(self, n: int, color: str) -> None:
        """
        Метод удаляет точку
        :param n: номер точки
        :param color: цвет точки
        :return: None
        """
        self.delete(self.set1[n - 1][0]) if color == "#006400" else self.delete(self.set2[n - 1][0])
        self.set1.pop(n - 1) if color == "#006400" else self.set2.pop(n - 1)

# def change_point(self, new_x, new_y):
# def draw_line(self, x1, y1, x2, y2, color='black', width=1):
#     # Рисуем линию, соединяющую заданные точки
#     canvas_x1, canvas_y1 = self.to_canvas_coords(x1, y1)
#     canvas_x2, canvas_y2 = self.to_canvas_coords(x2, y2)
#     self.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=color, width=width)
#
# def draw_polygon(self, points, color='black', outline='', width=1):
#     # Рисуем многоугольник, заданный списком точек
#     canvas_points = []
#     for x, y in points:
#         canvas_x, canvas_y = self.to_canvas_coords(x, y)
#         canvas_points.append(canvas_x)
#         canvas_points.append(canvas_y)
#     self.create_polygon(canvas_points, fill=color, outline=outline, width=width)
