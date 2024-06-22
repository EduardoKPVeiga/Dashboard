import tkinter as tk
from tkinter import *
from tkinter import ttk
# from Menu.Menu import Menu
# from BackEnd.interpretadorC import interpretador
from FrontEnd.Menu import Menu

class Controller:
    def __init__(self):
        self.Menu = tk.Tk()
        self.dash = Menu(self.Menu)
        self.Menu.mainloop()

    # def Atualizando_Dados():
    #     thread1 = threading.Thread(target=self.dados.buscaProcessos)
        
    #     thread1.start()

