from win32 import win32gui
import win32con
import pydirectinput as pdt
import time
from typing import Dict, Tuple
import numpy as np


class gWindow:
    hwnd = 0

    def __init__(self, o_hwnd, debug=False):
        self.hwnd = o_hwnd
        self.w = 0
        self.h = 0
        self.rect = []
        self.tlrb = []

    @staticmethod
    def init(self, debug: bool = False):
        window_name = "CABAL"

    def activeWindow(self):
        if win32gui.GetForegroundWindow() != self.hwnd:
            pdt.keyDown('alt')
            pdt.keyUp('alt')
            win32gui.BringWindowToTop(self.hwnd)
            if win32gui.IsIconic(self.hwnd):  # Verifica se a janela está minimizada
                # Restaura a janela se estiver minimizada
                win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.hwnd)
        else:
            return True

    def winRect(self):
        self.activeWindow()
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.rect = (left, top, right, bottom)
        self.w = right - left
        self.h = bottom - top
        self.tlrb = top, left, right, bottom
        return self.rect

    def win_info(self):
        return win32gui.GetWindowRect(self.hwnd)

    def resizeWindow(self, width=1024, height=768, x=0, y=0):
        self.activeWindow()
        win32gui.MoveWindow(self.hwnd, x, y, width, height, True)
        self.winRect()


def find_all_windows(name):
    result = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
            result.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)
    return result


def is_window_foreground(hwnd):
    foreground_hwnd = win32gui.GetForegroundWindow()
    return hwnd == foreground_hwnd
