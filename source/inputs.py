import random
import time
import pydirectinput as pdt
from pynput.mouse import Controller
import source.actions as Action
import keyboard

from config import config
from win32 import win32api
from win32.lib import win32con as wcon

window = config.windows


class Inputs:
    @classmethod
    def click(cls, btn, coord, downTime=0.1, debug=False, fast=False):
        xC, yC = coord
        if not btn == "m":
            cls.moveMouse(xC, yC, r=0)

        if btn == "l":
            if debug:
                print("Left click in:", xC, yC)
            win32api.mouse_event(wcon.MOUSEEVENTF_LEFTDOWN, 0, 0)
            time.sleep(downTime)
            win32api.mouse_event(wcon.MOUSEEVENTF_LEFTUP, 0, 0)
        elif btn == "r":
            win32api.mouse_event(wcon.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(downTime)
            win32api.mouse_event(wcon.MOUSEEVENTF_RIGHTUP, 0, 0)
        elif btn == "m":
            win32api.mouse_event(wcon.MOUSEEVENTF_MIDDLEDOWN, 0, 0)
            time.sleep(downTime)
            win32api.mouse_event(wcon.MOUSEEVENTF_MIDDLEUP, 0, 0)
        else:
            raise ValueError(
                "Botão inválido. Use 'l' para esquerdo, 'r' para direito, ou 'm' para o meio.")

        if not fast:
            time.sleep(0.2)

    @classmethod
    def moveMouse(cls, x, y, r=0):
        win32api.SetCursorPos((x + r, y + r))

    @classmethod
    def moveMouseRandom(cls, x, y, r=0):
        left, top, right, bottom = window[0].rect
        realX, realY = left + x, top + y
        win32api.SetCursorPos(
            (cls.addRandomness(realX, r), cls.addRandomness(realY, r)))

    @staticmethod
    def scrollDown(amount: int = 1, interval: float = 0.05) -> None:
        mouse = Controller()
        for _ in range(amount):
            mouse.scroll(0, -1)
            time.sleep(interval)

    @staticmethod
    def sendKey(button: str, times: int = 1, interval: float = 0) -> None:
        # Certifique-se de que a janela está ativa antes de enviar as teclas
        window[0].activeWindow()

        for _ in range(times):
            keyboard.press_and_release(button)
            time.sleep(interval)

    @classmethod
    def mouse_drag(cls, start_coord, end_coord, drag_time, loop_count=1, loop_interval=0.05, debug=False):
        for _ in range(loop_count):
            start_x, start_y = start_coord
            end_x, end_y = end_coord

            win32api.mouse_event(wcon.MOUSEEVENTF_LEFTDOWN, 0, 0)
            cls.moveMouse(start_x, start_y)
            time.sleep(0.05)  # Ajuste conforme necessário
            cls.moveMouse(end_x, end_y)
            time.sleep(drag_time)
            win32api.mouse_event(wcon.MOUSEEVENTF_LEFTUP, 0, 0)

            time.sleep(loop_interval)

    def addRandomness(n, randomn_factor_size=None):
        if randomn_factor_size is None:
            randomness_percentage = 0.1
            randomn_factor_size = randomness_percentage * n

        min_random_factor = -randomn_factor_size
        max_random_factor = randomn_factor_size

        random_factor = random.uniform(min_random_factor, max_random_factor)
        without_average_random_factor = n - randomn_factor_size
        randomized_n = int(without_average_random_factor + random_factor)

        return randomized_n

    @classmethod
    def interpolate(cls, startX, startY, targetX, targetY, t):
        # Gera um valor aleatório para os pontos de controle
        controlX = random.uniform(startX, targetX)
        controlY = random.uniform(startY, targetY)

        # Função de interpolação de curva de Bezier
        x = (1 - t) ** 3 * startX + 3 * (1 - t) ** 2 * t * controlX + \
            3 * (1 - t) * t ** 2 * controlX + t ** 3 * targetX
        y = (1 - t) ** 3 * startY + 3 * (1 - t) ** 2 * t * controlY + \
            3 * (1 - t) * t ** 2 * controlY + t ** 3 * targetY
        return x, y

    @classmethod
    def generateBezierCurve(cls, startX, startY, targetX, targetY, num_points):
        # Gera pontos intermediários ao longo da curva de Bezier
        num_points = max(num_points, 2)
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            point = cls.interpolate(startX, startY, targetX, targetY, t)
            points.append(point)
        return points
