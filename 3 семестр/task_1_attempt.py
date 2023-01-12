import math
import tkinter as tk

CIRCULAR_PATH_INCR = 10

sin = lambda angle: math.sin(math.radians(angle))
cos = lambda angle: math.cos(math.radians(angle))
radius = 200


def coordinates(x_coord, y_coord, radius):
    return (x_coord + radius * cos(0), y_coord + radius * sin(270),
            x_coord + radius * cos(180), y_coord + radius * sin(90))


def circular_path(x, y, radius, dt):  # генератор координат
    angle = 0
    ang = angle % 360
    while True:
        yield x + radius*cos(ang), y + radius*sin(ang)  # приращение координат на каждой итерации
        ang = (ang+dt) % 360  # увеличиваем угол на dt и дробим на сектора

def update_position(canvas, id, obj_data, path_iter):
    obj_data[0], obj_data[1] = next(path_iter) # генерируем новую позицию
    x0, y0, x1, y1 = canvas.coords(id)  # получаем координаты точки
    oldx, oldy = (x0+x1) // 2, (y0+y1) // 2  # координаты центра
    dx, dy = obj_data[0] - oldx, obj_data[1] - oldy  # шаг прироста по координатам
    canvas.move(id, dx, dy)  # на этот прирост и передвигаем объект
    canvas.after(100, update_position, canvas, id, obj_data, path_iter) # повторяем

root = tk.Tk()
root.title('Круговое движение')

canvas = tk.Canvas(root, bg='black', height=500, width=500)
canvas.pack()

oval_data = [250, 250, 200]
dot_data = [350, 250, 10]
x_o, y_o, o_radius = oval_data
x_d, y_d, d_radius = dot_data
main_oval = canvas.create_oval(coordinates(x_o, y_o, o_radius), fill='yellow', width=0)
dot_oval = canvas.create_oval(coordinates(x_d, y_d, d_radius), fill='blue', width=0)


path_iter = circular_path(x_o, y_o, radius, CIRCULAR_PATH_INCR)
next(path_iter)

root.after(100, update_position, canvas, dot_oval, dot_data , path_iter)
root.mainloop()