import os
import random
import sys
import threading
from subprocess import call

import pygame

pygame.init()
button_sound = pygame.mixer.Sound("button.wav")
pygame.init()
pygame.display.set_caption('Game')
size = width, height = 480, 800
screen = pygame.display.set_mode(size)
running = False
YELLOW = (255, 0, 0)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def lvl1():
    threading.Thread(target=call, args=[["python", "main.py"]]).start()
    pygame.quit()
    sys.exit()


def lvl2():
    threading.Thread(target=call, args=[["python", "main_second.py"]]).start()
    pygame.quit()
    sys.exit()


def print_text1(message, x, y, font_size, font_color=(255, 255, 255), font_type='freesansbold.ttf'):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def start_game():
    global running
    check_winner_variable = show_menu()
    if check_winner_variable == '1':
        running = True
    return running


def show_menu():
    global running
    menu_back = pygame.image.load("menu.png")
    sh = True
    start = Button(200, 70)
    btn1 = Button(200, 70)
    btn2 = Button(200, 70)
    while sh:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and 150 <= pos[0] <= 350 and 250 <= pos[1] <= 320:
                pygame.mixer.Sound.play(button_sound)
                lvl1()
            elif event.type == pygame.MOUSEBUTTONDOWN and 35 <= pos[0] <= 235 and 350 <= pos[1] <= 420:
                pygame.mixer.Sound.play(button_sound)
                lvl1()
            elif event.type == pygame.MOUSEBUTTONDOWN and 245 <= pos[0] <= 445 and 350 <= pos[1] <= 420:
                pygame.mixer.Sound.play(button_sound)
                lvl2()

        screen.blit(menu_back, (0, 0))
        start.draw(140, 250, "Play", start_game, 50)
        print_text1("Play", 185, 255, 50)
        btn1.draw(35, 350, "LVL 1", start_game, 40)
        print_text1("lvl 1", 85, 355, 50)
        btn2.draw(245, 350, "LVL 2", start_game, 40)
        print_text1("lvl 2", 295, 355, 50)
        print_text1("Space battle", 90, 150, 50)

        pygame.display.update()


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.impos_color = (168, 168, 168)
        self.possible_color = (99, 99, 99)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.possible_color, (x, y, self.width, self.height))

            if click[0] == 1 and action is not None:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                action()

        else:
            pygame.draw.rect(screen, self.impos_color, (x, y, self.width, self.height))


show_menu()
