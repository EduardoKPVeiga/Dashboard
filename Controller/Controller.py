import tkinter as tk
from tkinter import *
from FrontEnd.Menu import Menu

class Controller:
    """Função inicializa o software
    """
    def __init__(self):
        """Inicializa tk e deixa em loop
        """
        self.Menu = tk.Tk()
        self.dash = Menu(self.Menu)
        self.Menu.mainloop()
