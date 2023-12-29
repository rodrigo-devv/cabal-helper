from customtkinter import *
import os
import sys
# Certifique-se de ter instalado esta biblioteca usando 'pip install ruamel.yaml'
import ruamel.yaml

import time
import tkinter
import keyboard
import ctypes
import threading
from threading import Event
from threading import Thread
import pydirectinput as pdi

import source.uTools as uT
import source.actions as Action
import source.dataInfo as data_info

from source.logger import logger
from source.inputs import Inputs as INP
from config import config, attack_observer, CountdownConfig
from source.winh import gWindow, find_all_windows, is_window_foreground

global run
run = False
gameWindow = config.windows
configuration = None
run_event = Event()


def carregar_config():
    # Obtém o diretório do script em execução
    script_dir = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

    # Constrói o caminho para o arquivo config.yaml
    config_path = os.path.join(script_dir, "config.yaml")

    try:
        with open(config_path, "r") as arquivo_config:
            # Cria uma instância de YAML
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
            config = yaml.load(arquivo_config)

            # Certifica-se de que 'warps' seja uma lista
            if 'warps' not in config or not isinstance(config['warps'], list):
                config['warps'] = []

            return config

    except FileNotFoundError:
        # Tratar a exceção se o arquivo config.yaml não for encontrado
        print("Arquivo config.yaml não encontrado.")
        return {'warps': []}


def save_channel(channel):
    global configuration

    if configuration is None:
        configuration = carregar_config()

    # Atualiza a chave 'channel' no dicionário de configuração
    configuration['channel'] = channel

    # Obtém o diretório do script em execução
    script_dir = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

    # Constrói o caminho para o arquivo config.yaml
    config_path = os.path.join(script_dir, "config.yaml")

    try:
        with open(config_path, "w") as arquivo_config:
            # Use o Dumper da ruamel.yaml para preservar os comentários
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
            yaml.dump(configuration, arquivo_config)

    except FileNotFoundError:
        print("Arquivo config.yaml não encontrado.")


def salvar_coordenadas(warps):
    global configuration

    if configuration is None:
        configuration = carregar_config()

    # Limpa as coordenadas antigas
    configuration['warps'] = []

    # Adiciona cada warp como uma lista [x, y]
    for warp in warps:
        configuration['warps'].append([warp[0], warp[1]])

    # Obtém o diretório do script em execução
    script_dir = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

    # Constrói o caminho para o arquivo config.yaml
    config_path = os.path.join(script_dir, "config.yaml")

    try:
        with open(config_path, "w") as arquivo_config:
            # Use o Dumper da ruamel.yaml para preservar os comentários
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
            yaml.dump(configuration, arquivo_config)

    except FileNotFoundError:
        print("Arquivo config.yaml não encontrado.")


def start_process(run_event, direction_var, auto_teleport_var):
    global run

    selected_direction = direction_var.get()
    auto_teleport_enabled = auto_teleport_var.get()

    if run:
        # Botão "Stop" pressionado
        run_event.clear()
        run = False
        start_button.configure(text="Start")
    else:
        # Botão "Start" pressionado
        run_event.set()
        run = True
        start_button.configure(text="Stop")


def find_windows(debug=False):
    try:
        ptWindows = find_all_windows("CABAL")
        if not ptWindows:
            raise Exception("Nenhuma janela do jogo foi encontrada.")

        for i in range(0, len(ptWindows)):
            gameWindow.append(gWindow(ptWindows[i]))
            if debug:
                print("EXE:", gameWindow[i].hwnd, '-', gameWindow[i].winRect())

        if gameWindow[0].w != 1936 or gameWindow[0].h != 1048:
            gameWindow[0].resizeWindow(maximize=True)

    except Exception as e:
        print(f"Erro: {e}")
        break_app(e)


def save_warps():
    while True:
        time.sleep(0.5)
        map_confirm = uT.imgSearch(
            gameWindow[0].rect, data_info.MAP_TEXT_HD, gameWindow[0].rect, threshold=0.95, raw=True)
        if map_confirm:
            search_rect = [
                map_confirm[0] - 185, map_confirm[1] + 75, map_confirm[0] + 170, map_confirm[1] + 420]

            warps_finded = uT.all_positions(
                gameWindow[0].rect, data_info.MAP_CUSTOM_WARP, search_rect, threshold=0.8, raw=True, min_distance_factor=0.1)

            # Adiciona 7 a X e 6 a Y de cada warp
            adjusted_warps = [[warp[0] + 7, warp[1] + 6]
                              for warp in warps_finded]

            logger(('⚡ Warps encontrados: ' + str(len(warps_finded))), color="green")

            if warps_finded:
                salvar_coordenadas(adjusted_warps)
                break
        else:
            INP.sendKey("m")


def teleport(warps_saved, warp_index):
    while True:
        time.sleep(0.05)
        map_confirm = uT.imgSearch(
            gameWindow[0].rect, data_info.MAP_TEXT_HD, gameWindow[0].rect, threshold=0.90, raw=True)
        if map_confirm:
            if warps_saved:
                warp_coord = warps_saved[warp_index]
                while True:
                    INP.click("l", [warp_coord[0], warp_coord[1]], fast=True)
                    time.sleep(0.1)
                    map_confirm = uT.imgSearch(
                        gameWindow[0].rect, data_info.MAP_TEXT_HD, gameWindow[0].rect, threshold=0.90, raw=True)
                    if not map_confirm:
                        break
                break
            else:
                print("Lista de warps vazia.")
        else:
            INP.sendKey("m")


def hunt_gm(warps_saved):
    warp_index = 0  # Índice para rastrear a posição atual na lista de warps

    while True:
        time.sleep(0.1)

        # Verifica se a combinação de teclas Shift+Espaço foi pressionada
        if keyboard.is_pressed('v'):
            teleport(warps_saved, warp_index)

            warp_index += 1
            if warp_index >= len(warps_saved):
                # Se atingir o final da lista, reinicia
                warp_index = 0

            # Adicione o logger aqui


def hunting(direction_value, auto_teleport_enabled, run_event):
    global run
    global configuration

    if configuration is None:
        configuration = carregar_config()

    channel = configuration['channel']

    if direction_value == 1:
        logger("⚠️ Test = Top-bottom selected")
    elif direction_value == 2:
        logger("⚠️ Test = Bottom-top selected")
    elif direction_value == 3:
        logger("⚠️ Test = Random selected")
    else:
        logger("🛑 Bot stopped... Invalid direction value", color="red")
        return

    while run_event.is_set():
        keyboard.wait('r')
        time.sleep(0.1)
        INP.sendKey("o")
        menu_open = uT.imgSearch(gameWindow[0].rect, data_info.MENU_TEXT,
                                 data_info.MENU_AREA_HD, threshold=0.80, raw=True)
        if menu_open:
            INP.click("l", [960, 514])  # SELECIONAR MUDAR CANAL
            while True:
                pixel_channel = uT.pixelSearch(
                    data_info.CHANNEL_LIST_AREA, "#BBFFBB")
                if pixel_channel:
                    for _ in range(7):
                        time.sleep(0.05)
                        war_on = uT.imgSearch(gameWindow[0].rect, data_info.CHANNEL_WAR_TEXT,
                                              data_info.MENU_AREA_HD, threshold=0.80, raw=True)
                        war_red_on = uT.imgSearch(gameWindow[0].rect, data_info.CHANNEL_WAR_TEXT_RED,
                                                  data_info.MENU_AREA_HD, threshold=0.80, raw=True)
                        if war_on or war_red_on:  # Verifica se os canais de guerra estão ativos.
                            # SELECIONAR MUDAR CANAL
                            INP.click("l", [1135 + 8, 667 + 8])
                            time.sleep(0.05)
                            break
                    break
                time.sleep(0.1)

            if direction_value == 1:  # Se Top-bottom
                old_channel = channel

                print("Próximo canal:", str(channel + 1))

                # Verificar o canal selecionado
                if (channel + 1) >= 10 and (channel + 1) <= 17:
                    # Se o canal for maior que 9, aperte em um lugar X
                    INP.click("l", [1135 + 8, 555 + 8])
                elif (channel + 1) >= 18:
                    # Se o canal for maior que 17, aperte em um lugar Y
                    INP.click("l", [1135 + 8, 635 + 8])
                    time.sleep(0.5)
                    INP.click("l", [1135 + 8, 635 + 8])

                # Verificar se o próximo canal é o último canal (25)
                next_channel = (
                    channel + 1) % len(data_info.CHANNEL_COORDINATES)
                if channel == 25:
                    next_channel = 1

                while old_channel == channel:
                    INP.click(
                        "l", data_info.CHANNEL_COORDINATES[channel])
                    INP.click(
                        "l", data_info.CHANNEL_COORDINATES[channel])
                    time.sleep(0.1)
                    channel_menu_confirm = uT.imgSearch(gameWindow[0].rect, data_info.MENU_CANAL_CONFIRM,
                                                        data_info.MENU_AREA_HD, threshold=0.80, raw=True)
                    if channel_menu_confirm:
                        channel_loaded = False
                        while not channel_loaded:
                            # SELECIONAR MUDAR CANAL
                            INP.click("l", [962, 611])
                            time.sleep(0.1)
                            channel_menu_confirm = uT.imgSearch(gameWindow[0].rect, data_info.MENU_CANAL_CONFIRM,
                                                                data_info.MENU_AREA_HD, threshold=0.85, raw=True)
                            if not channel_menu_confirm:
                                while not channel_loaded:
                                    main_gem = uT.imgSearch(gameWindow[0].rect, data_info.LOADING_BAR_FULL,
                                                            data_info.MAIN_LOADING_BAR_HD, threshold=0.80, raw=True)
                                    if main_gem:
                                        save_channel(channel + 1)
                                        channel = next_channel
                                        channel_loaded = True
                                        time.sleep(0.1)
                                        break
                                time.sleep(0.1)

            elif direction_value == 2:  # Se Bottom-top
                old_channel = channel

                print("Próximo canal:", str(channel - 1))

                # Verificar o canal selecionado
                if channel == 0:
                    channel = 25
                if (channel - 1) >= 10 and (channel - 1) <= 17:
                    # Se o canal for maior que 9, aperte em um lugar X
                    INP.click("l", [1135 + 8, 555 + 8])
                elif (channel - 1) >= 18:
                    # Se o canal for maior que 17, aperte em um lugar Y
                    INP.click("l", [1135 + 8, 635 + 8])
                    time.sleep(0.3)
                    INP.click("l", [1135 + 8, 635 + 8])

                # Verificar se o próximo canal é o último canal (1)
                prev_channel = channel - 1 if channel > 1 else 25

                while old_channel == channel:
                    INP.click(
                        "l", data_info.CHANNEL_COORDINATES[prev_channel - 1])
                    INP.click(
                        "l", data_info.CHANNEL_COORDINATES[prev_channel - 1])
                    time.sleep(0.1)
                    channel_menu_confirm = uT.imgSearch(gameWindow[0].rect, data_info.MENU_CANAL_CONFIRM,
                                                        data_info.MENU_AREA_HD, threshold=0.80, raw=True)
                    if channel_menu_confirm:
                        channel_loaded = False
                        while not channel_loaded:
                            # SELECIONAR MUDAR CANAL
                            INP.click("l", [962, 611])
                            time.sleep(0.1)
                            channel_menu_confirm = uT.imgSearch(gameWindow[0].rect, data_info.MENU_CANAL_CONFIRM,
                                                                data_info.MENU_AREA_HD, threshold=0.85, raw=True)
                            if not channel_menu_confirm:
                                while not channel_loaded:
                                    main_gem = uT.imgSearch(gameWindow[0].rect, data_info.LOADING_BAR_FULL,
                                                            data_info.MAIN_LOADING_BAR_HD, threshold=0.80, raw=True)
                                    if main_gem:
                                        save_channel(channel)
                                        exibir_canal()
                                        channel = prev_channel
                                        channel_loaded = True
                                        time.sleep(0.1)
                                        break
                                time.sleep(0.1)
            # Adicione aqui lógica para os outros casos (Random)

    logger("🛑 Bot stopped... Reason: Hunting loop ended", color="red")


class Watchdog:
    def __init__(self, run_event, direction_var, auto_teleport_var):
        self.run_event = run_event
        self.direction_var = direction_var
        self.auto_teleport_var = auto_teleport_var

    def get_direction(self):
        return self.direction_var.get()

    def is_auto_teleport_enabled(self):
        return self.auto_teleport_var.get() == "on"

    def start_watchdog(self):
        logged = False
        while True:
            time.sleep(1)
            if self.run_event.is_set():
                if logged:
                    logged = False
                logger("🚨 Bot: reloging")
            else:
                if not logged:
                    logger("🚨 Bot: idle")
                    logged = True

            while self.run_event.is_set():
                current_direction = self.get_direction()
                auto_teleport_enabled = self.is_auto_teleport_enabled()

                # Use as informações conforme necessário
                print(f"Current Direction: {current_direction}")
                print(f"Auto Teleport Enabled: {auto_teleport_enabled}")

                hunting(current_direction, auto_teleport_enabled, self.run_event)

                if not is_window_foreground(gameWindow[0].hwnd):
                    gameWindow[0].activeWindow()
                time.sleep(0.3)


def exibir_canal():
    # Carrega a configuração
    configuration = carregar_config()

    # Se a configuração existe e o canal está definido, atualiza a label
    if configuration and 'channel' in configuration:
        label_update.configure(text=str(configuration['channel']))
    else:
        # Se não houver configuração ou canal definido, exibe 0
        label_update.configure(text="0")

    # Agende a função para ser chamada novamente após 1000 milissegundos (1 segundo)
    root.after(1000, exibir_canal)


# Cria a janela principal
root = CTk()
root.title("Hunter")

# Configura a janela para ficar sempre no topo
root.attributes("-topmost", 1)

# Desabilita os botões padrão de minimizar, maximizar e fechar
root.overrideredirect(True)

# Obtém a largura da tela
screen_width = root.winfo_screenwidth()

# Define a largura da janela como toda a largura da tela menos 50 pixels
window_width = screen_width - 130

# Define a geometria da janela
root.geometry(f"{window_width}x24+0+0")

# Configura a cor de fundo da janela
root.configure(bg="#222222")

# Cria uma variável para armazenar a direção selecionada
direction = tkinter.IntVar(value=1)

# Cria os Radio buttons para as direções
label_text = CTkLabel(root, text="Canal: ")
label_update = CTkLabel(root, text="0")


label_text.pack(side="left", padx=3)
label_update.pack(side="left", padx=10)
radio_top_down = CTkRadioButton(root, text="Top-bottom", variable=direction,
                                value=1, radiobutton_width=20, radiobutton_height=20, border_width_checked=5)
radio_down_top = CTkRadioButton(root, text="Bottom-top", variable=direction,
                                value=2, radiobutton_width=20, radiobutton_height=20, border_width_checked=5)
radio_random = CTkRadioButton(root, text="Random", variable=direction, value=3,
                              radiobutton_width=20, radiobutton_height=20, border_width_checked=5)
radio_top_down.pack(side="left", padx=5)
radio_down_top.pack(side="left", padx=5)
radio_random.pack(side="left", padx=5)


auto_teleport_var = StringVar(value="on")
auto_tp_checkbox = CTkCheckBox(root, text="Auto teleport",
                               variable=auto_teleport_var, onvalue="on", offvalue="off", checkbox_width=20, checkbox_height=20, corner_radius=5)

auto_tp_checkbox.pack(side="left", padx=5)

""" progressbar = CTkProgressBar(root, orientation="horizontal")
progressbar.pack(side="left", padx=50) """

save_warps = CTkButton(
    root, text="Save Warps", command=save_warps, width=70, height=20, corner_radius=3)

save_warps.pack(side="right", padx=5)

start_button = CTkButton(
    root, text="Start", command=lambda: start_process(run_event, direction, auto_teleport_var), width=70, height=20, corner_radius=3)

start_button.pack(side="right", padx=5)


def pause_app():
    global run
    run = not run
    if run:
        run_event.set()
        start_button.configure(text="Stop")
    else:
        run_event.clear()
        start_button.configure(text="Start")


def break_app(exception=None):
    if exception:
        logger(('🛑 Bot stoped... Reason: ' + str(exception)), color="red")

    else:
        logger('🛑 Shutting down', color="red")
    os._exit(0)


def testes():
    warp_index = 0  # Índice para rastrear a posição atual na lista de warps

    while True:
        time.sleep(0.05)

        # Verifica se a combinação de teclas Shift+Espaço foi pressionada
        if keyboard.is_pressed('shift+space'):
            teleport(warps_saved, warp_index)

            warp_index += 1
            if warp_index >= len(warps_saved):
                # Se atingir o final da lista, reinicia
                warp_index = 0


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl+alt+shift', break_app)
    keyboard.add_hotkey('ctrl+alt+q', pause_app)

    if not ctypes.windll.shell32.IsUserAnAdmin():
        run_as_admin()

    carregar_config()
    exibir_canal()
    warps_saved = carregar_config().get('warps', [])

    find_windows(debug=True)
    watchdog_instance = Watchdog(run_event, direction, auto_teleport_var)
    Thread(target=watchdog_instance.start_watchdog).start()
    Thread(target=hunt_gm, args=(warps_saved,)).start()

    # testes()

    root.mainloop()
