from tkinter import *


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
        self.points = []

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
        for i in range(0, self.height, 50):
            self.create_line(7, self.height - i, 13, self.height - i, width=2)
            if i != 0:
                origin_y = self.to_origin_y(self.height - i + 10)
                text = str(round(origin_y, 2))
                self.create_text(14, self.height - i, text=text, anchor='w')

        for i in range(0, self.width, 50):
            self.create_line(i, self.height - 7, i, self.height - 13, width=2)
            if i != 0:
                origin_x = self.to_origin_x(i - 10)
                text = str(round(origin_x, 2))
                self.create_text(i, self.height - 20, text=text)

        self.create_line(0, self.height - 10, self.width, self.height - 10, width=2, arrow=LAST)
        self.create_line(10, self.height, 10, 0, width=2, arrow=LAST)

    def to_origin_x(self, canvas_x: float) -> float:
        """
        Метод преобразует абсциссу точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_x: абсцисса холста
        :return: оригинальная абсцисса
        """
        return canvas_x * (self.x_max - self.x_min) / self.width + self.x_min

    def to_origin_y(self, canvas_y: float) -> float:
        """
        Метод преобразует ординату точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_y:  ордината холста
        :return: оригинальная ордината
        """
        return -(canvas_y * (self.y_max - self.y_min) / self.height - self.y_max)

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
        canvas_x = (origin_x - self.x_min) / (self.x_max - self.x_min) * self.width
        return canvas_x + self.axis_space

    def to_canvas_y(self, origin_y: float) -> float:
        """
        Метод преобразует полученную с поля ввода ординату
        для отображения на холсте
        :param origin_y: оригинальная ордината
        :return: ордината холста
        """
        canvas_y = (self.y_max - origin_y) / (self.y_max - self.y_min) * self.height
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

    def draw_point(self, origin_x: float, origin_y: float, color='red') -> None:
        """
        Метод отображает точку на плоскости
        :param origin_x: оригинальная абсцисса
        :param origin_y: оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        canvas_x, canvas_y = self.to_canvas_coords(origin_x, origin_y)
        point = self.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill=color, outline=color)
        self.points.append(point)

    def change_point(self, n: int, new_origin_x: float, new_origin_y: float, color='red') -> None:
        """
        Метод изменяет точку
        :param n: номер точки
        :param new_origin_x: новая оригинальная абсцисса
        :param new_origin_y: новая оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        new_canvas_x, new_canvas_y = self.to_canvas_coords(new_origin_x, new_origin_y)
        self.coords(self.points[n - 1], new_canvas_x - 3, new_canvas_y - 3, new_canvas_x + 3, new_canvas_y + 3)
        point = self.create_oval(new_canvas_x - 3, new_canvas_y - 3, new_canvas_x + 3, new_canvas_y + 3, fill=color,
                                 outline=color)
        self.points[n - 1] = point

    def del_point(self, n: int) -> None:
        """
        Метод удаляет точку
        :param n: номер точки
        :return: None
        """
        self.delete(self.points[n - 1])
        self.points.pop(n - 1)

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