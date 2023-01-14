import random
from pygame import Color
from pygame.image import load
from pygame.math import Vector2


def load_sprite(name, with_alpha=True):
    """Загрузка иконок объектов и их адаптация/конвертирование"""
    path2file = f"models/{name}.png"
    loaded_sprite = load(path2file)

    if with_alpha:
        return loaded_sprite.convert_alpha() # Создает новую копию поверхности с нужным форматом пикселей
    else:
        return loaded_sprite.convert()

def update_position(position, surface):
    """"Возвращает координаты объекта для метода move класса GameObject,
        используется для отрисовки прохождения через границы поля"""
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    """Получает рандомные координаты на поле, в зависимости от ширины и высоты"""
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    """Получает рандомный вектор направления ускорения, с разными показателями скорости
        т.е. позволяет объектам двигаться в рандомных направлениях с разной скоростью."""
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, color=Color("red")):
    """Отрисовка текста поверх основного слоя по центру"""
    text_surface = font.render(text, False, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)