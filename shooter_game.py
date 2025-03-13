from pygame import *
from random import randint

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Pym pam')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
font.init()

game = True
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_height, player_width, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

lost = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -80
            self.rect.x = randint(0, 620)
            self.speed = randint(1,3)
            lost = lost + 1

killm = 0

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

player = Player('rocket.png', 200, 400, 100, 80, 10)
monsters = sprite.Group()
bullets = sprite.Group()


for i in range(5):
    monster = Enemy('ufo.png', randint(0, 620), -80, 50, 80, randint(1, 3))
    monsters.add(monster)

font1 = font.SysFont("Arial", 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    window.blit(background, (0, 0))
    text_lose = font1.render('Пропушено: ' + str(lost), 1, (255, 51, 255))
    window.blit(text_lose, (10, 10))
    text_kill = font1.render('Подбито: ' + str(killm), 1, (255, 81, 255))
    window.blit(text_kill, (10, 50))
    if sprite.spritecollide(player, monsters, False):
        game = False
    if sprite.groupcollide(monsters, bullets, True, True):
        monster = Enemy('ufo.png', randint(0, 620), -80, 50, 80, randint(1, 3))
        monsters.add(monster)
        killm = killm + 1
    if lost == 3:
        game = False
    player.reset()
    player.update()
    monsters.update()
    monsters.draw(window)
    bullets.update()
    bullets.draw(window)
    display.update()
    clock.tick(60)