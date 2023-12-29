import numpy as np
import cv2
import mss
from config import config
from win32 import win32gui

window = config.windows


def hex_to_bgr(hex_color):
    # Converte a cor hexadecimal para formato BGR
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (4, 2, 0))


def show(rectangles, scanArea=None, img=None, debug=False):
    if rectangles is None:
        return False
    if img is None:
        with mss.mss() as sct:
            if scanArea is None:
                monitor = sct.monitors[1]
            else:
                left, top, right, bottom = scanArea
                width, height = [right - left, bottom - top]
                if debug:
                    monitor = {"top": top, "left": left,
                               "width": width, "height": height}
                else:
                    monitor = sct.monitors[1]
            img = np.array(sct.grab(monitor))
    if len(rectangles) > 1:
        for (x, y, w, h) in rectangles:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255, 255), 2)
    else:
        for (x, y, w, h) in rectangles:
            cv2.rectangle(img, (x, y), (x + 30, y + 30),
                          (255, 255, 255, 255), 2)
    cv2.imshow('debug', img)
    cv2.waitKey(0)


def printSreen(scanArea=None):
    with mss.mss() as sct:
        # The screen part to capture
        if scanArea is not None:
            left, top, right, bottom = scanArea
            width, height = [right - left, bottom - top]
            monitor = {"top": top, "left": left,
                       "width": width, "height": height}
        else:
            monitor = sct.monitors[1]
        sct_img = np.array(sct.grab(monitor))
        # Grab the data
        return sct_img[:, :, :3]


def imgSearch(window, target, rect, threshold=0.8, img=None, raw=False):
    window_left, window_top, window_right, window_bottom = window

    if raw:
        rect_left, rect_top, rect_right, rect_bottom = rect
        if rect_left < window_left or rect_right > window_right or rect_top < window_top or rect_bottom > window_bottom:
            return None
        scanArea = rect
    else:
        scanArea = [(window[0] + rect[0]), (window[1] + rect[1]) -
                    23, (window[0] + rect[2]), (window[1] + rect[3]) - 23]

    if img is None:
        img = printSreen(scanArea)
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal >= threshold:
        w = target.shape[1]
        h = target.shape[0]
        topLeft = maxLoc
        centerX = int(topLeft[0] + w / 2) + rect[0]
        centerY = int(topLeft[1] + h / 2) + rect[1]
        return [centerX, centerY]
    return None


def all_positions(window, target, rect=None, img=None, threshold=0.9, raw=False, min_distance_factor=1.0):
    window_left, window_top, window_right, window_bottom = window
    if raw:
        rect_left, rect_top, rect_right, rect_bottom = rect
        if rect_left < window_left or rect_right > window_right or rect_top < window_top or rect_bottom > window_bottom:
            return None
        scanArea = rect
    else:
        scanArea = [(window[0] + rect[0]), (window[1] + rect[1]) -
                    23, (window[0] + rect[2]), (window[1] + rect[3]) - 23]
    if img is None:
        img = printSreen(scanArea)
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)

    h, w = target.shape[:2]
    min_distance = int(min_distance_factor * max(h, w))

    yloc, xloc = np.where(result >= threshold)  # type: ignore

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        new_rect = [int(x) + rect[0] + 8, int(y) + rect[1] + 8, w, h]
        rectangles.append(new_rect)

    # Agrupa retângulos semelhantes
    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)

    return rectangles.tolist()


def positions(window, target, rect=None, img=None, threshold=0.9, raw=False):
    if raw:
        rect_left, rect_top, rect_right, rect_bottom = rect
        if rect_left < window_left or rect_right > window_right or rect_top < window_top or rect_bottom > window_bottom:
            return None
        scanArea = rect
    else:
        scanArea = [(window[0] + rect[0]), (window[1] + rect[1]) -
                    23, (window[0] + rect[2]), (window[1] + rect[3]) - 23]
    if img is None:
        img = printSreen(scanArea)
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)  # type: ignore

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x) + rect[0], int(y) +
                          rect[1] - 23, int(w), int(h)])
        rectangles.append([int(x) + rect[0], int(y) +
                          rect[1] - 23, int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def pixelColor(coord, debug=False):
    hwnd = window[0].hwnd
    dc = win32gui.GetWindowDC(hwnd)
    rgba = win32gui.GetPixel(dc, coord[0], coord[1])
    win32gui.ReleaseDC(hwnd, dc)
    r, g, b = rgba & 0xff, rgba >> 8 & 0xff, rgba >> 16 & 0xff
    hexColor = '%02x%02x%02x'.upper() % (r, g, b)
    if debug:
        print('Search result :', hexColor)
        print((r, g, b))

    return hexColor


def pixelSearch(area, target_color_hex, threshold=100, img=None):
    area_left, area_top, area_right, area_bottom = area
    if img is None:
        img = printSreen(area)
    else:
        img = np.array(img)

    # Converte a cor-alvo hexadecimal para formato BGR
    target_color = hex_to_bgr(target_color_hex)

    # Cria uma máscara para pixels dentro da faixa de tolerância
    lower_bound = np.array(target_color) - threshold
    upper_bound = np.array(target_color) + threshold
    mask = cv2.inRange(img, lower_bound, upper_bound)

    # Encontra os índices dos pixels correspondentes à cor-alvo
    indices = np.where(mask > 0)

    # Se houver pelo menos um pixel correspondente
    if len(indices[0]) > 0:
        # Calcula a média dos índices para obter a posição média
        avg_x = int(np.mean(indices[1])) + area_left
        avg_y = int(np.mean(indices[0])) + area_top
        return [avg_x, avg_y]

    return None
