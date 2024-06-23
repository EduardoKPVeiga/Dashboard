import tkinter as tk
# from tkinter import ttk
import threading
from FrontEnd.InfoArqs.InfoArqs import InfoArqs
from FrontEnd.InfoSistema.InfoSistema import InfoSistema
from FrontEnd.MemInfo.MemInfo import MemInfo
from FrontEnd.ProcessInfo.ProcessInfo import ProcessInfo
from FrontEnd.InfoProcessador.InfoProcessador import InfoProcessador

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
        menu_bar.add_command(label="Infos Sistmema", command=self.mostrar_infos_sistema)
        menu_bar.add_command(label="Mem Infos", command=self.mostrar_mem_infos)
        menu_bar.add_command(label="Process Infos", command=self.mostrar_process_infos)
        menu_bar.add_command(label="Info Processador", command=self.mostrar_info_processador)
        
        
        # mostrar_info_processador
        # Configura a barra de menu na janela principal
        self.janela.config(menu=menu_bar)
        self.content_label.pack_forget()
        
    def apagar_elementos(self): 
        for widget in self.janela.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()
                
    def mostrar_infos_arquivos(self):
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: InfoArqs(self.janela))
        thread.start()
    
    def mostrar_infos_sistema(self):
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: InfoSistema(self.janela))
        thread.start()
        
    def mostrar_mem_infos(self):
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: MemInfo(self.janela))
        thread.start()
        
    def mostrar_process_infos(self):
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: ProcessInfo(self.janela))
        thread.start()
        
    def mostrar_info_processador(self):
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: InfoProcessador(self.janela))
        thread.start()
        
    
