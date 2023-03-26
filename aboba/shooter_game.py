from pygame import *
from random import randint
import time as Timer
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    prev_time = Timer.time()
    num_fire = 0
    rel_flag = False
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < (WIDTH - self.rect.width - 5):
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        if Timer.time() - self.prev_time < 2 and self.rel_flag:
            return
        if Timer.time() - self.prev_time > 2 and self.rel_flag:
            self.rel_flag = False
            self.num_fire = 0
        if Timer.time() - 0.3 > self.prev_time:
            x = self.rect.centerx
            y = self.rect.top
            Bullet = bullet('bullet.png', x, y, 15, 20, 5)        
            bullets.add(Bullet)
            self.prev_time = Timer.time()
            self.num_fire += 1
            if self.num_fire >= 5:
                self.rel_flag = True

    def reset(self):
        super().reset()
        if Timer.time() - self.prev_time > 2 and self.rel_flag:
            self.rel_flag = False
            self.num_fire = 0
        if self.rel_flag:
            reload_ = my_font.render("Перезарядка...", True, (255, 255, 255))
            reload_rect =  reload_.get_rect()
            reload_rect.centerx = WIDTH // 2
            reload_rect.centery = HEIGHT // 2
            mw.blit(reload_, (reload_rect.x, reload_rect.y))

class bullet(GameSprite):
    def update(self):
        self.rect.x == self.speed
        if self.rect.y <= 0:
            self.kill()
        self.rect.y -= self.speed

    def fire(self):
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -60
            self.speed = randint(1, 8)
            global lost, HP
            lost += 1
            damage = randint(650, 950)
            HP -= damage

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -60
            self.rect.x = randint(0, 650)
            self.speed = randint(5, 10)

class MedKit(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -60
            self.rect.x = randint(0, 650)
            self.speed = randint(2, 4)

class Laser(GameSprite):
    def update(self):
        self.rect.y

WIDTH, HEIGHT = 700, 500
FPS = 60
lost = 0
score = 0
HP = 100000
defense = 1

mw = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Shooter | шутер')

background = transform.scale(image.load('galaxy.jpg'), (WIDTH, HEIGHT))
player = Player('rocket.png', WIDTH // 2, HEIGHT - 70, 65, 65, 10)

bullets = sprite.Group()
meteors = sprite.Group()
monsters = sprite.Group()
buffs = sprite.Group()

for i in range(250):
    enemy = Enemy('ufo.png', randint(0, 650), -100, 70, 70, randint(1, 8))
    monsters.add(enemy)
for i in range(3):
    meteor = Meteor('asteroid.png', randint(0, 650), -100, 70, 70, randint(5, 10))
    meteors.add(meteor)
for i in range(1):
    medkit = MedKit('health.png', randint(0, 650), -100, 70, 70, randint(2, 4))
    buffs.add(medkit)

mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
my_font = font.SysFont('Arial', 30)
result_font = font.SysFont('Arial', 60)

clock = time.Clock()

game = True
finish = True
while game:
    mw.blit(background, (0, 0))
    if finish:
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(mw)
        bullets.update()
        bullets.draw(mw)
        meteors.update()
        meteors.draw(mw)
        buffs.update()
        buffs.draw(mw)
    missed_text = my_font.render('Пропущено: ' + str(lost), True, (225, 225, 225))
    score_text = my_font.render('Очков (нужно 2500): ' + str(score), True, (225, 225, 225))
    HP_text = my_font.render('Здоровье: ' + str(HP), True, (200, 225, 255))
    mw.blit(missed_text, (10, 10))
    mw.blit(score_text, (10, 50))
    mw.blit(HP_text, (10, 90))
    collided = sprite.groupcollide(bullets, monsters, True, True)
    collided_2 = sprite.spritecollide(player, meteors, True)
    collided_3 = sprite.spritecollide(player, buffs, True)
    if len(collided) > 0:
            for i in range(len(collided)):
                enemy = Enemy('ufo.png', randint(0, 650), -100, 70, 70, randint(1, 8))
                monsters.add(enemy)
                score += randint(10, 50)
    if len(collided_2) > 0:
        for i in range(len(collided_2)):
            meteor = Meteor('asteroid.png', randint(0, 650), -100, 70, 70, randint(5, 10))
            meteors.add(meteor)
            HP -= randint(3500,5000)
            score -= randint(10, 20)
    if len(collided_3) > 0:
        for i in range(len(collided_3)):
            medkit = MedKit('health.png', randint(0, 650), -100, 70, 70, randint(2, 4))
            buffs.add(medkit)
            HP += 3500
    if score > 2500:
        finish = False
        result_text = result_font.render('Победа', True, (0, 225, 0))
        mw.blit(result_text, (250, 250))
    if HP < 0:
        finish = False
        fail_text = result_font.render('Поражение', True, (225, 0, 0))
        mw.blit(fail_text, (250, 250))

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)