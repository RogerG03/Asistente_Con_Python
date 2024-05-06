from pathlib import Path

import tkinter
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from gui.gui import Gui
from logica_del_asistente_chat import establecer_referencia, iniciar_chat

class Gui_Chat(Gui):
    """Chat de texto con la IA"""
    def __init__(self, window, gui_voz_window):
        super(Gui_Chat, self).__init__(window)
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"assets\frame0")

        self.gui_voz_window = gui_voz_window

        self.window.title("Chat de texto | Ruperta")

        self.registry = ""
        self.respuesta2 = False
        self.funcion = None

        #Declaracion de las imagenes
        self._load_images()
        #Dibujado de elementos
        self._draw_window()
        #Abrir centrado
        self._open_centered()
        establecer_referencia(self)


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
            364.0,
            image=self.image_image_1
        )


        image_2 = canvas.create_image(
            142.0,
            32.0,
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
            x=11.0,
            y=12.0,
            width=56.0,
            height=40.0
        )


        image_3 = canvas.create_image(
            521.0,
            506.0,
            image=self.image_image_3
        )


        entry_bg_1 = canvas.create_image(
            514.5,
            506.5,
            image=self.entry_image_1
        )
        self.entry_1 = Text(
            bd=0,
            bg="#F6FAFD",
            fg="#000716",
            highlightthickness=0,
            state = "disabled"
        )
        self.entry_1.place(
            x=259.0,
            y=422.0,
            width=511.0,
            height=167.0
        )


        image_4 = canvas.create_image(
            483.0,
            662.0,
            image=self.image_image_4
        )


        entry_bg_2 = canvas.create_image(
            481.0,
            662.0,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=251.0,
            y=644.0,
            width=460.0,
            height=34.0
        )


        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.button_2_action,
            relief="flat"
        )
        button_2.place(
            x=752.0,
            y=633.0,
            width=80.0,
            height=58.0
        )


        image_5 = canvas.create_image(
            514.0,
            216.0,
            image=self.image_image_5
        )

    def _load_images(self):
        self.image_image_1 = PhotoImage(
            file=self._relative_to_assets("image_1.png"))
        self.image_image_2 = PhotoImage(
            file=self._relative_to_assets("image_2.png"))
        self.button_image_1 = PhotoImage(
            file=self._relative_to_assets("button_1.png"))
        self.image_image_3 = PhotoImage(
            file=self._relative_to_assets("image_3.png"))
        self.entry_image_1 = PhotoImage(
            file=self._relative_to_assets("entry_1.png"))
        self.image_image_4 = PhotoImage(
            file=self._relative_to_assets("image_4.png"))
        self.entry_image_2 = PhotoImage(
            file=self._relative_to_assets("entry_2.png"))
        self.button_image_2 = PhotoImage(
            file=self._relative_to_assets("button_2.png"))
        self.image_image_5 = PhotoImage(
            file=self._relative_to_assets("image_5.png"))

    def button_1_action(self):
        self.window.destroy()
        self.gui_voz_window()

    def button_2_action(self):
        print("Boton enviar pulsado")
        if self.entry_2.get() == "":
            return
        self.registry += "Usuario: " + self.entry_2.get() + "\n"


        # Agregar nuevo texto al widget Text
        self.entry_1.config(state="normal")  # Habilitar el widget para editar
        #self.entry_1.delete("1.0", tkinter.END)   # Eliminar el contenido actual
        #self.entry_1.insert(tkinter.END, self.registry)  # Insertar el nuevo texto
        self.entry_1.insert(tkinter.END, "Usuario: " + self.entry_2.get() + "\n") 
        self.entry_1.config(state="disabled")  # Volver a deshabilitar el widget
        self.entry_1.see(tkinter.END)

        if self.respuesta2:
           self.funcion(self.entry_2.get())
           self.respuesta2 = False 
        else:
            iniciar_chat(self.entry_2.get())
        self.entry_2.delete(0, tkinter.END)

        #self.window.destroy()
        #self.gui_chat_window()

    def ruperta_responde(self, mensaje):
        
        self.registry += "Ruperta: " + mensaje + "\n"
        
        # Agregar nuevo texto al widget Text
        self.entry_1.config(state="normal")  # Habilitar el widget para editar
        #self.entry_1.delete("1.0", tkinter.END)   # Eliminar el contenido actual
        #self.entry_1.insert(tkinter.END, self.registry)  # Insertar el nuevo texto
        self.entry_1.insert(tkinter.END, "Ruperta: " + mensaje + "\n") 
        self.entry_1.config(state="disabled")  # Volver a deshabilitar el widget

