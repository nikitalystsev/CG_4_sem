from tkinter import *


class PlaneCanvas(Canvas):
    def __init__(self, y_min, y_max, x_min, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = self.get_x_max()

    def get_x_max(self):
        axis_coef = self.width / self.height
        x_max = axis_coef * self.y_max
        return x_max

    def draw_axis(self):
        for i in range(0, self.height, 50):
            self.create_line(7, self.height - i, 13, self.height - i, width=2)
            if i != 0:
                origin_y = self.to_origin_y(self.height - i)
                text = str(round(origin_y, 2))
                self.create_text(14, self.height - i, text=text, anchor='w')

        for i in range(0, self.width, 50):
            self.create_line(i, self.height - 7, i, self.height - 13, width=2)
            if i != 0:
                origin_x = self.to_origin_x(i)
                text = str(round(origin_x, 2))
                self.create_text(i, self.height - 20, text=text)

        self.create_line(0, self.height - 10, self.width, self.height - 10, width=2, arrow=LAST)
        self.create_line(10, self.height, 10, 0, width=2, arrow=LAST)

    def to_origin_x(self, x):
        """
        Функция преобразует абсциссу точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        """
        return x * (self.x_max - self.x_min) / self.width + self.x_min

    def to_origin_y(self, y):
        """
        Функция преобразует ординату точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        """
        return -(y * (self.y_max - self.y_min) / self.height - self.y_max)

    def to_origin_coords(self, x, y):
        return self.to_origin_x(x), self.to_origin_y(y)

    def to_canvas_x(self, x):
        """
        Функция преобразует полученную с поля ввода абсциссу
        для отображения на холсте
        """
        return (x - self.x_min) / (self.x_max - self.x_min) * self.width

    def to_canvas_y(self, y):
        """
        Функция преобразует полученную с поля ввода ординату
        для отображения на холсте
        """
        return (self.y_max - y) / (self.y_max - self.y_min) * self.height

    def to_canvas_coords(self, x, y):
        return self.to_canvas_x(x), self.to_canvas_y(y)

    def draw_point(self, x, y, color='black'):
        canvas_x, canvas_y = self.to_canvas_coords(x, y)
        self.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill=color, outline=color)

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
