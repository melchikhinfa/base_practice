import tkinter as tk
from math import sin, cos, pi
from numpy import sign

width = 600
height = 600
root = tk.Tk()
root.title("Суперэллипс")
c = tk.Canvas(root, width=width, height=height, bg='white')

points_list = []  # список точек для отрисовки


def draw_points(canvas, x, y, a, b): # создает точки и записывает их в список
    # Смещение относительно центра, a и b это коорд. центра канваса
    x = a + x
    y = b + y
    x1, y1 = (x - 1), (y - 1)
    x2, y2 = (x + 1), (y + 1)

    points = canvas.create_oval(x1, y1, x2, y2, fill="red", outline="red")
    points_list.append(points)  # Добавляем точку в список точек


def superellips(canvas, n):
    """Метод отрисовки суперэллипса"""
    a, b = 300, 300  # ширина и высота пополам
    step = 1000  # шаг отрисовки точек-овалов
    delta = (2 * pi) / step  # дробим значения 2*pi
    x_points = []
    y_points = []
    theta = 0  # theta не интерпретировать как угол, это один из параметров в уравнениях ниже

    for i in range(step + 1):
        # Суперэллипс определяется следующими формулами
        x = (abs(cos(theta)) ** (2 / n)) * a * sign(cos(theta))
        y = (abs(sin(theta)) ** (2 / n)) * b * sign(sin(theta))
        x_points.append(x)
        y_points.append(y)
        theta += delta  # при каждой итерации приращиваем значение тетта, для отрисовки кривой Ламе по точкам

    if len(x_points) == len(y_points):
        for i in range(len(x_points)):
            draw_points(canvas, x_points[i], y_points[i], a, b)
    else:
        raise ValueError("Списки координат точек не равны!")


def check_points_list(number):  # проверка, что список точек пуст, перед повторным вычислением координат точек и отрисовкой
    if len(points_list) != 0:
        for point in points_list:
            c.delete(point)
    superellips(c, float(number))


def main():
    c.pack(fill=tk.BOTH, expand=1)  # в середине окна, с растягиванием до краев окна
    scale = tk.Scale(root, from_=0.01, to=3.75, digits=3, resolution=0.01,
                     command=check_points_list, orient=tk.HORIZONTAL)
    scale.pack(side=tk.LEFT, padx=150)
    root.mainloop()


main()
