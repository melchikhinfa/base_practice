import pygame
from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text

score = 0


class Asteroids:
    """Основной класс игры"""
    dist_to_asteroid = 200 # дистанция до астероида, нужна при генерации случайных объектов астероидов
    # ниже в цикле объяснил подробно

    def __init__(self):
        self.pygame_initialize()
        self.window = pygame.display.set_mode((800, 600)) # создание игрового поля
        self.background = load_sprite("space", False) # загрузка фона
        self.clock = pygame.time.Clock() # для частоты отрисовки (ограничение фпс)
        self.font = pygame.font.Font(None, 64) # обработка шрифта
        self.message = ""   # константа для вывода текста (можно заменить на isinstance в коде, при вызове отрисовки текста)
        self.asteroids = [] # объекты астероидов
        self.bullets = []   # объекты пуль
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        # спавним астероиды на расстоянии от игрока,
        # дабы не получить случайный эндгейм при запуске или во время игры
        for i in range(6):
            while True:
                position = get_random_position(self.window)
                if (
                        position.distance_to(self.spaceship.position)
                        > self.dist_to_asteroid
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        """Основной цикл в котором выполняются все методы"""
        while True:
            self.input_handler()
            self.main_logic()
            self.draw_objects()

    def pygame_initialize(self):
        """Инициализируем pygame и устанавливаем тайтл"""
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def input_handler(self):
        """Хэндлер комманд с клавиатуры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit() # если закрыли окно или нажали ESC, то выход из игры
            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE # на пробел стреляем
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]: # rotation_dir = True - крутимся по часовой
                self.spaceship.rotate(rotation_dir=True)
            elif is_key_pressed[pygame.K_LEFT]: # получаем отрицательные углы и крутимся против часовой
                self.spaceship.rotate(rotation_dir=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()


    def main_logic(self):
        """Основная логика игры: движения и столкновения объектов"""
        global score
        global lives

        for game_object in self.game_obj_list():
            game_object.move(self.window) # получаем новые координаты объекта

        if self.spaceship: # Если корабль на поле, проверяем его столкновения
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship): # если врезался, то проиграл, пока так...
                    # не успел дописать проверку здоровья
                    self.spaceship = None
                    self.message = "Вы проиграли!"
                    break


        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet): # если астероид столкнулся с пулей, то
                    self.asteroids.remove(asteroid) # удаляем астероид
                    self.bullets.remove(bullet) # удаляем пулю
                    score += 1 # прибавляем счет

                    position = get_random_position(self.window) # генерация новых астероидов взамен "убитых"
                    self.asteroids.append(Asteroid(position, self.asteroids.append))
                    break

        for bullet in self.bullets[:]:
            if not self.window.get_rect().collidepoint(bullet.position): # если пуля выходи за границу окна - она удаляется
                self.bullets.remove(bullet)


    def draw_objects(self):
        """"Перманентная отрисовка объекта на поле"""
        self.window.blit(self.background, (0, 0)) # отрисовка слоя фона

        for game_object in self.game_obj_list():
            game_object.draw(self.window) # отрисовка каждого объекта

        # окошко счета
        pygame.draw.rect(self.window, rect=(0, 0 , 90, 30), color='white')
        font = pygame.font.Font(None, 30)
        text_score = font.render(f"Счет: {score}", True, 'red')
        self.window.blit(text_score, (5,3, 100, 10))

        if self.message:
            print_text(self.window, self.message, self.font) # вызов функции отрисовки текста о проигрыше

        pygame.display.flip()
        self.clock.tick(60) # ограничение по кадрам в секунду, иначе астероиды летают как угорелые

    def game_obj_list(self):
        ''''Возвращает список сгенерированных объектов
            для последующей отрисовки'''
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

if __name__ == "__main__":
    game = Asteroids()
    game.main_loop()