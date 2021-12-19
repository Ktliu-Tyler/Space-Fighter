import pygame
import random
import os

FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

WIDTH = 500
HEIGHT = 600

rocks_num = 15

t = open('score.txt', 'r')
highest_score = int(t.readline())
last_score = int(t.readline())
t.close()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空戰機")
clock = pygame.time.Clock()

background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img0 = pygame.image.load(os.path.join("img", "player0.png")).convert()
player_img1 = pygame.image.load(os.path.join("img", "player1.png")).convert()
player_img2 = pygame.image.load(os.path.join("img", "player2.png")).convert()
player_img0.set_colorkey(BLACK)
player_img1.set_colorkey(BLACK)
player_img2.set_colorkey(BLACK)
player_mini_img = pygame.transform.scale(player_img0, (25,19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
boss_img0 = pygame.image.load(os.path.join("img", "Boss0.png")).convert()
boss_img1 = pygame.image.load(os.path.join("img", "Boss1.png")).convert()
boss_img2 = pygame.image.load(os.path.join("img", "Boss2.png")).convert()
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
boss_bullet_img = pygame.image.load(os.path.join("img", "boss_bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30,30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
power_imgs['shield'] =pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] =pygame.image.load(os.path.join("img", "gun.png")).convert()


shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))


expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]

pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.6)

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, hp_ori, x, y, color):
    if hp < 0:
        hp = 0
    BAR_LENGTH = hp_ori
    BAR_HEIGHT = 10
    fill = (hp/hp_ori)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_boss_health(surf, hp, hp_ori, x, y, color):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = (hp/hp_ori)*200
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, '太空戰機!!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, f'上回得分: {last_score}  最高得分: {highest_score}', 25, WIDTH/2, HEIGHT/2-35)
    draw_text(screen, '|   按下 \'a\' \'d\' 左右移動戰機   |', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '| 按空白鍵發射子彈摧毀石頭 |', 22, WIDTH/2, HEIGHT/2+25)
    draw_text(screen, '|  ~吃盾牌回血 吃閃電升級~ |', 22, WIDTH/2, HEIGHT/2+50)
    draw_text(screen, '|           挑戰最高分!!!!            |', 22, WIDTH/2, HEIGHT/2+75)
    draw_text(screen, '~~~按下任意鍵開始吧~~~', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img0, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 8
        self.health = 100
        self.life = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 4000:
            self.gun -= 1
            self.gun_time = now
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                self.image = pygame.transform.scale(player_img0, (50,38))
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun == 2:
                self.image = pygame.transform.scale(player_img0, (50,38))
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun == 3:
                self.image = pygame.transform.scale(player_img1, (50,38))
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery-10)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
            elif self.gun == 4:
                self.image = pygame.transform.scale(player_img1, (50,38))
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx+10, self.rect.centery-20)
                bullet4 = Bullet(self.rect.centerx-10, self.rect.centery-20)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        if self.gun > 4:
            self.gun = 4
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85/2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -10
        self.redius = 27

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Boss_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 7
        self.redius = 15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame ==  len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img0
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = -200
        self.health = 200
        self.health_ori = 200
        self.speedx = 3
        self.speedy = 3
        self.radius = 80
        self.hide = True
        self.time = pygame.time.get_ticks()
        self.shoot_time = pygame.time.get_ticks()
        self.shoot_rate = 1000

    def update(self):
        if not(self.hide):
            if self.rect.centery < 20:
                self.rect.centery += 3
            else :
                # self.rect.centery = 100
                self.rect.centerx += self.speedx
                self.rect.centery += self.speedy/3
                if self.rect.right > WIDTH:
                    self.speedx *= -1
                    self.rect.right = WIDTH
                elif self.rect.left < 0:
                    self.speedx *= -1
                    self.rect.left = 0

                if self.rect.bottom > 300:
                    self.speedy *= -1
                    self.rect.bottom = 300
                elif self.rect.top < 20:
                    self.speedy *= -1
                    self.rect.top = 20
                now = pygame.time.get_ticks()
                if now - self.shoot_time > self.shoot_rate:
                    self.shoot_time = now
                    self.boss_shoot()

        elif boss.rect.centery > -150:
            boss.rect.centery -= 3
            if boss.rect.centery < -100:
                boss.rect.centery = -100
                boss.health = boss.health_ori

    def boss_out(self):
        boss.hide = False

    def boss_die(self):
        self.time = pygame.time.get_ticks()
        boss.health_ori += 100
        boss.hide = True

    def boss_shoot(self):
        b1 = Boss_Bullet(self.rect.centerx-25,self.rect.bottom-10)
        b2 = Boss_Bullet(self.rect.centerx+25,self.rect.bottom-10)
        all_sprites.add(b1)
        all_sprites.add(b2)
        boss_bullets.add(b2)
        boss_bullets.add(b2)
        if self.health / self.health_ori * 200 > 150 :
            self.shoot_rate = 1000
            self.image = boss_img0
        elif self.health / self.health_ori * 200 < 150 and self.health / self.health_ori * 200 > 50:
            self.image = boss_img1
            self.shoot_rate = 500
        elif self.health / self.health_ori * 200 < 50 and self.health / self.health_ori * 200 > 0:
            self.image = boss_img2
            self.shoot_rate = 100
        self.image.set_colorkey(BLACK)
score = 0
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
boss = Boss()
all_sprites.add(boss)
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
for i in range(rocks_num):
    new_rock()

pygame.mixer.music.play(-1)

show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_rock()

    hits = pygame.sprite.spritecollide(player, boss_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= 10
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

    if player.health <= 0:
        die = Explosion(player.rect.center, 'player')
        all_sprites.add(die)
        die_sound.play()
        player.life -= 1
        player.health = 100
        player.hide()
        # running = False
    if boss.hide == False:
        hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            random.choice(expl_sounds).play()
            boss.health -= 2
            if boss.health < 0:
                boss.health = 0
            score+= 5
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.97:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)


    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 10
            shield_sound.play()
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            gun_sound.play()
            player.gunup()

    if boss.hide == True:
        now_time = pygame.time.get_ticks()
    if now_time - boss.time > 20000 and boss.rect.centery < 50 and boss.health > 0 :
        boss.boss_out()
    if boss.health <= 0 and boss.hide == False:
        boss.boss_die()
        score += 1000
        for i in range(5):
            pow = Power(boss.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        die = Explosion(boss.rect.center, 'player')
        all_sprites.add(die)
        die_sound.play()





    if player.life == 0 and not(die.alive()):
        show_init = True
        now_time = 0
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        boss = Boss()
        all_sprites.add(boss)
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        last_score = score
        if last_score > highest_score:
            highest_score = last_score
        t = open("score.txt",'w')
        t.write(f"{highest_score}\n{last_score}")
        t.close()
        score = 0
        for i in range(rocks_num):
            new_rock()

    # screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, "Score: "+ str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health,100, 5, 15, GREEN)
    draw_boss_health(screen, boss.health / boss.health_ori * 200, 200, boss.rect.centerx-95, boss.rect.top+10, RED)
    draw_lives(screen, player.life, player_mini_img, WIDTH-100, 15)
    pygame.display.update()
    print(boss.health)

pygame.quit()