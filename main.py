import pygame
from random import randint, choice

pygame.init()

# Код, описывающий окно программы
WIDTH = 600  # Ширина окна
HEIGHT = 400 # Высота окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

class Character:
    def __init__(self, x, y, speed, health, image_path, visidle: bool = True):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.image = pygame.image.load(image_path)
        self.visidle = visidle
    def show(self, screen):
        if self.visidle:
            screen.blit(self.image, (self.x, self.y))
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.visidle = False

class Enemy(Character):
    def move(self):
        self.x += self.speed * randint(-1, 1)
        self.y += self.speed * randint(-1, 1)

images_path = { 
    "shlepa": "images/shlepa.png",
    "cheremsha": "images/cheremsha.png",
    "asphalt": "images/asphalt.png",
}
loaded_images = {
    "asphalt": pygame.image.load(images_path["asphalt"])
}
# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 30  # Устанавливаем нужное значение FPS
shlepa = Character(200, HEIGHT - 100, 10, 100, images_path["shlepa"], True)

# Игровые переменные, если надо, описываем в этом блоке

# Игровой цикл и флаг выполнения программы
game_run = True
while game_run:
    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    # БЛОК ИГРОВОЙ ЛОГИКИ (обновление переменных)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        shlepa.y -= shlepa.speed
    if keys[pygame.K_s]:
        shlepa.y += shlepa.speed
    if keys[pygame.K_a]:
        shlepa.x -= shlepa.speed
    if keys[pygame.K_d]:
        shlepa.x += shlepa.speed
    
    # БЛОК ОТРИСОВКИ ОБЪЕКТОВ В ОКНЕ ПРОГРАММЫ
    screen.blit(loaded_images["asphalt"], (0, 0), (0, 0, WIDTH, HEIGHT))
    shlepa.show(screen)
    
    # Обновление экрана

    pygame.display.flip()  # Отображение нарисованных объектов
    clock.tick(FPS)  # Контроль FPS

pygame.quit()