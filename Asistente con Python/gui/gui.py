from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
        

class Gui():
    """Clase padre para todas las GUI de este programa"""
    def __init__(self, window):
        self.window = window

        self.width = 1080
        self.height = 720
        self.window.geometry("1080x720")
        self.window.configure(bg = "#FFFFFF")
        #self.window.title("Asistente inteligente | Ruperta")
        self.window.resizable(False, False)


    def _relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def _open_centered(self):
        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.window.winfo_screenwidth()
        alto_pantalla = self.window.winfo_screenheight()

        x_centro = int(ancho_pantalla / 2 - self.width / 2)
        y_centro = int(alto_pantalla / 2 - self.height / 2)

        # Establecer la geometría de la ventana para que se abra centrada
        self.window.geometry("+{}+{}".format(x_centro, y_centro))

