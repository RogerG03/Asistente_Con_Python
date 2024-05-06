from interfaz_inicial.gui_inicio import Gui_Inicio
from gui_voz.gui_voz import Gui_Voz
from gui_chat.gui_chat import Gui_Chat
from pathlib import Path
from tkinter import Toplevel, Tk, Canvas, Entry, Text, Button, PhotoImage


def gui_voz_window():
	window = Tk()
	Gui_Voz(window, gui_chat_window)
	window.update()


def gui_chat_window():
	window = Tk()
	Gui_Chat(window, gui_voz_window)
	window.update()

if __name__ == '__main__':
    window = Tk()
    Gui_Inicio(window, gui_voz_window)
    #Gui_Voz(window)

    window.mainloop()




