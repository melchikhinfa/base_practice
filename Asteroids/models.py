from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sprite, update_position

UP = Vector2(0, -1) # вектор "вперед/вверх" - стартовый вектор для корабля

class GameObject:
    """"Родительский класс объектов игрового поля,
        описывает поведение объектов на игровом поле."""
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position) # координаты положения на поле
        self.sprite = sprite # bullet/space/spaceship/asteroid
        self.radius = sprite.get_width() / 2 # радиус объекта
        self.velocity = Vector2(velocity) # вектор скорости (т.е. изменение координат)

    def draw(self, surface):
        """"Отрисовка объектов со смещением"""
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        """Обновляем позиции согласно приращению координат"""
        self.position = update_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        """Проверяет столкновение одного объекта спрайта с другим,
        возвращает булево значение (True = столкновение)"""
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    """"Класс корабль. Используется для генерации объекта корабля (игрока) с заданными параметрами.
    Определяет вращение вокруг оси, ускорение, """
    rotation_speed = 5 # скорость изменения угла поворота
    acceleration_koef = 0.05 # ускорение корабля
    bullet_speed = 10 # скорость пули

    def __init__(self, position, create_bullets):
        self.direction = Vector2(UP)
        self.create_bullets = create_bullets
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, rotation_dir=True):
        """"Вращение корабля вокргу своей оси"""
        sign = 1 if rotation_dir else -1 # вращение по часовой стрелке или против
        angle = self.rotation_speed * sign
        self.direction.rotate_ip(angle) # вращаем полученный вектор в зависимости от угла

    def accelerate(self):
        """"Генерируем вектор ускорения корабля"""
        self.velocity += self.direction * self.acceleration_koef

    def draw(self, surface):
        """Отрисовка вращения корабля"""
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0) # масштабираем пикчу спрайта и вращаем
        rotated_surface_size = Vector2(rotated_surface.get_size()) # получаем корды вращающ. пикчи
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)  # Отрисовывем вращения, согласно новым коорлинатам спрайта

    def shoot(self):
        """Генерирует объект пули и кладет ее в список """
        bullet_velocity = self.direction * self.bullet_speed + self.velocity # вектор ускорения + приращение вектора напр. движ. пули
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullets(bullet) # create_bullets == self.bullets.append добавляем спрайт пульки в список



class Asteroid(GameObject):
    """"Используется для создания объекта 'астероид',
        поведение объекта полностью описывается методами родительского класса."""
    def __init__(self, position, create_asteroids):
        sprite = load_sprite("asteroid")
        super().__init__(position, sprite, get_random_velocity(1, 2))



class Bullet(GameObject):
    """"Используется для создания объекта 'пуля',
        поведение объекта описывается методами родительского класса."""
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        """Позиция корабля для совершения движения"""
        self.position = self.position + self.velocity