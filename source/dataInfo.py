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
Coordinate = namedtuple('Coordinate', 'x y')

# AREAS
MENU_AREA = Area(456, 255, 556, 314)
TARGET_AREA = Area(351, 34, 395, 70)
MENU_AREA_HD = Area(720, 332, 1179, 704)  # 1920-1080
CHANNEL_WAR_AREA = Area(763, 428, 1150, 490)  # 1920-1080
CHANNEL_LIST_AREA = Area(765, 430, 975, 600)  # 1920-1080
CAPTCHA_AREA = Area(709, 554, 1014, 677)
RELOG_BTNS = Area(760, 675, 1012, 757)
CHARACTER_LOCK_AREA = Area(694, 34, 1013, 234)
MAIN_BOTTOM_RIGHT_BAR = Area(716, 649, 1016, 761)
MAIN_BOTTOM_RIGHT_BAR_HD = Area(1720, 970, 1785, 1020)  # 1920-1080
MAIN_LOADING_BAR_HD = Area(640, 850, 1280, 1000)  # 1920-1080
BAR_HP = Bars(332, 831, 333, 924, 'FF3033')

# KEYS
S_BUFF1 = "f4"
S_BUFF2 = "f5"
S_BUFF3 = "f6"
S_BUFF4 = "f7"
S_BUFF5 = "f8"

# IMAGES
MENU_TEXT = images['option_menu']
MENU_CANAL = images['canal_menu']
TARGET_MOB_NORMAL = images['selected_mob_normal']
MENU_CANAL_CONFIRM = images['canal_menu_confirm']
CHANNEL_WAR_TEXT = images['canal_war']
CHANNEL_WAR_TEXT_RED = images['canal_war_red']
MAP_TEXT = images['map_text']
MAP_TEXT_HD = images['map_text_hd']
MAP_CUSTOM_WARP = images['map_warp']
CAPTCHA_TITLE = images['captchaTitle']
CAPTCHA_BTN = images['captchaOk']
ENTRAR_BTN = images['entrar_btn']
CHARACTER_LOCK = images['character_lock']
MAIN_GEM = images['main_screen_gem']
LOADING_BAR_FULL = images['loading_bar_full']
TELEPORT_ICON = images['teleport_icon']
TESTE = images['teste']

# SUB-SENHA
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


CHANNEL_1_COORD = Coordinate(950, 455)
CHANNEL_2_COORD = Coordinate(950, 480)
CHANNEL_3_COORD = Coordinate(950, 505)
CHANNEL_4_COORD = Coordinate(950, 530)
CHANNEL_5_COORD = Coordinate(950, 555)
CHANNEL_6_COORD = Coordinate(950, 580)
CHANNEL_7_COORD = Coordinate(950, 605)
CHANNEL_8_COORD = Coordinate(950, 630)
CHANNEL_9_COORD = Coordinate(950, 655)
CHANNEL_10_COORD = Coordinate(950, 480)
CHANNEL_11_COORD = Coordinate(950, 505)
CHANNEL_12_COORD = Coordinate(950, 530)
CHANNEL_13_COORD = Coordinate(950, 555)
CHANNEL_14_COORD = Coordinate(950, 580)
CHANNEL_15_COORD = Coordinate(950, 605)
CHANNEL_16_COORD = Coordinate(950, 630)
CHANNEL_17_COORD = Coordinate(950, 655)
CHANNEL_18_COORD = Coordinate(950, 480)
CHANNEL_19_COORD = Coordinate(950, 505)
CHANNEL_20_COORD = Coordinate(950, 530)
CHANNEL_21_COORD = Coordinate(950, 555)
CHANNEL_22_COORD = Coordinate(950, 580)
CHANNEL_23_COORD = Coordinate(950, 605)
CHANNEL_24_COORD = Coordinate(950, 630)
CHANNEL_25_COORD = Coordinate(950, 655)

# CHANNEL COORDINATES
CHANNEL_COORDINATES = [
    Coordinate(960, 455),  # CHANNEL 1
    Coordinate(960, 480),  # CHANNEL 2
    Coordinate(960, 505),  # CHANNEL 3
    Coordinate(960, 530),  # CHANNEL 4
    Coordinate(960, 555),  # CHANNEL 5
    Coordinate(960, 580),  # CHANNEL 6
    Coordinate(960, 605),  # CHANNEL 7
    Coordinate(960, 630),  # CHANNEL 8
    Coordinate(960, 655),  # CHANNEL 9
    Coordinate(960, 480),  # CHANNEL 10
    Coordinate(960, 505),  # CHANNEL 11
    Coordinate(960, 530),  # CHANNEL 12
    Coordinate(960, 555),  # CHANNEL 13
    Coordinate(960, 580),  # CHANNEL 14
    Coordinate(960, 605),  # CHANNEL 15
    Coordinate(960, 630),  # CHANNEL 16
    Coordinate(960, 655),  # CHANNEL 17
    Coordinate(960, 480),  # CHANNEL 18
    Coordinate(960, 505),  # CHANNEL 19
    Coordinate(960, 530),  # CHANNEL 20
    Coordinate(960, 555),  # CHANNEL 21
    Coordinate(960, 580),  # CHANNEL 22
    Coordinate(960, 605),  # CHANNEL 23
    Coordinate(960, 630),  # CHANNEL 24
    Coordinate(960, 655),  # CHANNEL 25
]
