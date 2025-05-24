from pygame import *

'''Необходимые классы'''

# класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        # для движение врага
        self.rect.x -= self.speed
        if self.rect.x < win_width - 250:
            self.speed *= -1 
        if self.rect.x > win_width - 70:
            self.speed *= -1 

class Wall(sprite.Sprite):
    def __init__(self, R=0, G=0, B=0, x=0, y=0, wall_width=10, wall_height=50):
        super().__init__()  # Добавлено для корректной инициализации родительского класса
        self.image = Surface((wall_width, wall_height))
        self.image.fill((R, G, B))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

walls = [
    Wall(154, 205, 50, 100, 20, 450, 10),
    Wall(154, 205, 50, 100, 480, 350, 10),
    Wall(154, 205, 50, 100, 20, 10, 380),
    Wall(154, 205, 50, 100, 400, 250, 10),
    Wall(154, 205, 50, 350, 150, 10, 250),
    Wall(154, 205, 50, 450, 150, 10, 340),
    Wall(154, 205, 50, 450, 150, 100, 10),
]

# Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Название вашего проекта")
# фон проекта
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
# Персонажи игры:
player = Player('hero.png', 10, 10, 5)
monstr = Enemy('cyborg.png', win_width - 80, 280, 3)
gold = GameSprite('treasure.png', win_width - 80, win_height - 80, 0)

game = True
finish = False
clock = time.Clock()
FPS = 60
# музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()  # воспроизведёт звук

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font1 = font.Font(None, 80)
win_text = font1.render('you win', True, (0, 222, 0))
lose_text = font1.render('you lose', True, (219, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        for w in walls:
            w.draw_wall()
        gold.reset()
        player.reset()
        player.update()
        monstr.reset()
        monstr.update()
        
        if sprite.collide_rect(player, monstr) or any(sprite.collide_rect(player, wall) for wall in walls):
            window.blit(lose_text, (250, 200))
            kick.play()
            finish = True
        if sprite.collide_rect(player, gold):
            window.blit(win_text, (250, 200))  # Исправлено на правильное имя переменной
            money.play()
            finish = True
        
        display.update()
    else:
        time.wait(2000)
        player.rect.x = 10
        player.rect.y = 10
        finish = False
    clock.tick(FPS)
