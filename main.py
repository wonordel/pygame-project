import os # для № 1
import platform # для № 1
import pygame
from random import randint

# ===== ФИКС ЗВУКА ДЛЯ DISCORD ===== от chatgpt, фикс для дискорда и наверное для винды, необязателен № 1

system = platform.system()

if system == "Windows":
    os.environ["SDL_AUDIODRIVER"] = "directsound"

elif system == "Linux":
    # PipeWire/PulseAudio
    os.environ["SDL_AUDIODRIVER"] = "pulse"

# ==================================



pygame.init()
pygame.mixer.init()

# Код, описывающий окно программы
WIDTH = 1000  # Ширина окна X
HEIGHT = 1000 # Высота окна Y
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шлёпа против черемши")

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def play_music(file, volume=1):
    pygame.mixer.music.stop()
    
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

def load_image(path, fallback_color, size=(80, 80), use_alpha=True): # by Gemini, чтобы не лагало :)
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        # Оптимизация 2: Преобразование формата пикселей в формат экрана (ускоряет отрисовку до 10 раз!)
        if use_alpha:
            return image.convert_alpha()
        else:
            return image.convert()
    except pygame.error:
        # Если картинка не найдена, создаем цветную заглушку
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf.convert()

class Character:
    def __init__(self, x, y, speed, image_path, fallback_color, visidle: bool = True):
        self.x = x
        self.y = y
        self.defx = x
        self.defy = y
        self.speed = speed
        self.defspeed = speed
        
        # Безопасная загрузка
        self.image = load_image(image_path, fallback_color)
        self.rect = self.image.get_rect(center=(x, y)) # от gemini, оптимизация чтобы не лагало (до этого даже на топовом процессоре лагало) № 2
        self.half_width = self.image.get_width() // 2
        self.half_height = self.image.get_height() // 2
        
        self.visidle = visidle

    def show(self, screen):
        if self.visidle:
            screen.blit(self.image, (self.x - self.half_width, self.y - self.half_height))

    def reset(self):
        self.x = self.defx
        self.y = self.defy
        self.speed = self.defspeed
    
    def check_in_wall(self):
        # от gemini, оптимизация № 2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(Character):
    def __init__(self, x, y, speed, image_path, fallback_color, smart_moving: bool = True, visidle: bool = True):
        Character.__init__(self, x, y, speed, image_path, fallback_color, visidle)
        self.smart_moving = smart_moving

    def _move_x_(self, x):
        if x != self.x:
            if self.x > x:
                if self.x - x < self.speed:
                    self.x = x
                else:
                    self.x -= self.speed
            elif self.x < x:
                if x - self.x < self.speed:
                    self.x = x
                else:
                    self.x += self.speed

    def _move_y_(self, y):
        if y != self.y:
            if self.y > y:
                if self.y - y < self.speed:
                    self.y = y
                else:
                    self.y -= self.speed
            elif self.y < y:
                if y - self.y < self.speed:
                    self.y = y
                else:
                    self.y += self.speed
        
    def move(self, x, y):
        if self.visidle:
            if self.smart_moving:
                if x != self.x and y != self.y:
                    self._move_x_(x)
                    self._move_y_(y)
                elif x != self.x:
                    self._move_x_(x)
                elif y != self.y:
                    self._move_y_(y)
            else:
                if x != self.x:
                    self._move_x_(x)
                elif y != self.y:
                    self._move_y_(y)
            self.check_in_wall()


images_path = { 
    "shlepa": "images/shlepa.png",
    "cheremsha": "images/cheremsha.png",
    "asphalt": "images/asphalt.png",
    "brdish": "images/brdish.png"
}

# Загружаем фон асфальта (или создаем серый фон, если картинки нет)
bg_image = load_image(images_path["asphalt"], (50, 50, 50), (WIDTH, HEIGHT))

# Создаём контроль FPS
clock = pygame.time.Clock()
frames = 0
frames_from_respawn = 0
red_frames = 0

# Игровые переменные
FPS = 60  
font = pygame.font.SysFont("Arial", 36)

# Создаем персонажей
# Аргументы: x, y, speed, путь, цвет-заглушка (на случай если картинки нет)
shlepa = Character(200, HEIGHT - 100, 5, images_path["shlepa"], (230, 190, 150))
vead = False
enemys = [
    Enemy(400, 100, 2, images_path["cheremsha"], (0, 255, 0)), 
    Enemy(800, 100, 3.5, images_path["brdish"], (255, 0, 0), False)
]

def game_over():
    global shlepa, enemys, frames_from_respawn, vead
    frames_survived = frames_from_respawn
    frames_from_respawn = 0
    vead = True
    
    for enemy in enemys:
        enemy.reset()
    shlepa.reset()
    
    return frames_survived

# Игровой цикл и флаг выполнения программы
game_run = True
play_music("sounds/music.ogg")
while game_run:
    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
    
    keys = pygame.key.get_pressed()
    if not vead:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            shlepa.x -= shlepa.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            shlepa.x += shlepa.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            shlepa.y -= shlepa.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            shlepa.y += shlepa.speed

        shlepa.check_in_wall()

        for enemy in enemys:
            enemy.move(shlepa.x, shlepa.y)

        for enemy in enemys:
            if distance(shlepa.x, shlepa.y, enemy.x, enemy.y) < (shlepa.half_width + enemy.half_width) * 0.8:
                frames_survived = game_over()
        screen.blit(bg_image, (0, 0))


        shlepa.show(screen)
        for enemy in enemys:
            enemy.show(screen)


        seconds_survived = round(frames_from_respawn / FPS, 1)
        score_text = font.render(f"Время выживания: {seconds_survived} сек.", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
    else:
        pygame.mixer.music.stop()
        screen.fill((255, 0, 0))
        score_text = font.render(f"Время выживания: {round(frames_survived // FPS, 1)}", True, (255, 255, 255))
        screen.blit(font.render("Нажмите пробел чтобы продолжить...", True, (255, 255, 255)), (WIDTH // 2 - 130, HEIGHT // 2 + 50))
        screen.blit(score_text, (WIDTH // 2 - 130, HEIGHT // 2))
        red_frames += 1
        if keys[pygame.K_SPACE]:
            vead = False
            red_frames = 0
            if randint(1, 1000) == 1:
                play_music("sounds/music_vocice.ogg")
            else:
                play_music("sounds/music.ogg")
        
    # Обновление экрана
    pygame.display.flip()

    # Контроль времени и тики
    clock.tick(FPS)
    frames += 1
    frames_from_respawn += 1
    
pygame.quit()
