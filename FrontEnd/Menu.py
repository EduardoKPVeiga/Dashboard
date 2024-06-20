import tkinter as tk
# from tkinter import ttk

from FrontEnd.InfoArqs.InfoArqs import InfoArqs


class Menu:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("1500x800")
        
        # Cria uma área para exibir o conteúdo inicial
        self.content_label = tk.Label(self.janela, text="Bem-vindo ao Gerenciador de Tarefas", font=("Arial", 20))
        self.content_label.pack(pady=20)

        # Cria a barra de menu
        menu_bar = tk.Menu(self.janela)
        menu_bar.add_command(label="Infos Arquivos", command=self.mostrar_infos_arquivos)
        # Configura a barra de menu na janela principal
        self.janela.config(menu=menu_bar)
        self.content_label.pack_forget()
        
    def mostrar_infos_arquivos(self): # esse cara vai ser o mediador de todos os menus 
        for widget in self.janela.winfo_children():
            widget.destroy()
        InfoArqs(self.janela)
