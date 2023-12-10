from config import CountdownConfig
from customtkinter import *
import ruamel.yaml
import threading
import datetime

set_appearance_mode("dark")
set_default_color_theme("dark-blue")


class GuiApp:
    def __init__(self, master):
        self.master = master
        self.setup_ui()
        self.start_timer_thread()  # Inicia a thread do cronômetro

    def setup_ui(self):
        frame = CTkFrame(master=self.master)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        relog_label = CTkLabel(master=frame, text="Relogando em :")
        relog_label.pack(side="left", pady=5, padx=10)

        self.timer_label = CTkLabel(master=frame, text="00:00:00")
        self.timer_label.pack(side="left", pady=5)

        time_frame = CTkFrame(master=self.master)
        time_frame.pack(side="bottom", pady=10, padx=20,
                        fill="both", expand=True)

        title_label = CTkLabel(master=time_frame, text="Configurações")
        title_label.pack(pady=4, padx=5)

        hour_frame = CTkFrame(master=time_frame)
        minute_frame = CTkFrame(master=time_frame)
        sub_frame = CTkFrame(master=time_frame)

        hour_label = CTkLabel(master=hour_frame, text="Horas")
        self.hour_entry = CTkEntry(master=hour_frame, placeholder_text="Horas")

        minute_label = CTkLabel(master=minute_frame, text="Minutos")
        self.minute_entry = CTkEntry(
            master=minute_frame, placeholder_text="Minutos")

        sub_label = CTkLabel(master=sub_frame, text="Sub-senha")
        self.sub_entry = CTkEntry(
            master=sub_frame, placeholder_text="Sub-senha", show="*")

        button = CTkButton(master=time_frame, text="Save",
                           command=self.save_config)
        button.pack(side="bottom", fill="x", pady=8, padx=10)

        # FRAMES
        hour_frame.pack(side="left", padx=10)
        minute_frame.pack(side="left", padx=5)
        sub_frame.pack(side="left", padx=10)

        # LABELS
        hour_label.pack(pady=2, padx=5)
        minute_label.pack(pady=2, padx=5)
        sub_label.pack(pady=2, padx=5)

        # ENTRYS
        self.hour_entry.pack(side="left", pady=5, padx=5, expand=True)
        self.minute_entry.pack(side="left", pady=5, padx=5, expand=True)
        self.sub_entry.pack(side="left", pady=5, padx=5, expand=True)

        self.load_config()

    def save_config(self):
        config_file_path = "config.yaml"

        try:
            with open(config_file_path, "r") as config_file:
                yaml = ruamel.yaml.YAML(typ='rt')  # Use round-trip loader
                config_data = yaml.load(config_file)
        except FileNotFoundError:
            config_data = {}

        # Modificar somente as linhas necessárias
        config_data["countdown"] = config_data.get("countdown", {})
        config_data["countdown"]["hours"] = int(self.hour_entry.get())
        config_data["countdown"]["minutes"] = int(self.minute_entry.get())
        config_data["user_sub"] = self.sub_entry.get()

        with open(config_file_path, "w") as config_file:
            yaml = ruamel.yaml.YAML(typ='rt')  # Use round-trip dumper
            yaml.dump(config_data, config_file)

        # Atualiza o CountdownConfig ao salvar a configuração
        CountdownConfig.set_countdown(
            int(self.hour_entry.get()), int(self.minute_entry.get()), 0)

    def load_config(self):
        config_file_path = "config.yaml"

        try:
            with open(config_file_path, "r") as config_file:
                yaml = ruamel.yaml.YAML(typ='rt')  # Use round-trip loader
                config_data = yaml.load(config_file)

                # Preencher os campos de entrada com os dados do arquivo config.yaml
                hour_value = config_data.get("countdown", {}).get("hours", "")
                minute_value = config_data.get(
                    "countdown", {}).get("minutes", "")
                sub_value = config_data.get("user_sub", "")

                self.hour_entry.delete(0, "end")  # Clear any existing text
                self.hour_entry.insert(0, str(hour_value))

                self.minute_entry.delete(0, "end")  # Clear any existing text
                self.minute_entry.insert(0, str(minute_value))

                self.sub_entry.delete(0, "end")  # Clear any existing text
                self.sub_entry.insert(0, str(sub_value))
        except FileNotFoundError:
            # Se o arquivo config.yaml não existir, não há configurações a serem carregadas
            pass

    def start_timer_thread(self):
        h, m, _ = CountdownConfig.get_countdown()
        self.master.after(1000, self.update_timer)

    def update_timer(self):
        # Atualiza o rótulo com os valores do CountdownConfig
        timer = datetime.timedelta(
            hours=CountdownConfig.hours, minutes=CountdownConfig.minutes)
        timer_str = str(timer).split(".")[0]  # Remove os milissegundos
        self.timer_label.configure(text=timer_str)  # Atualiza o rótulo


def run_gui():
    root = CTk()

    # Tornar a janela não redimensionável
    root.resizable(width=False, height=False)

    root.geometry("500x300")
    root.title("Helper")

    gui_app = GuiApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
