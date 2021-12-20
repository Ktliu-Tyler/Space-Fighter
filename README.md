# Space Fighter<br>
## Author: Tyler<br>
### 利用pygame進行的遊戲開發學習<br>
* **遊戲介紹**<br>
  玩家可透過鍵盤a和d對遊戲中機體進行左右移動，
  並利用空格鍵進行子彈的發射。
  吃到閃電可以提升機體，吃到能量可以回血。
  每10秒鐘會出一次BOSS，BOSS在血量為50%及25%時會提升能力，增加攻擊速度。
  持續挑戰存活可以獲得分數!
* **執行後的遊戲介面**<br>
  <img src="/github_img/Example2.jpg" width="50%" height="50%"/>

* **遊戲中的畫面**<br>
  <img src="/github_img/Example.jpg" width="50%" height="50%"/>

* **程式碼**<br>
  * 建立玩家的Class
    ```python
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

    ```
  * 建立掉落石頭的Class
    ```python
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
    ```
  * 建立玩家子彈的Class
    ```python
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
    ```
  * 建立魔王的Class
    ```python
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
    ```
  * 建立魔王的子彈Class
    ```python
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
    ```
  * 建立能量物件Class
    ```python
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
    ```
  * 建立爆炸特效Class
    ```python
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
    ```
#### 參考影片:<br>
Youtube pygame教學影片<https://www.youtube.com/watch?v=61eX0bFAsYs>
