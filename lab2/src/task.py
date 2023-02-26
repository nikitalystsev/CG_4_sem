from itertools import combinations
import math

EPS = 1e-9


class Task:
    """
    Параметры задачи
    """

    def __init__(self):
        self.set1 = []
        self.set2 = []
        self.other_points = []
        self.triangle1 = []
        self.triangle2 = []
        self.min_angle = float("inf")
        self.ph1 = None
        self.ph2 = None
        self.count = 0

    def default_task_param(self) -> None:
        """
        Метод приводит значения параметров задачи к начальным
        :return: None
        """
        self.triangle1 = []
        self.triangle2 = []
        self.min_angle = float("inf")
        self.ph1 = None
        self.ph2 = None
        self.count = 0

    @staticmethod
    def generate_triangles(points):
        triangles = []
        for triplet in combinations(points, 3):
            x1, y1 = triplet[0]
            x2, y2 = triplet[1]
            x3, y3 = triplet[2]
            # если точки не лежат на одной прямой (соотношение 3)
            if (x2 - x1) * (y3 - y1) != (x3 - x1) * (y2 - y1):
                triangles.append(triplet)
        return triangles

    # уравнение прямой, проходящей через 2 точки (соотношение 7):
    # A*X+B*Y+C=0, где A=Y1-Y2, B=X2-X1, C=(X1-X2)*Y1+(Y2-Y1)*X1

    # Уравнение прямой, перпендикулярной рассматриваемому отрезку и проходящей
    # через точку (Xc,Yc), имеет вид -B*X+A*Y+D=0,
    # где D=B*Xc-A*Yc (соотношение 8)

    # система уравнений для нахождения точки пересечения 2-х прямых:
    # A1*X+B1*Y+C1=0 - уравнение первой прямой
    # A2*X+B2*Y+C2=0 - уравнение второй прямой
    # A1,A2,B1,B2,C1,C2 - известные коэффициенты
    # уравнений соответствующих прямых

    # Пусть заданы две прямые общими уравнениями:
    # A1*X+B1*Y+C1=0 - уравнение первой прямой
    # A2*X+B2*Y+C2=0 - уравнение второй прямой
    # Угол между прямыми определяется след. образом:
    # tg(w)=(A1*B2-A2*B1)/(A1*A2+B1*B2)

    @staticmethod
    def get_coef_side(point1, point2) -> (float, float, float):
        """
        Метод позволяет определить коэффициенты стороны треугольника,
        к которой перпендикулярна высота используя соотношение 7
        :param point1: первая точка
        :param point2: вторая точка
        :return: Коэффициенты
        """
        x1, y1 = point1[0], point1[1]
        x2, y2 = point2[0], point2[1]

        a = y1 - y2
        b = x2 - x1
        c = (x1 - x2) * y1 + (y2 - y1) * x1

        return a, b, c

    @staticmethod
    def get_coef_h(coef_side_triangle, point) -> (float, float, float):
        """
        Метод позволяет определить коэффициенты уравнения высоты по известным
        коэффициентам уравнения стороны треугольника и известным координатам
        вершины треугольника используя соотношение 8
        :param coef_side_triangle: коэф-ты ур-я стороны треугольника
        :param point: вершина треугольника
        :return: коэффициенты
        """
        a_side, b_side, c_side = coef_side_triangle[0], \
            coef_side_triangle[1], coef_side_triangle[2]
        x_c, y_c = point[0], point[1]

        b = -b_side
        a = a_side
        d = b_side * x_c - a_side * y_c

        return b, a, d

    @staticmethod
    def find_point_intersection(line1, line2) -> (float, float):
        """
        Метод находит точку пересечения 2-х прямых
        :param line1: коэф-ты первой прямой
        :param line2: коэф-ты второй прямой
        :return: точка пересечения
        """
        a1, b1, c1 = line1[0], line1[1], line1[2]
        a2, b2, c2 = line2[0], line2[1], line2[2]

        x_p = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)
        y_p = (c1 * a2 - c2 * a1) / (a1 * b2 - a2 * b1)

        return x_p, y_p

    @staticmethod
    def find_inters_heights(triangle):
        """
        Метод обрабатывает треугольник
        :param triangle: треугольник
        :return:
        """
        # находим коэф-ты уравнения стороны, к которой проведем высоту
        a_side1, b_side1, c_side1 = Task.get_coef_side(
            triangle[0], triangle[1])
        # находим коэф-ты уравнения высоты по известным коэф-там стороны,
        # и вершины
        a_h1, b_h1, c_h1 = Task.get_coef_h(
            (a_side1, b_side1, c_side1), triangle[2])

        a_side2, b_side2, c_side2 = Task.get_coef_side(
            triangle[1], triangle[2])
        a_h2, b_h2, c_h2 = Task.get_coef_h(
            (a_side2, b_side2, c_side2), triangle[0])

        # находим точку пересечения высот треугольника
        x_ph, y_ph = Task.find_point_intersection(
            (a_h1, b_h1, c_h1), (a_h2, b_h2, c_h2))

        return x_ph, y_ph

    @staticmethod
    def find_angle(line1, line2):
        """
        Метод находит угол между двумя прямыми
        :param line1: первая прямая
        :param line2: вторая прямая
        :return: угол в градусах
        """
        a1, b1, c1 = line1[0], line1[1], line1[2]
        a2, b2, c2 = line2[0], line2[1], line2[2]

        if abs(a1 * a2 - b1 * b2) < EPS:
            return 90

        tg_w = (a1 * b2 - a2 * b1) / (a1 * a2 - b1 * b2)

        angle = math.atan(tg_w)
        angle_degrees = math.degrees(angle)

        if angle_degrees < 0:
            angle_degrees += 180
        elif abs(angle_degrees) < EPS:
            angle_degrees = 0

        return angle_degrees
