import tkinter as tk
from tkinter import ttk
import keyboard
import pygetwindow as gw
import win32gui
import time


class CoordenadasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Salvador de Coordenadas")

        self.coordenadas = []

        # Encontrar a janela específica pelo título
        self.janela_cabal = gw.getWindowsWithTitle('CABAL')[0]

        self.tree = ttk.Treeview(self.root, columns=("X", "Y"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        self.tree.pack(padx=10, pady=10)

        self.label_monitor = tk.Label(
            self.root, text="Mouse Position (Monitor): X = 0, Y = 0")
        self.label_monitor.pack()

        self.label_cliente = tk.Label(
            self.root, text="Mouse Position (Cliente): X = 0, Y = 0")
        self.label_cliente.pack()

        # Adiciona hotkey
        keyboard.add_hotkey('ctrl+alt+v', self.adicionar_coordenada)

        # Inicia a atualização em tempo real
        self.root.after(100, self.atualizar_coordenadas_em_tempo_real)

    def adicionar_coordenada(self):
        x, y = self.get_cursor_position()
        coordenadas_rel_janela = self.get_relative_to_window_coordinates(x, y)
        self.coordenadas.append(coordenadas_rel_janela)
        item_id = len(self.coordenadas)
        self.tree.insert("", "end", item_id, text=str(
            item_id), values=coordenadas_rel_janela)

    def get_cursor_position(self):
        return (self.root.winfo_pointerx(), self.root.winfo_pointery())

    def get_relative_to_window_coordinates(self, x, y):
        # Obtem o tamanho do cliente da janela usando win32gui
        _, _, width, height = win32gui.GetClientRect(self.janela_cabal._hWnd)

        # Obtem a posição do topo e esquerda da área cliente
        left, top = win32gui.ClientToScreen(self.janela_cabal._hWnd, (0, 0))

        # Calcula as coordenadas relativas ao cliente
        x_rel_janela = x - left
        y_rel_janela = y - top

        return (x_rel_janela, y_rel_janela)

    def atualizar_coordenadas_em_tempo_real(self):
        x, y = self.get_cursor_position()
        self.label_monitor.config(
            text=f"Mouse Position (Monitor): X = {x}, Y = {y}")

        x_rel, y_rel = self.get_relative_to_window_coordinates(x, y)
        self.label_cliente.config(
            text=f"Mouse Position (Cliente): X = {x_rel}, Y = {y_rel}")

        self.root.after(100, self.atualizar_coordenadas_em_tempo_real)


if __name__ == "__main__":
    root = tk.Tk()
    app = CoordenadasApp(root)
    root.mainloop()
