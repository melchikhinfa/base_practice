import tkinter as tk
import random

width = 800
height = 600
snake_speed = 100
block_size = 20  # размер блока змеи/еды
start_size = 3  # стартовое значение блоков змеи
dir = "Down"  # дефолтное значение направления движения, до получения комманды с клавиатуры


class Snake:
    """Описывает положение и отрисовку блоков змейки"""

    def __init__(self):
        self.snake_size = start_size
        self.coordinates = []
        self.sn_blocks = []  # тут будем хранить отрисовки блоков змеи
        for i in range(0, self.snake_size):
            self.coordinates.append([400, 300])  # стартоое положение по центру

        for x, y in self.coordinates:
            sn_block = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill='black',
                                               tag='Snake')  # отрисовываем
            self.sn_blocks.append(sn_block)


class Food:
    """Описывает положение и отрисовку блока еды"""

    def __init__(self):
        x = random.randint(0, width / block_size) * block_size
        y = random.randint(0, height / block_size) * block_size
        self.coordinates = [x, y]
        canvas.create_rectangle(x, y, x + block_size, y + block_size, fill='red', tag='food')


def turn_and_collision(snake, food):
    """Производит перемещение змейки по 4-м направлениям и фиксирует столкновения"""
    x, y = snake.coordinates[0]
    if dir == "Up":
        y -= block_size
    elif dir == "Down":
        y += block_size
    elif dir == "Left":
        x -= block_size
    elif dir == "Right":
        x += block_size

    snake.coordinates.insert(0, (x, y))  # новые координаты головы змеи
    sn_block = canvas.create_rectangle(x, y, x + block_size, y + block_size,
                                       fill='black')  # рисуем голову змеи в новой пизиции
    snake.sn_blocks.insert(0, sn_block)

    # "съедаем" объект food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        score_ind.config(text=f'Счет: {score}')
        canvas.delete('food')  # удаляем прежний объект еды
        food = Food()  # создаем новый
    else:
        del snake.coordinates[-1]  # удаляем последний набор координат в списке
        canvas.delete(snake.sn_blocks[-1])  # удаляем блоки с канваса
        del snake.sn_blocks[-1]  # удаляем блоки из списка блоков тела змеи

    # "съедаем" края окна
    if x <= 0 or x >= width:
        end_game()
    elif y <= 0 or y >= height:
        end_game()

    # Каннибализм
    for sn_block_coord in snake.coordinates[1:]:
        if x == sn_block_coord[0] and y == sn_block_coord[1]:
            end_game()

    root.after(snake_speed, turn_and_collision, snake, food)
    canvas.update()


def ch_dir(new_dir):
    """Меняет направление движения и не дает змейке сделать разворот на 180"""
    global dir

    match new_dir:
        case "Up" if dir != "Down":
            dir = new_dir
        case "Down" if dir != "Up":
            dir = new_dir
        case "Left" if dir != "Right":
            dir = new_dir
        case "Right" if dir != "Left":
            dir = new_dir


def end_game():
    """Выполняет очистку канваса и выводит сообщение об окончании игры"""
    canvas.delete('all')
    canvas.create_text(400, 300, font=('arial', 70), text="Вы проиграли!", fill="red", tag="gameover")


root = tk.Tk()
root.title("Змейка")
root.resizable(0, 0)

# Счет
score = 0
score_ind = tk.Label(root, text=f'Счет:{score}', font=('arial', 50))
score_ind.pack()

canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()
root.update()

# биндим кнопки
root.bind('<Left>', lambda turn: ch_dir('Left'))
root.bind('<Right>', lambda turn: ch_dir('Right'))
root.bind('<Up>', lambda turn: ch_dir('Up'))
root.bind('<Down>', lambda turn: ch_dir('Down'))

snake = Snake()
food = Food()
turn_and_collision(snake, food)

root.mainloop()
