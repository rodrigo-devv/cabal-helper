import os
import ctypes
import sys
from time import sleep
import yaml
import keyboard
import platform
import threading
import datetime
from customtkinter import *
from interface import run_gui

import pydirectinput as pdi

import source.uTools as uT
import source.actions as Action
import source.dataInfo as data_info

from source.logger import logger
from source.inputs import Inputs as INP
from config import config, attack_observer, CountdownConfig
from source.winh import gWindow, find_all_windows, is_window_foreground


global run, must_relog
run = False
must_relog = False
gameWindow = config.windows
configuration = None
countdown_instance = None


def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except ctypes.WinError as e:
        # Se o usuário cancelar a solicitação de privilégios de administrador,
        # a exceção ERROR_CANCELLED será levantada. Você pode lidar com isso conforme necessário.
        print(f"Erro: {e}")


def carregar_config():
    global configuration
    global countdown_instance

    # Obtém o diretório do script em execução
    script_dir = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

    # Constrói o caminho para o arquivo config.yaml
    config_path = os.path.join(script_dir, "config.yaml")

    try:
        with open(config_path, "r") as arquivo_config:
            configuration = yaml.safe_load(arquivo_config)

            # Verifica se a seção "countdown" está presente no config.yaml
            if "countdown" in configuration:
                countdown_config = configuration["countdown"]
                hours = countdown_config.get("hours", 0)
                minutes = countdown_config.get("minutes", 0)
                seconds = countdown_config.get("seconds", 0)

                # Inicializa a instância do Countdown
                countdown_instance = Countdown(
                    hours, minutes, seconds, on_zero_callback)
    except FileNotFoundError:
        # Tratar a exceção se o arquivo config.yaml não for encontrado
        print("Arquivo config.yaml não encontrado.")

        configuration = None


class Countdown:
    def __init__(self, h, m, s, on_zero_callback):
        self.total_seconds = h * 3600 + m * 60 + s
        self.on_zero_callback = on_zero_callback
        self.run_countdown = True
        self.countdown_thread = threading.Thread(target=self._start_countdown)
        self.countdown_thread.start()

        # Atualiza o CountdownConfig com os valores iniciais
        self.update_config()

    def _start_countdown(self):
        while self.run_countdown and self.total_seconds > 0:
            timer = datetime.timedelta(seconds=self.total_seconds)
            print(">", timer, " ⏱️", end="\r")
            sleep(1)
            self.total_seconds -= 1

        if self.total_seconds <= 0:
            self.on_zero_callback()

    def restart_countdown(self, h, m, s):
        self.total_seconds = h * 3600 + m * 60 + s
        self.run_countdown = True
        self.countdown_thread = threading.Thread(target=self._start_countdown)
        self.countdown_thread.start()

        # Atualiza o CountdownConfig ao reiniciar o Countdown
        self.update_config()

    def stop_countdown(self):
        self.run_countdown = False

    def get_time_str(self):
        timer = datetime.timedelta(seconds=self.total_seconds)
        return str(timer).split(".")[0]  # Remove os milissegundos

    def update_config(self):
        # Atualiza os valores no CountdownConfig do config.py
        CountdownConfig.set_countdown(
            self.total_seconds // 3600, (self.total_seconds % 3600) // 60, self.total_seconds % 60)


def on_zero_callback():
    global must_relog
    must_relog = True


def find_windows(debug=False):
    try:
        ptWindows = find_all_windows("CABAL")
        if not ptWindows:
            raise Exception("Nenhuma janela do jogo foi encontrada.")

        for i in range(0, len(ptWindows)):
            gameWindow.append(gWindow(ptWindows[i]))
            if debug:
                print("EXE:", gameWindow[i].hwnd, '-', gameWindow[i].winRect())

        if gameWindow[0].w != 1024 or gameWindow[0].h != 768 or gameWindow[0].rect[0] != 0 or gameWindow[0].rect[1] != 0:
            gameWindow[0].resizeWindow()

    except Exception as e:
        print(f"Erro: {e}")
        break_app(e)


def watchdog():
    logged = False
    while True:
        sleep(1)
        if must_relog:
            if logged:
                logged = False
            logger("🚨 Bot: reloging")
        else:
            if not logged:
                logger("🚨 Bot: idle")
                logged = True

        while run:
            game_info = gameWindow[0].win_info()
            if game_info[0] or game_info[1]:
                gameWindow[0].resizeWindow()
            if is_window_foreground(gameWindow[0].hwnd) != True:
                gameWindow[0].activeWindow()
            sleep(0.3)
            if must_relog:
                relog()


def toggle_attack():
    if run:
        config.attack = not config.attack
        config.resumeAttack = not config.resumeAttack
    else:
        if config.attack:
            logger("⚔️ Ataque pausado")
        print("🚨 Watchdog está pausado. Ative antes de atacar.")


def pause_app():
    global run
    run = not run  # Alternar o valor de 'run' entre True e False


def break_app(exception=None):
    if exception:
        logger(('🛑 Bot stoped... Reason: ' + str(exception)), color="red")

    else:
        logger('🛑 Stopping bot', color="red")
    os._exit(0)


def relog():
    global run, must_relog, countdown_instance
    aero_bot = False
    relogado = False
    while not relogado:
        sleep(0.5)
        INP.sendKey("o")
        sleep(1)
        menu_open = uT.imgSearch(gameWindow[0].rect, data_info.MENU_TEXT,
                                 data_info.MENU_AREA, threshold=0.80, raw=True)
        if menu_open:
            INP.click("l", [514, 360])  # SELECIONAR SERVIDOR
            sleep(0.5)
            INP.click("l", [530, 473])

            while not relogado:
                sleep(0.1)
                entrar_btn = uT.imgSearch(gameWindow[0].rect, data_info.ENTRAR_BTN,
                                          data_info.RELOG_BTNS, threshold=0.95, raw=True)
                if entrar_btn:
                    INP.click("l", [946, 727])  # CLICA NO BTN ENTRAR

                    while not relogado:
                        sleep(0.1)
                        character_screen = uT.imgSearch(gameWindow[0].rect, data_info.CHARACTER_LOCK,
                                                        data_info.CHARACTER_LOCK_AREA, threshold=0.93, raw=True)
                        if character_screen:
                            INP.click("l", [946, 727])  # CLICA COMECAR
                            sleep(1)
                            if not sub_handle():
                                return False

                            while not relogado:
                                sleep(0.1)
                                login_confirm = uT.imgSearch(gameWindow[0].rect, data_info.MAIN_GEM,
                                                             data_info.MAIN_BOTTOM_RIGHT_BAR, threshold=0.95, raw=True)
                                INP.scrollDown(amount=12)
                                if login_confirm:
                                    # CLICA NA ABA 2
                                    if aero_bot:
                                        INP.click("l", [339, 666])
                                        INP.sendKey("f4")

                                    while not relogado:
                                        sleep(0.5)
                                        INP.sendKey("m")
                                        sleep(0.5)
                                        map_confirm = uT.imgSearch(gameWindow[0].rect, data_info.MAP_TEXT,
                                                                   gameWindow[0].rect, threshold=0.95, raw=True)
                                        if map_confirm:
                                            search_rect = [
                                                map_confirm[0] - 130, map_confirm[1] + 124, map_confirm[0] + 112, map_confirm[1] + 215]
                                            while not relogado:
                                                sleep(0.1)
                                                teleport_find = uT.imgSearch(gameWindow[0].rect, data_info.TELEPORT_ICON,
                                                                             search_rect, threshold=0.95, raw=True)
                                                if teleport_find:
                                                    INP.click(
                                                        "l", [teleport_find[0], teleport_find[1]])
                                                    relogado = True
                                                    break
    sleep(2)
    if aero_bot:
        INP.mouse_drag([200, 545], [150, 455], 0.2, 25)
        INP.sendKey("z")
        sleep(0.2)
        INP.sendKey("f1")
    else:
        routes("seni-procy-premium")
    # Verifica se há uma instância de Countdown e se a configuração está carregada
    if countdown_instance and configuration and "countdown" in configuration:
        countdown_config = configuration["countdown"]
        hours = countdown_config.get("hours", 1)
        minutes = countdown_config.get("minutes", 0)
        seconds = countdown_config.get("seconds", 0)

        # Cria uma nova instância de Countdown com os valores do arquivo de configuração
        countdown_instance.restart_countdown(hours, minutes, seconds)
    else:
        # Caso a configuração não esteja disponível, use os valores padrão
        countdown_instance = Countdown(1, 0, 0, on_zero_callback)
    logger("🤓 Relogado")
    must_relog = False
    return True


def sub_handle(sub=None):
    global configuration
    window = gameWindow[0].rect
    # Verifica se a janela da sub-senha esta aberta
    sub_window = uT.imgSearch(
        window, data_info.SUB_TEXT, data_info.SUB_PAD_AREA, threshold=0.90, raw=True)

    if sub_window:
        sleep(0.3)
        logger("🔑 Inserindo sub-senha")

        sub_done = False

        if sub is None:
            if configuration and "user_sub" in configuration:
                sub = configuration["user_sub"]
            else:
                print("Senha não encontrada no arquivo de configuração.")
                return False

        # Verifica se ja existe algum numero digitado. caso tenha, sera apagado.
        sub_digited = uT.imgSearch(
            window, data_info.SUB_FILL, data_info.SUB_PAD_AREA, threshold=0.95, raw=True)
        if sub_digited:
            fail_safe = 0
            while True:
                sleep(0.1)
                INP.click("l", [628, 447])
                check_sub_input = uT.imgSearch(
                    window, data_info.SUB_FILL, data_info.SUB_PAD_AREA, threshold=0.95, raw=True)
                if not check_sub_input:
                    break
                fail_safe += 1
                if fail_safe >= 100:
                    break
        for digito_str in sub:
            numero_atual = data_info.BUTTONS.get(digito_str, None)

            if numero_atual is not None:
                try:
                    number_found = uT.imgSearch(
                        window, numero_atual, data_info.SUB_PAD_AREA, threshold=0.90, raw=True)

                    if number_found and number_found[0]:
                        INP.click("l", [number_found[0], number_found[1]])
                        sleep(0.3)
                    else:
                        print(f"Número {digito_str} não encontrado.")
                except Exception as e:
                    print(f"Erro ao buscar o número {digito_str}: {e}")
            else:
                print(
                    f"Imagem do botão {digito_str} não encontrada na estrutura de dados.")
    else:
        return True

    while not sub_done:
        sub_window = uT.imgSearch(
            window, data_info.SUB_TEXT, data_info.SUB_PAD_AREA, threshold=0.95, raw=True)

        if sub_window:
            sub_digited = uT.imgSearch(
                window, data_info.SUB_FILL, data_info.SUB_PAD_AREA, threshold=0.95, raw=True)
            if sub_digited:
                INP.click("l", [455, 505])
                sleep(1)
                while not sub_done:
                    sub_window = uT.imgSearch(
                        window, data_info.SUB_TEXT, data_info.SUB_PAD_AREA, threshold=0.95, raw=True)

                    if sub_window:
                        sub_digited = uT.imgSearch(
                            window, data_info.SUB_FILL, data_info.SUB_PAD_AREA, threshold=0.95, raw=True)

                        if not sub_digited:
                            logger(
                                "🟥 Senha incorreta, ou digitada incorretamente. Parando BOT")
                            pause_app()
                            return False
                        break
                    else:
                        sub_done = True
                        logger("🚨 Sub-senha digitada com sucesso.")
                        return True
                        break


def routes(route):
    if route == "seni-procy-premium":
        INP.moveMouse(35, 676)
        sleep(0.2)
        INP.sendKey("1", interval=0.75)
        INP.sendKey("2", interval=0.55)
        INP.sendKey("1", interval=0.75)
        INP.sendKey("2", interval=0.55)
        INP.moveMouse(203, 552)
        sleep(0.2)
        INP.sendKey("1", interval=0.75)
        return


def hunt():
    target_on = False
    while True:
        sleep(0.2)
        while config.attack and not must_relog:
            target = uT.imgSearch(gameWindow[0].rect, data_info.TARGET_MOB_NORMAL,
                                  data_info.TARGET_AREA, threshold=0.80, raw=True)
            target_color = uT.pixelColor([387, 51])

            if target:
                target_on = True
                while target_on:
                    INP.sendKey("alt")
                    # Search in target health bar
                    color = uT.pixelColor([386, 51])
                    if color == "0x1E1E1E":  # Target without health
                        INP.sendKey("z")
                    INP.sendKey("3")
                    sleep(0.05)
                    INP.sendKey("4")
                    sleep(0.05)
                    INP.sendKey("5")
                    sleep(0.05)
                    INP.sendKey("6")
                    sleep(0.05)
                    INP.sendKey("space")
                    target = uT.imgSearch(gameWindow[0].rect, data_info.TARGET_MOB_NORMAL,
                                          data_info.TARGET_AREA, threshold=0.80, raw=True)
                    if not target:
                        target_on = False
                        break
                    sleep(0.1)
            elif target_color == "E22222":
                print("Player Selected")
                # TODO
            else:
                INP.click("m", [0, 0])
                sleep(0.1)
                print("Hunting")
            sleep(0.05)


def testes():
    logger("💻 Test acionado")
    sleep(1)
    INP.scrollDown(amount=12)
    routes("seni-procy-premium")


if __name__ == '__main__':
    keyboard.add_hotkey('f10', toggle_attack)
    keyboard.add_hotkey('f12', pause_app)
    keyboard.add_hotkey('ctrl+alt+shift', break_app)

    if not ctypes.windll.shell32.IsUserAnAdmin():
        run_as_admin()

    find_windows()
    carregar_config()

    # gui_thread = threading.Thread(target=run_gui)
    # gui_thread.start()

    threading.Thread(target=watchdog, args=()).start()
    threading.Thread(target=hunt, args=()).start()
    # testes()

    run = True
