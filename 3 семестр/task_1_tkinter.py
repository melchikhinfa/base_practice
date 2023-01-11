import tkinter as tk
import math
from math import pi

width = 600
height = 600
bg_colour = 'white'
center_x = width // 2
center_y = height // 2

oval_radius = 200  # радиус желтого овала
point_radius = 10  # радиус овала-точки
dist2point = oval_radius  # расстояние до овала-точки
angle = 0  # угол
angle_speed = -0.5  # угловая скорость, она же управляет направлением движения


def point_coords(figure_data):  # вычисляем координаты точки
    center_x, center_y, radius, distance, angle, angle_speed = figure_data
    # Вычисление новой позиции объекта
    x = center_x - distance * math.sin(math.radians(angle))
    y = center_y - distance * math.cos(math.radians(angle))
    # Вычисление координат
    x1 = x - radius
    y1 = y - radius
    x2 = x + radius
    y2 = y + radius
    return x1, y1, x2, y2


def point_move(object, figure_data):
    x1, y1, x2, y2 = point_coords(figure_data)  # вычисляем координаты точки
    c.coords(object, x1, y1, x2, y2)  # изменяем координаты


def point_animation():
    point_data[4] += point_data[5]  # angle += angle_speed - приращение значения на каждой итерации
    point_move(point, point_data)
    root.after(1, point_animation)  # анимация в 1мс


root = tk.Tk()
c = tk.Canvas(root, width=width, height=height, bg=bg_colour)
c.pack()

oval_coords = [100, 100, 500, 500]  # координаты считаем как center_x - radius = x1 (center_x + radius = x2)
x1, y1, x2, y2 = oval_coords
oval = c.create_oval(x1, y1, x2, y2, fill="yellow")

point_data = [center_x, center_y, point_radius, dist2point, angle, angle_speed]  # данные точки
x1, y1, x2, y2 = point_coords(point_data)
point = c.create_oval(x1, y1, x2, y2, fill="red")

point_animation()
root.mainloop()
