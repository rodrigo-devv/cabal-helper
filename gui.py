import tkinter as tk
from tkinter import ttk
import threading
import time
from tkinter import messagebox


class CronometroGUI:
    def __init__(self, root, pause_app_func):
        self.root = root
        self.root.title("Cronômetro")

        self.pause_app_func = pause_app_func

        self.label_tempo = ttk.Label(self.root, text="Tempo: 0 segundos")
        self.label_tempo.pack(pady=10)

        self.botao_pause_app = ttk.Button(
            self.root, text="Relogar", command=self.pause_app)
        self.botao_pause_app.pack(pady=10)

    def pause_app(self):
        self.pause_app_func()

    def reset_cronometro(self):
        self.reset_cronometro_func()


def start_gui(pause_app_func):
    root = tk.Tk()
    app = CronometroGUI(root, pause_app_func)
    root.mainloop()
