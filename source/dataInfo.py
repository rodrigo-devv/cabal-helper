from collections import namedtuple
from os import listdir
import cv2 as cv
import sys
import os


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def load_images(dir_path='images'):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Use o diretório temporário do executável PyInstaller
        images_dir = os.path.join(sys._MEIPASS, dir_path)
    else:
        # Caso contrário, use o diretório do script atual
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        images_dir = os.path.join(script_dir, dir_path)

    file_names = listdir(images_dir)
    targets = {}
    for file in file_names:
        path = os.path.join(images_dir, file)
        targets[remove_suffix(file, '.png')] = cv.imread(path)

    return targets


images = load_images()
Pixel = namedtuple('Pixel', 'x y')
Path = namedtuple('Path', 'OFFSET NAME')
ColorPixel = namedtuple('ColorPixel', Pixel._fields + ('color',))
Area = namedtuple('Area', 'left top right bottom')
Bars = namedtuple('Bars', 'x1 y1 x2 y2 color')

# AREAS
MENU_AREA = Area(456, 255, 556, 314)
CAPTCHA_AREA = Area(709, 554, 1014, 677)
RELOG_BTNS = Area(760, 675, 1012, 757)
CHARACTER_LOCK_AREA = Area(694, 34, 1013, 234)
MAIN_BOTTOM_RIGHT_BAR = Area(716, 649, 1016, 761)
BAR_HP = Bars(332, 831, 333, 924, 'FF3033')

# KEYS
S_BUFF1 = "f4"
S_BUFF2 = "f5"
S_BUFF3 = "f6"
S_BUFF4 = "f7"
S_BUFF5 = "f8"

# IMAGES
MENU_TEXT = images['option_menu']
MAP_TEXT = images['map_text']
CAPTCHA_TITLE = images['captchaTitle']
CAPTCHA_BTN = images['captchaOk']
ENTRAR_BTN = images['entrar_btn']
CHARACTER_LOCK = images['character_lock']
MAIN_GEM = images['main_screen_gem']
TELEPORT_ICON = images['teleport_icon']
TESTE = images['teste']

# SUB-SENHA
WRONG_AREA = Area(177, 51, 993, 161)
SUB_PAD_AREA = Area(304, 220, 707, 567)

# SUB IMAGES
SUB_FILL = images['sub_filled']
SUB_TEXT = images['sub_senha_text']

BUTTON_0 = images['sub_0_btn']
BUTTON_1 = images['sub_1_btn']
BUTTON_2 = images['sub_2_btn']
BUTTON_3 = images['sub_3_btn']
BUTTON_4 = images['sub_4_btn']
BUTTON_5 = images['sub_5_btn']
BUTTON_6 = images['sub_6_btn']
BUTTON_7 = images['sub_7_btn']
BUTTON_8 = images['sub_8_btn']
BUTTON_9 = images['sub_9_btn']

BUTTONS = {
    "0": BUTTON_0,
    "1": BUTTON_1,
    "2": BUTTON_2,
    "3": BUTTON_3,
    "4": BUTTON_4,
    "5": BUTTON_5,
    "6": BUTTON_6,
    "7": BUTTON_7,
    "8": BUTTON_8,
    "9": BUTTON_9,
}

# PINPOINT
PIXEL_POINT_EXAMPLE = Pixel(516, 908)  # 0F0F0F Red color #FF3033

EXAMPLE1 = Pixel(1492, 779)
EXAMPLE2 = Pixel(1492, 864)
EXAMPLE3 = Pixel(1573, 864)
EXAMPLE4 = Pixel(1573, 779)

MAP_PIXELS_LIBRARY = [
    EXAMPLE1,
    EXAMPLE2,
    EXAMPLE3,
    EXAMPLE4
]
