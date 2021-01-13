import pygame
import sys
import os
import copy
from random import randrange

HAVESOUND = True
LEVEL = 1
SPEED = 1.0
RESUME = True
CONT = True
pygame.init()
SOUNDNOM = pygame.mixer.Sound("data/omnom.mp3")
SOUNDNOUCH = pygame.mixer.Sound('data/ouch.mp3')
clock = pygame.time.Clock()
FPS = 60
CLR = {'active_but': (100, 100, 100),
       'notactive_but': (30, 30, 30),
       'board': (100, 100, 100),
       'snake': (0, 200, 0),
       'apple': (200, 0, 0),
       'title': (0, 0, 200)}


class Button(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y, text, notact, act, func=None):
        super().__init__(group)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, notact, (0, 0, width, height))
        self.font = pygame.font.Font(None, 30)
        self.text = text
        self.string = self.font.render(text, 1, pygame.Color('white'))
        self.image.blit(self.string, (10, 10))

        self.rect = pygame.Rect(x, y, width, height)
        self.act = act
        self.notact = notact
        self.func = func

    def update(self, pos):
        if self.rect.collidepoint(pos):
            pygame.draw.rect(self.image, self.act, (0, 0, self.width, self.height))
            self.image.blit(self.string, (10, 10))

        else:
            pygame.draw.rect(self.image, self.notact, (0, 0, self.width, self.height))
            self.image.blit(self.string, (10, 10))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            if self.func(self):
                return True

    def change_text(self, new_text):
        self.text = new_text
        self.string = self.font.render(self.text, 1, pygame.Color('white'))
        self.image.blit(self.string, (10, 10))


class Apple:
    def __init__(self, h, w):
        self.pos = None
        self.board_size = h, w

    def generate_new_pos(self, board, snake):
        y, x = self.board_size
        while True:
            xx = randrange(0, x)
            yy = randrange(0, y)
            if board[yy][xx] == 0 and (xx, yy) not in snake:
                self.pos = (xx, yy)
                break


class Snake:
    def __init__(self, mesto, h, w):
        self.mesto = mesto
        self.dead = False
        self.last_move = None
        self.dob = False
        self.board_size = h, w
        self.ru = load_image('snake_parts/ru.png', colorkey=-1)
        self.rd = load_image('snake_parts/rd.png', colorkey=-1)
        self.lu = load_image('snake_parts/lu.png', colorkey=-1)
        self.ld = load_image('snake_parts/ld.png', colorkey=-1)
        self.gor = load_image('snake_parts/goriz.png', colorkey=-1)
        self.vert = load_image('snake_parts/vert.png', colorkey=-1)
        self.hu = load_image('snake_parts/hu.png', colorkey=-1)
        self.hd = load_image('snake_parts/hd.png', colorkey=-1)
        self.hr = load_image('snake_parts/hr.png', colorkey=-1)
        self.hl = load_image('snake_parts/hl.png', colorkey=-1)
        self.tu = load_image('snake_parts/tu.png', colorkey=-1)
        self.td = load_image('snake_parts/td.png', colorkey=-1)
        self.tr = load_image('snake_parts/tr.png', colorkey=-1)
        self.tl = load_image('snake_parts/tl.png', colorkey=-1)

    def __len__(self):
        return len(self.mesto)

    def get_im(self, x, y):
        if (x, y) == self.mesto[-1]:
            x1, y1 = self.mesto[-2]
            if x1 == x and (y + 1 == y1 or y + 1 - self.board_size[0] == y1):
                return self.hu
            elif x1 == x and (y - 1 == y1 or y - 1 + self.board_size[0] == y1):
                return self.hd
            elif (x + 1 == x1 or x + 1 - self.board_size[1] == x1) and y == y1:
                return self.hl
            elif (x - 1 == x1 or x - 1 + self.board_size[1] == x1) and y == y1:
                return self.hr
        elif (x, y) == self.mesto[0]:
            x1, y1 = self.mesto[1]
            if x1 == x and (y + 1 == y1 or y + 1 - self.board_size[0] == y1):
                return self.td
            elif x1 == x and (y - 1 == y1 or y - 1 + self.board_size[0] == y1):
                return self.tu
            elif (x + 1 == x1 or x + 1 - self.board_size[1] == x1) and y == y1:
                return self.tr
            elif (x - 1 == x1 or x - 1 + self.board_size[1] == x1) and y == y1:
                return self.tl
        else:
            ind = self.mesto.index((x, y))
            x_1, y_1 = self.mesto[ind - 1]
            x1, y1 = self.mesto[ind + 1]
            if (((x - 1 == x_1 or x - 1 + self.board_size[1] == x_1) and (
                    x + 1 == x1 or x + 1 - self.board_size[1] == x1)) or (
                        (x - 1 == x1 or x - 1 + self.board_size[1] == x1) and (
                        x + 1 == x_1 or x + 1 - self.board_size[1] == x_1))) and y == y1 == y_1:
                return self.gor
            elif (((y - 1 == y_1 or y - 1 + self.board_size[0] == y_1) and (
                    y + 1 == y1 or y + 1 - self.board_size[0] == y1)) or (
                          (y - 1 == y1 or y - 1 + self.board_size[0] == y1) and (
                          y + 1 == y_1 or y + 1 - self.board_size[0] == y_1))) and x == x1 == x_1:
                return self.vert
            elif ((x - 1 == x1 or x - 1 + self.board_size[1] == x1) and (
                    y + 1 == y_1 or y + 1 - self.board_size[0] == y_1) and y == y1 and x == x_1) or (
                    (x - 1 == x_1 or x - 1 + self.board_size[1] == x_1) and (
                    y + 1 == y1 or y + 1 - self.board_size[0] == y1) and y == y_1 and x == x1):
                return self.ld
            elif ((x + 1 == x1 or x + 1 - self.board_size[1] == x1) and (
                    y + 1 == y_1 or y + 1 - self.board_size[0] == y_1) and y == y1 and x == x_1) or (
                    (x + 1 == x_1 or x + 1 - self.board_size[1] == x_1) and (
                    y + 1 == y1 or y + 1 - self.board_size[0] == y_1) and y == y_1 and x == x1):
                return self.rd
            elif ((x + 1 == x1 or x + 1 - self.board_size[1] == x1) and (
                    y - 1 == y_1 or y - 1 + self.board_size[0] == y_1) and y == y1 and x == x_1) or (
                    (x + 1 == x_1 or x + 1 - self.board_size[1] == x_1) and (
                    y - 1 == y1 or y - 1 + self.board_size[0] == y1) and y == y_1 and x == x1):
                return self.ru
            elif ((x - 1 == x1 or x - 1 + self.board_size[1] == x1) and (
                    y - 1 == y_1 or y - 1 + self.board_size[0] == y_1) and y == y1 and x == x_1) or (
                    (x - 1 == x_1 or x - 1 + self.board_size[1] == x_1) and (
                    y - 1 == y1 or y - 1 + self.board_size[0] == y1) and y == y_1 and x == x1):
                return self.lu

    def move(self, board, kuda=None):
        if self.dead:
            return
        if kuda == None and self.last_move != None:
            kuda = self.last_move
        if {self.last_move, kuda} in ({'right', 'left'}, {'up', 'down'}):
            kuda = self.last_move
        if kuda:
            x, y = self.mesto[-1]
            if not self.dob:
                del self.mesto[0]

            else:
                self.dob = False
            if kuda == 'up':
                if y - 1 >= 0:
                    y -= 1
                else:
                    y = self.board_size[0] - 1
            elif kuda == 'down':
                if y + 1 < self.board_size[0]:
                    y += 1
                else:
                    y = 0
            elif kuda == 'right':
                if x + 1 < self.board_size[1]:
                    x += 1
                else:
                    x = 0
            elif kuda == 'left':
                if x - 1 >= 0:
                    x -= 1
                else:
                    x = self.board_size[1] - 1
            self.mesto.append((x, y))
            self.last_move = kuda
        yy = self.mesto[-1][1]
        xx = self.mesto[-1][0]
        if board[yy][xx] == 3:
            self.dead = True

        for i in set(self.mesto):
            if self.mesto.count(i) != 1:
                self.dead = True
                break

    def lengthen(self):
        if self.dead:
            return
        self.dob = True


class Board:
    # создание поля
    def __init__(self, map):
        filemap = 'data/' + map + '.txt'
        snakelst = []
        self.board = []
        try:
            with open(filemap, 'r') as mapFile:
                for y, line in enumerate(mapFile):
                    line = list(line.strip())
                    line = [int(i) for i in line]
                    lst = []
                    for x, obj in enumerate(line):
                        if obj != 1:
                            lst.append(obj)
                        else:
                            lst.append(obj)
                            snakelst.append((x, y))
                    self.board.append(lst)

        except Exception:
            print('ОШИБКА! файла с таким названием нет')
            terminate()

        self.height = len(self.board)
        self.width = len(self.board[0])
        self.snake = Snake(snakelst, self.height, self.width)
        self.apple = Apple(self.height, self.width)
        self.apple.generate_new_pos(self.board, self.snake.mesto)
        self.left = 0
        self.top = 0
        self.cell_size = 30
        self.box = load_image('box.png')
        self.sand = load_image('sand.png')
        self.apl_im = load_image('apple.png', colorkey=-1)

    def returnsize(self):
        return (self.width * self.cell_size, self.height * self.cell_size)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] == 0 or self.board[y][x] == 1 or self.board[y][x] == 2:
                    im = self.sand
                    screen.blit(im, (x * self.cell_size + self.left, y * self.cell_size + self.top))
                elif self.board[y][x] == 3:
                    im = self.box
                    screen.blit(im, (x * self.cell_size + self.left, y * self.cell_size + self.top))
                if self.board[y][x] == 2:
                    im = self.apl_im
                    screen.blit(im, (x * self.cell_size + self.left, y * self.cell_size + self.top))
                elif self.board[y][x] == 1:
                    im = self.snake.get_im(x, y)
                    if im != None:
                        screen.blit(im, (x * self.cell_size + self.left, y * self.cell_size + self.top))

                        # pygame.draw.rect(screen, CLR['board'], (
                #     self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size),
                #                  1)

    def help(self, x):
        if x == 1:
            x = 0
        return x

    def update(self, screen, key):
        if key is None:
            self.snake.move(self.board, kuda=None)
        else:
            if key == pygame.K_UP:
                self.snake.move(self.board, kuda='up')
            elif key == pygame.K_DOWN:
                self.snake.move(self.board, kuda='down')
            elif key == pygame.K_RIGHT:
                self.snake.move(self.board, kuda='right')
            elif key == pygame.K_LEFT:
                self.snake.move(self.board, kuda='left')
        if self.snake.dead:
            return 1
        asd = copy.deepcopy(self.board)
        boardd = []
        for y in asd:
            lst = []
            for x in y:
                if x == 1:
                    x = 0
                lst.append(x)
            boardd.append(lst)
        for x, y in self.snake.mesto:
            if (x, y) == self.apple.pos:
                self.snake.lengthen()
                self.apple.generate_new_pos(boardd, self.snake.mesto)
                if HAVESOUND:
                    SOUNDNOM.play()
        for x, y in self.snake.mesto:
            boardd[y][x] = 1
        appos = self.apple.pos
        boardd[appos[1]][appos[0]] = 2

        self.board = copy.deepcopy(boardd)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= y <= self.height - 1 and 0 <= x <= self.width - 1:
            return (y, x)
        else:
            return None


def terminate(*args):
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start(but):
    if game():
        return True


def cont(but):
    global CONT
    CONT = True
    return False


def turnsound(but):
    global HAVESOUND
    if HAVESOUND:
        HAVESOUND = False
        but.change_text('SOUNDS: OFF')
        but.update(pygame.mouse.get_pos())
    else:
        HAVESOUND = True
        but.change_text('SOUNDS: ON')
        but.update(pygame.mouse.get_pos())
    return False


def changelevel(but):
    global LEVEL

    if LEVEL == 4:
        LEVEL = 1
    else:
        LEVEL += 1
    but.change_text(f'LEVEL: {LEVEL}')
    but.update(pygame.mouse.get_pos())
    return False


def changespeed(but):
    global SPEED

    if SPEED == 3:
        SPEED = 1.0
    else:
        SPEED += 0.5
    but.change_text(f'SPEED: {SPEED}')
    but.update(pygame.mouse.get_pos())
    return False


def start_screen():
    global HAVESOUND
    if HAVESOUND:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/start_and pause.mp3')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/start_and pause.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
    size = WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode(size)
    buttons = pygame.sprite.Group()
    intro_but = [[buttons, 200, 50, 50, 100, 'START', CLR['notactive_but'], CLR['active_but'], start],
                 [buttons, 200, 50, 50, 160, 'SOUNDS: ON' if HAVESOUND else 'SOUNDS: OFF', CLR['notactive_but'],
                  CLR['active_but'], turnsound],
                 [buttons, 200, 50, 50, 220, 'SPEED: 1', CLR['notactive_but'], CLR['active_but'], changespeed],
                 [buttons, 200, 50, 50, 280, 'LEVEL: 1', CLR['notactive_but'], CLR['active_but'], changelevel],
                 [buttons, 200, 50, 50, 340, 'EXIT', CLR['notactive_but'], CLR['active_but'], terminate]]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    for but in intro_but:
        Button(but[0], but[1], but[2], but[3], but[4], but[5], but[6], but[7], func=but[8])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                buttons.update(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in buttons.sprites():
                    if i.click(event.pos):
                        return
        if not HAVESOUND:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        buttons.draw(screen)
        clock.tick(60)
        pygame.display.flip()


def resume(but):
    global RESUME
    RESUME = True
    return False


def game():
    global HAVESOUND
    if HAVESOUND:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/game.mp3')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/game.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
    board = Board(str(LEVEL))
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(board.returnsize())
    UPDEV = pygame.USEREVENT + 1
    pygame.time.set_timer(UPDEV, int(400 // SPEED))
    key = None
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    global RESUME
                    RESUME = False
                    if HAVESOUND:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/start_and pause.mp3')
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/start_and pause.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.pause()
                    pygame.mouse.set_visible(True)
                    btnn = pygame.sprite.Group()
                    butns = [[btnn, 200, 50, 0, 100, 'RESUME', CLR['notactive_but'], CLR['active_but'], resume],
                             [btnn, 200, 50, 0, 160, 'SOUNDS: ON' if HAVESOUND else 'SOUNDS: OFF',
                              CLR['notactive_but'], CLR['active_but'], turnsound],
                             [btnn, 200, 50, 0, 220, 'EXIT', CLR['notactive_but'], CLR['active_but'], terminate]]
                    for but in butns:
                        Button(but[0], but[1], but[2], but[3], but[4], but[5], but[6], but[7], func=but[8])
                    sur = pygame.Surface((200, board.returnsize()[1]))
                    sur.fill((0, 0, 0))
                    font = pygame.font.Font(None, 30)
                    score = len(board.snake.mesto) - 3
                    text = f'SCORE: {score}'
                    string = font.render(text, 1, pygame.Color('white'))
                    sur.blit(string, (10, 10))
                    screen.blit(sur, (0, 0))
                    pygame.display.flip()
                    while True:
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT:
                                terminate()
                            elif ev.type == pygame.MOUSEMOTION:
                                btnn.update(ev.pos)
                            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                                for i in btnn.sprites():
                                    i.click(ev.pos)
                            elif ev.type == pygame.KEYDOWN:
                                if ev.key == pygame.K_ESCAPE:
                                    RESUME = True
                        if not HAVESOUND:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        if RESUME:
                            pygame.mouse.set_visible(False)
                            screen.fill((0, 0, 0))
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load('data/game.mp3')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.pause()
                            if HAVESOUND:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                            break
                        btnn.draw(screen)
                        clock.tick(60)
                        pygame.display.flip()

            elif event.type == UPDEV:
                if board.update(screen, key):
                    if HAVESOUND:
                        SOUNDNOUCH.play()
                    if HAVESOUND:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/game_over.mp3')
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/game_over.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.pause()
                    global CONT
                    CONT = False
                    pygame.mouse.set_visible(True)
                    btnn = pygame.sprite.Group()
                    butns = [[btnn, 200, 50, 0, 150, 'NEW GAME', CLR['notactive_but'], CLR['active_but'], cont],
                             [btnn, 200, 50, 0, 210, 'EXIT', CLR['notactive_but'], CLR['active_but'], terminate]]
                    for but in butns:
                        Button(but[0], but[1], but[2], but[3], but[4], but[5], but[6], but[7], func=but[8])
                    sur = pygame.Surface((200, board.returnsize()[1]))
                    sur.fill((0, 0, 0))
                    font = pygame.font.Font(None, 30)
                    score = len(board.snake.mesto) - 3
                    text = 'GAME OVER'
                    text1 = f'SCORE: {score}'
                    string1 = font.render(text1, 1, pygame.Color('white'))
                    string = font.render(text, 1, pygame.Color('white'))
                    sur.blit(string, (10, 10))
                    sur.blit(string1, (10, 50))
                    screen.blit(sur, (0, 0))
                    pygame.display.flip()
                    while True:
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT:
                                terminate()
                            elif ev.type == pygame.MOUSEMOTION:
                                btnn.update(ev.pos)
                            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                                for i in btnn.sprites():
                                    i.click(ev.pos)
                            elif ev.type == pygame.KEYDOWN:
                                if ev.key == pygame.K_ESCAPE:
                                    CONT = True
                        if CONT:
                            screen.fill((0, 0, 0))
                            return True
                        if HAVESOUND:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                        btnn.draw(screen)
                        clock.tick(60)
                        pygame.display.flip()
                screen.fill((0, 0, 0))
        if not HAVESOUND:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


while True:
    LEVEL = 1
    SPEED = 1.0
    RESUME = True
    CONT = True
    start_screen()
