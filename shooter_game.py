
from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
   monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
   asteroids.add(asteroid)
game = True
finish = False
clock = time.Clock()
FPS = 60
lost = 0
score = 0
num_fire = 0
rel_time = False
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 40)
win = font1.render('ПОБЕДА!', True, (255,255,255))
lose = font1.render('ОХ!', True, (255,255,255))
bullets = sprite.Group()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire +=1
                    fire_sound.play()
                    ship.fire()
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish != True:
        window.blit(background,(0, 0))
        text = font1.render('Счёт:' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text2 = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text2, (10,50))
        bullets.update()
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                text3 = font1.render('Wait, reload...', 1, (255,255,255))
                window.blit(text3, (250, 460))
            else:
                num_fire = 0
                rel_time = False
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprites_list:
            score +=1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >=3:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
        ship.update()
        monsters.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window) 
        bullets.draw(window)
        asteroids.draw(window) 
    display.update()
    clock.tick(FPS)





