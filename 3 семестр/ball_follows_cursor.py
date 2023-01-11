from tkinter import *
import time, random, math


class BallAttraction:
    def __init__(self, canvas):
        self.canvas = canvas
        self.stop = False
        self.object_id = self.canvas.create_oval(350, 350, 400, 400, tag='Ball', fill=random.choice(colors))

    def coords(self):
        print(self.canvas.coords('Ball'))
        return self.canvas.coords('Ball')

    def mouse_coords(self):
        mouse_x, mouse_y = tk.winfo_pointerx(), tk.winfo_pointery()
        self.mousecoords = mouse_x - tk.winfo_rootx(), mouse_y - tk.winfo_rooty()
        return self.mousecoords

    def move_toward_mouse(self):
        center_x, center_y = (self.coords()[0] + self.coords()[2]) / 2, (self.coords()[1] + self.coords()[3]) / 2
        mouse_x, mouse_y = self.mousecoords
        move_x = (mouse_x - center_x)
        move_y = (mouse_y - center_y)

        speed = 2
        theta = math.atan2(move_y, move_x)  ## угол между точкой и позицией мыши, относительно x

        x = speed * math.cos(theta)
        y = speed * math.sin(theta)

        self.canvas.move('Ball', x, y)



tk = Tk()
tk.title("А-ля Agar.io")
canvas = Canvas(tk, width=750, height=750)
colors = ['red', 'blue', 'green', 'yellow']

canvas.pack()

agar = BallAttraction(canvas)
agar.mouse_coords()

while agar.stop == False:
    try:
        agar.move_toward_mouse()
        agar.mouse_coords()
        tk.update_idletasks()
        tk.update()
        time.sleep(.005)
    except:  # KeyboardInterrupt:
        print('CRL-C recieved, quitting')
        tk.quit()
        break
