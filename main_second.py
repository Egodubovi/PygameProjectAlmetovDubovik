import os
import random
import sys
import threading
import pygame
from subprocess import call


YELLOW = (255, 0, 0)
BLUE = (0, 0, 255)


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def restart():
    threading.Thread(target=call, args=[["python", "main_second.py"]]).start()
    pygame.quit()
    sys.exit()


def next_level():
    call(["python", "main_second.py"])
    sys.exit()


def return_menu():
    threading.Thread(target=call, args=[["python", "menu.py"]]).start()
    pygame.quit()
    sys.exit()


def previous_level():
    threading.Thread(target=call, args=[["python", "main.py"]]).start()
    pygame.quit()
    sys.exit()


def print_text1(message, x, y, font_size, font_color=(255, 255, 255), font_type='freesansbold.ttf'):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def pause():
    paused = True
    pygame.mouse.set_visible(True)
    mouse_pos = 0, 0
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
        screen.blit(load_image('menu.png'), (0, 0))
        rest = screen.blit(restart_image, (200, 500))
        previous = screen.blit(previous_image, (80, 520))
        men = screen.blit(load_image('menu_btn.png'), (140, 620))
        if rest.collidepoint(mouse_pos):
            restart()
        if previous.collidepoint(mouse_pos):
            previous_level()
        if men.collidepoint(mouse_pos):
            return_menu()
        print_text1("Paused. Press enter to continue", 0, 200, 30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(15)


class Stars(pygame.sprite.Sprite):
    image = load_image("star.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.add(stars_sprite)
        self.x = random.random() * width
        self.y = random.random() * height
        self.image = Stars.image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args):
        self.rect.y += 2
        if self.rect.y >= 800:
            self.rect.y = 0
        if MainSuttle.health <= 0:
            self.kill()


class MainSuttle(pygame.sprite.Sprite):
    shuttle_image = load_image("shuttle3.png")
    bullit_image = load_image("bullit.png")
    speed = 3
    health = 3

    def __init__(self, *group):
        super().__init__(*group)
        self.add(shuttle_sprite)
        self.image = MainSuttle.shuttle_image
        self.rect = self.image.get_rect()
        self.rect.x = 217
        self.rect.y = 700
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self, *args):
        if args and pygame.key.get_pressed()[pygame.K_w] and self.rect.y > 30:
            self.rect.y -= MainSuttle.speed
        elif args and pygame.key.get_pressed()[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= MainSuttle.speed
        elif args and pygame.key.get_pressed()[pygame.K_s] and self.rect.y < 780:
            self.rect.y += MainSuttle.speed
        elif args and pygame.key.get_pressed()[pygame.K_d] and self.rect.x < 450:
            self.rect.x += MainSuttle.speed
        elif args and pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = Bullet(self.rect.x + 24, self.rect.y - 5)
            all_sprites.add(bullet)
            bullets.add(bullet)
        if pygame.sprite.spritecollideany(self, boss_sprite):
            MainSuttle.health = 0
            self.kill()
        if MainSuttle.health <= 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    damage = 2

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 3))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, mobs_sprite):
            self.image.set_alpha(0)
        if pygame.sprite.spritecollideany(self, boss_sprite):
            self.image.set_alpha(0)
        if pygame.sprite.spritecollideany(self, asteroids_sprite):
            self.image.set_alpha(0)
        if MainSuttle.health <= 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    mob_image = load_image('mob.png')

    def __init__(self, x, y, xn, s, live, *group):
        super().__init__(*group)
        self.image = Mob.mob_image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.kills = 0
        self.rect.x = xn
        self.mob_hp = 100
        self.x = x
        self.y = y
        self.live = live
        self.speed = s

    def update(self):
        if self.rect.x < self.x or self.rect.x > self.x:
            self.rect.x += self.speed
        if pygame.sprite.spritecollideany(self, bullets):
            self.mob_hp -= Bullet.damage
        if self.mob_hp <= 0:
            self.live = False
            self.kill()
            del mob_lst[1]
        elif pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health -= 1
            self.kill()
            del mob_lst[-1]
        elif MainSuttle.health <= 0:
            self.kill()
            del mob_lst[-1]


class StrongerMob(pygame.sprite.Sprite):
    stronger_image = load_image('strongermob.png')

    def __init__(self, x, y, xn, s, live, *group):
        super().__init__(*group)
        self.image = StrongerMob.stronger_image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.kills = 0
        self.rect.x = xn
        self.mob_hp = 250
        self.x = x
        self.y = y
        self.live = live
        self.speed = s

    def update(self):
        if self.rect.x < self.x or self.rect.x > self.x:
            self.rect.x += self.speed
        if pygame.sprite.spritecollideany(self, bullets):
            self.mob_hp -= Bullet.damage
        if self.mob_hp <= 0:
            self.live = False
            self.kill()
            del mob_lst[-1]
        elif pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health -= 1
            self.kill()
            del mob_lst[-1]
        elif MainSuttle.health <= 0:
            self.kill()
            del mob_lst[-1]


class StrongestMob(pygame.sprite.Sprite):
    strongest_image = load_image('strongestmob.png')

    def __init__(self, x, y, xn, s, live, *group):
        super().__init__(*group)
        self.image = StrongestMob.strongest_image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.kills = 0
        self.rect.x = xn
        self.mob_hp = 550
        self.x = x
        self.y = y
        self.live = live
        self.speed = s

    def update(self):
        if self.rect.x < self.x or self.rect.x > self.x:
            self.rect.x += self.speed
        if pygame.sprite.spritecollideany(self, bullets):
            self.mob_hp -= Bullet.damage
        if self.mob_hp <= 0:
            self.live = False
            self.kill()
            del mob_lst[-1]
        elif pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health -= 1
            self.kill()
            del mob_lst[-1]
        elif MainSuttle.health <= 0:
            self.kill()
            del mob_lst[-1]


class Bomb(pygame.sprite.Sprite):
    bomb = load_image('bomb.png')

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Bomb.bomb
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.kills = 0
        self.rect.x = x
        self.x = x
        self.y = y

    def update(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health -= 1
            self.kill()
        elif self.rect.y >= 800:
            self.kill()
        elif MainSuttle.health <= 0:
            self.kill()


class Improvement(pygame.sprite.Sprite):
    speed = load_image('speed.png')
    heart = load_image('heart.png')
    x2 = load_image('x2.png')

    def __init__(self, x, y, k, *groups):
        super().__init__(*groups)
        if k == 3:
            self.image = Improvement.speed
        elif k == 1:
            self.image = Improvement.heart
        elif k == 2:
            self.image = Improvement.x2
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.k = k
        self.rect.x = x
        self.x = x
        self.y = y

    def update(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, shuttle_sprite):
            if self.k == 2:
                Bullet.damage *= 2
            elif self.k == 3:
                MainSuttle.speed += 1
            elif self.k == 1:
                MainSuttle.health += 1
            self.kill()
        elif self.rect.y >= 800:
            self.kill()
        elif MainSuttle.health <= 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    boss_image = load_image('boss1.png')

    def __init__(self, x, y, live, *group):
        super().__init__(*group)
        self.image = Boss.boss_image
        self.rect = self.image.get_rect()
        self.rect.y = -60
        self.kills = 0
        self.rect.x = 190
        self.boss_hp = 7000
        self.x = x
        self.y = y
        self.live = live

    def update(self):
        if self.rect.y <= self.y:
            self.rect.y += 1
        if pygame.sprite.spritecollideany(self, bullets):
            self.boss_hp -= Bullet.damage
        if self.boss_hp <= 0:
            self.live = False
            self.kill()
            del mob_lst[-1]
        elif pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health = 0
            self.kill()
            del mob_lst[-1]


class BossBomb(pygame.sprite.Sprite):
    bomb = load_image('bomb.png')

    def __init__(self, x, y, xs, ys, *groups):
        super().__init__(*groups)
        self.image = Bomb.bomb
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.kills = 0
        self.rect.x = x
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.f = True

    def update(self):
        if self.rect.x < self.xs and self.f:
            self.rect.x += 1
        elif self.rect.x > self.xs and self.f:
            self.rect.x -= 1
        if self.rect.y < self.ys and self.f:
            self.rect.y += 1
        elif self.rect.y > self.ys and self.f:
            self.rect.y -= 1
        elif self.rect.y == self.ys or not self.f:
            self.rect.y += 1
            self.f = False
        if pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health -= 1
            self.kill()
        elif self.rect.y >= 800:
            self.kill()
        elif MainSuttle.health <= 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    asteroid_image = load_image('asteroid.png')

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Asteroid.asteroid_image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.kills = 0
        self.rect.x = x
        self.x = x
        self.y = y
        self.f = True
        self.asteroid_hp = 100

    def update(self):
        self.rect.y += 3
        if pygame.sprite.spritecollideany(self, bullets):
            self.asteroid_hp -= Bullet.damage
        if pygame.sprite.spritecollideany(self, shuttle_sprite):
            MainSuttle.health -= 1
            self.kill()
        elif self.rect.y >= 800:
            self.kill()
        elif MainSuttle.health <= 0:
            self.kill()
        elif self.asteroid_hp <= 0:
            self.kill()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    size = width, height = 480, 800
    screen = pygame.display.set_mode(size)

    bullets = pygame.sprite.Group()
    improvement_sprite = pygame.sprite.Group()
    bomb_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    boss_sprite = pygame.sprite.Group()
    shuttle_sprite = pygame.sprite.Group()
    stars_sprite = pygame.sprite.Group()
    mobs_sprite = pygame.sprite.Group()
    asteroids_sprite = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()

    shuttle = MainSuttle(all_sprites)

    for i in range(300):
        Stars(all_sprites)

    clock = pygame.time.Clock()
    running = True
    move = False
    shoot = False
    cursor_image = load_image('cursor.png')
    win_image = load_image('youwin.png')
    lose_image = load_image('youlose.png')
    heart_image = load_image('heart.png')
    pause_image = load_image('pause.png')
    restart_image = load_image('restart.png')
    next_image = load_image('next.png')
    previous_image = load_image('previous.png')
    rest = pygame.Rect(100, 100, 50, 50)
    next = pygame.Rect(100, 100, 50, 50)
    previous = pygame.Rect(100, 100, 50, 50)
    men = pygame.Rect(100, 100, 50, 50)
    mouse_pos = 0, 0
    delta = 5000
    wave = 1
    count = 0
    wave_time = 0
    bomb_time = 10000000
    all = 10000000000
    boss_bomb_time = 10000000000000
    improvement_time = 10000000
    asteroids_time = 100000000
    mob_lst = []
    k = 1
    time = pygame.time.get_ticks()
    asteroids = 0

    while running:
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 0))
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                move = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                shoot = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
                pause()
        time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        if time >= delta and wave == 1:
            c = 140
            for i in range(5):
                mob = Mob(c, 150, 0, 2, True, all_sprites)
                mob_lst.append(mob)
                mobs_sprite.add(mob)
                c += 40
            c = 140
            for i in range(5):
                mob = StrongerMob(c, 100, 0, 2, True, all_sprites)
                mob_lst.append(mob)
                mobs_sprite.add(mob)
                c += 40
            c = 140
            for i in range(5):
                mob = StrongestMob(c, 50, 0, 2, True, all_sprites)
                mob_lst.append(mob)
                mobs_sprite.add(mob)
                c += 40
            wave = 2
            wave_time = time + delta
            bomb_time = pygame.time.get_ticks()
            improvement_time = pygame.time.get_ticks()
        if not mob_lst and wave == 2 and count == 0:
            all = pygame.time.get_ticks()
            count += 1
        if time >= all + delta and wave == 2 and len(mob_lst) <= 0:
            c = 400
            for i in range(7):
                mob = Mob(c, 200, 480, -2, True, all_sprites)
                mob_lst.append(mob)
                mobs_sprite.add(mob)
                c -= 60
            c = 40
            for i in range(7):
                mob = StrongerMob(c, 150, 0, 2, True, all_sprites)
                mob_lst.append(mob)
                mobs_sprite.add(mob)
                c += 60
            c = 400
            for i in range(7):
                mob = StrongestMob(c, 100, 480, -2, True, all_sprites)
                mob_lst.append(mob)
                mobs_sprite.add(mob)
                c -= 60
            wave = 3
            wave_time = time + delta
            bomb_time = pygame.time.get_ticks()
            improvement_time = pygame.time.get_ticks()
        if not mob_lst and wave == 3 and count == 1:
            all = pygame.time.get_ticks()
            asteroids_time = all
            count += 1
        if time >= asteroids_time + delta / 10 and wave == 3 and len(mob_lst) <= 0:
            if asteroids >= 30:
                wave = 4
            asteroids += 1
            asteroid = Asteroid(random.randint(0, 450), -30, all_sprites)
            asteroids_sprite.add(asteroid)
            asteroids_time = pygame.time.get_ticks()
        if not mob_lst and wave == 4 and count == 2:
            all = pygame.time.get_ticks()
            count += 1
            wave = 0
        if time >= all + delta and wave == 0:
            boss = Boss(190, 100, True, all_sprites)
            mob_lst.append(boss)
            boss_sprite.add(boss)
            wave = -1
            boss_bomb_time = pygame.time.get_ticks()
        if len(mob_lst) >= 1 and time >= bomb_time + delta and wave >= 1:
            m = mob_lst[random.randint(0, len(mob_lst) - 1)]
            o = mob_lst[random.randint(0, len(mob_lst) - 1)]
            b = mob_lst[random.randint(0, len(mob_lst) - 1)]
            if m.live:
                bomb1 = Bomb(m.rect.x + 10, m.rect.y + 30, all_sprites)
                bomb_sprite.add(bomb1)
            if o.live:
                bomb2 = Bomb(o.rect.x + 10, o.rect.y + 30, all_sprites)
                bomb_sprite.add(bomb2)
            if b.live:
                bomb3 = Bomb(b.rect.x + 10, b.rect.y + 30, all_sprites)
                bomb_sprite.add(bomb3)
            bomb_time = pygame.time.get_ticks()
        if len(mob_lst) >= 1 and time >= improvement_time + delta * 1.8 and wave >= 1:
            imp = mob_lst[random.randint(0, len(mob_lst) - 1)]
            if imp.live:
                k = random.randint(1, 3)
                improve = Improvement(imp.rect.x + 10, imp.rect.y + 30, k, all_sprites)
                improvement_sprite.add(improve)
                improvement_time = pygame.time.get_ticks()
        if len(mob_lst) >= 1 and time >= boss_bomb_time + delta / 4 and wave == -1:
            m = mob_lst[0]
            if m.live:
                bomb1 = BossBomb(m.rect.x + 50, m.rect.y + 60, shuttle.rect.x, shuttle.rect.y,  all_sprites)
                bomb_sprite.add(bomb1)
            boss_bomb_time = pygame.time.get_ticks()
        if move:
            for shuttle in shuttle_sprite:
                shuttle.update(event)
        if shoot:
            for shuttle in shuttle_sprite:
                shuttle.update(event)
        x = 50
        if MainSuttle.health and wave != -2:
            screen.blit(pause_image, (5, 5))
            for i in range(MainSuttle.health):
                screen.blit(heart_image, (x, 5))
                x += 30
        if not mob_lst and wave == -1 or wave == -2:
            screen.fill((0, 0, 0))
            screen.blit(win_image, (0, 0))
            pygame.mouse.set_visible(True)
            wave = -2
            rest = screen.blit(restart_image, (200, 600))
            previous = screen.blit(previous_image, (80, 620))
            men = screen.blit(load_image('menu_btn.png'), (140, 700))
        elif shuttle.health <= 0:
            wave = -5
            pygame.mouse.set_visible(True)
            screen.fill((0, 0, 0))
            screen.blit(lose_image, (0, 0))
            rest = screen.blit(restart_image, (200, 600))
            previous = screen.blit(previous_image, (80, 620))
            men = screen.blit(load_image('menu_btn.png'), (140, 700))
        if rest.collidepoint(mouse_pos):
            restart()
            running = False
        if previous.collidepoint(mouse_pos):
            previous_level()
            running = False
        if men.collidepoint(mouse_pos):
            return_menu()
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
