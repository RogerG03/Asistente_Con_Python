from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from gui.gui import Gui

from logica_del_asistente import iniciar

class Gui_Voz(Gui):
    """Chat de voz con la IA"""
    def __init__(self, window, gui_chat_window):
        super(Gui_Voz, self).__init__(window)
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets\frame0")

        self.gui_chat_window = gui_chat_window

        self.window.title("Chat de voz | Ruperta")

        #Declaracion de las imagenes
        self._load_images()
        #Dibujado de elementos
        self._draw_window()
        #Abrir centrado
        self._open_centered()

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
            540.0,
            360.0,
            image=self.image_image_1
        )


        image_2 = canvas.create_image(
            505.0,
            224.0,
            image=self.image_image_2
        )

        image_3 = canvas.create_image(
            510.0,
            543.0,
            image=self.image_image_3
        )

        image_4 = canvas.create_image(
            928.0,
            36.0,
            image=self.image_image_4
        )

        button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.button_1_action,
            relief="flat"
        )
        button_1.place(
            x=1010.0,
            y=15.0,
            width=56.0,
            height=42.0
        )

        image_5 = canvas.create_image(
            510.0,
            499.0,
            image=self.image_image_5
        )

        image_6 = canvas.create_image(
            509.0,
            630.0,
            image=self.image_image_6
        )

        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.button_2_action,
            relief="flat"
        )
        button_2.place(
            x=411.0,
            y=602.0,
            width=204.0,
            height=51.0
        )

    def _load_images(self):
        self.image_image_1 = PhotoImage(
            file=self._relative_to_assets("image_1.png"))
        self.image_image_2 = PhotoImage(
            file=self._relative_to_assets("image_2.png"))        
        self.image_image_3 = PhotoImage(
            file=self._relative_to_assets("image_3.png"))        
        self.image_image_4 = PhotoImage(
            file=self._relative_to_assets("image_4.png"))        
        self.button_image_1 = PhotoImage(
            file=self._relative_to_assets("button_1.png"))        
        self.image_image_5 = PhotoImage(
            file=self._relative_to_assets("image_5.png"))        
        self.image_image_6 = PhotoImage(
            file=self._relative_to_assets("image_6.png"))        
        self.button_image_2 = PhotoImage(
            file=self._relative_to_assets("button_2.png"))
    
    def button_1_action(self):
        self.window.destroy()
        self.gui_chat_window()

    def button_2_action(self):
        print("Boton hablar pulsado")
        iniciar()
        #self.window.destroy()
        #self.gui_chat_window()

