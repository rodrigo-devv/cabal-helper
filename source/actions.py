import time
import random
from config import config
from source.inputs import Inputs as INP
import source.uTools as uT
import pydirectinput as pdi
import source.dataInfo as dataInformation

window = config.windows


def openMenu(option):
    menu_actions = {
        "inventory": open_inventory,
        "info": open_info,
        "skills": open_skills
    }

    action_function = menu_actions.get(option)
    if action_function:
        return action_function()


def open_inventory():
    resultImg = uT.imgSearch(
        window[0].rect, dataInformation.ABA_INVENTORY, dataInformation.A_ABAS)
    if resultImg is not None:
        return True

    for _ in range(30):  # Tenta 5 vezes abrir
        INP.sendKey('v')
        time.sleep(0.1)  # Aguarda 1 segundo para a abertura do inventário
        resultImg = uT.imgSearch(
            window[0].rect, dataInformation.ABA_INVENTORY, dataInformation.A_ABAS)
        if resultImg is not None:
            return True
    return False


def open_info():
    resultImg = uT.imgSearch(
        window[0].rect, dataInformation.ABA_CHARACTER, dataInformation.A_ABAS)
    if resultImg is not None:
        return True

    for _ in range(30):  # Tenta 5 vezes abrir a aba
        window[0].key('c')
        time.sleep(0.1)  # Aguarda 1 segundo para a abertura do inventário
        resultImg = uT.imgSearch(
            window[0].rect, dataInformation.ABA_CHARACTER, dataInformation.A_ABAS)
        if resultImg is not None:
            return True


def open_skills():
    resultImg = uT.imgSearch(
        window[0].rect, dataInformation.ABA_SKILLS, dataInformation.A_ABAS)
    if resultImg is not None:
        return True

    for _ in range(30):  # Tenta 5 vezes abrir a aba
        window[0].key('s')
        time.sleep(0.1)  # Aguarda 1 segundo para a abertura do inventário
        resultImg = uT.imgSearch(
            window[0].rect, dataInformation.ABA_SKILLS, dataInformation.A_ABAS)
        if resultImg is not None:
            return True


def rdnClicks(window):
    mX, mY = int(window.w / 2), int(window.h / 2)
    rndResult = random.randint(1, 4)

    if rndResult == 1:
        cX1 = int(mX / 2)
        cX2 = cX1 * 3
        return cX1, mY, cX2, mY

    if rndResult == 2:
        cY1 = int(mY / 3)
        cY2 = cY1 * 5
        return mX, cY1, mX, cY2

    if rndResult == 3:
        cX1 = int(mX / 2)
        cY1 = int(mY / 2)
        cX2 = cX1 * 3
        cY2 = cY1 * 3
        return cX1, cY1, cX2, cY2

    if rndResult == 4:
        cX1 = mX * 3 / 2
        cY1 = mY / 2
        cX2 = mX / 2
        cY2 = mY * 3 / 2
        return cX1, cY1, cX2, cY2
