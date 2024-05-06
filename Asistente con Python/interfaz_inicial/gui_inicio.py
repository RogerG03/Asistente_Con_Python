from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from gui.gui import Gui

from logica_del_asistente import obtener_saludo, hablar

class Gui_Inicio(Gui):
    
    """Venta principal de bienvenida del programa"""
    def __init__(self, window, gui_voz_window):
        super(Gui_Inicio, self).__init__(window)
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets\frame0")

        self.gui_voz_window = gui_voz_window

        self.window.title("Asistente inteligente | Ruperta")

        #Declaracion de las imagenes
        self._load_images()
        #Dibujado de elementos
        self._draw_window()
        #Abrir centrado
        self._open_centered()
        #Llamar a la función ventana_cargada después de 2000 ms (2 segundos) de abrir la ventana
        window.after(700, saludar)

    
    def _draw_window(self):

        canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 720,
            width = 1080,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)

        image_1 = canvas.create_image(
            562.0,
            360.0,
            image=self.image_image_1
        )


        image_2 = canvas.create_image(
            540.0,
            360.0,
            image=self.image_image_2
        )


        button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.button_1_action,
            relief="flat"
        )
        button_1.place(
            x=127.0,
            y=523.0,
            width=501.0,
            height=148.0
        )

    def _load_images(self):
        self.image_image_1 = PhotoImage(
            file=self._relative_to_assets("image_1.png"))
        self.image_image_2 = PhotoImage(
            file=self._relative_to_assets("image_2.png"))
        self.button_image_1 = PhotoImage(
            file=self._relative_to_assets("button_1.png"))
    
    def button_1_action(self):
        self.window.destroy()
        self.gui_voz_window()

def saludar():
    saludo = obtener_saludo()
    hablar(saludo)