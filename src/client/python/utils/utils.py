import os
import sys
from enum import Enum

import pygame
import win32api
import win32con
import win32gui


class FieldDescription:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines


presets = {
    "Simple": FieldDescription(9, 9, 10),
    "Intermediate": FieldDescription(16, 16, 40),
    "Expert": FieldDescription(30, 16, 99),
}


class SquareContent(Enum):
    MINE = 1,
    EMPTY = 2,

    def describe(self):
        return self.name

    def __repr__(self):
        return self.describe()

    def __str__(self):
        return self.__repr__()


class Flag(Enum):
    QUESTION_FLAG = 0,
    MINE_FLAG = 1,
    NONE_FLAG = 2,


class Square:
    def __init__(self, x, y, content: SquareContent, visible: bool, value: int = None):
        self.x = x
        self.y = y

        self.content = content
        self.value = value

        self.flag = Flag.NONE_FLAG

        self.visible = visible

    def set_flag(self, flag: Flag):
        if not self.visible:
            self.flag = flag

    def can_open(self) -> bool:
        return self.flag == Flag.NONE_FLAG and not self.visible

    def set_content(self, content: SquareContent):
        self.content = content

    def __iter__(self):
        return iter((self.x, self.y))

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Square({self.x}, {self.y}, {self.content.__str__()}, {self.visible})"


class GameState:
    WIN = 0,
    FAIL = 1,
    IDLE = 2


def terminate():
    clock = pygame.time.Clock()

    pygame.mixer.music.load("resources/final_message.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        clock.tick(30)

    pygame.mixer.music.load("resources/ending.mp3")
    pygame.mixer.music.play()

    # Create layered window
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    clock = pygame.time.Clock()
    i = 255
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), round(i), win32con.LWA_ALPHA)
        i = max(0, i - 1.5)
        if i == 0:
            break
        clock.tick(30)
        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def load_image(name, colorkey=None):
    fullname = os.path.join('resources/image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
