import tkinter as tk
# from tkinter import ttk
import threading
from FrontEnd.InfoArqs.InfoArqs import InfoArqs
from FrontEnd.InfoSistema.InfoSistema import InfoSistema
from FrontEnd.MemInfo.MemInfo import MemInfo
from FrontEnd.ProcessInfo.ProcessInfo import ProcessInfo
from FrontEnd.InfoProcessador.InfoProcessador import InfoProcessador


class Menu:
    """Classe Menu: vai chamar as demais paginas, passando a janela para fazerem as devidas alterações
    """
    def __init__(self, janela):
        """Inicializa a janela e o Menu:\n
        Menu -> tool bar 
        Args:
            janela (tkk): Recebe a janela para colocar as caracteristicas do Menu
        """
        self.janela = janela
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("1500x800")

        menu_bar = tk.Menu(self.janela)
        menu_bar.add_command(label="Infos Arquivos", command=self.mostrar_infos_arquivos)
        menu_bar.add_command(label="Infos Sistmema", command=self.mostrar_infos_sistema)
        menu_bar.add_command(label="Mem Infos", command=self.mostrar_mem_infos)
        menu_bar.add_command(label="Process Infos", command=self.mostrar_process_infos)
        menu_bar.add_command(label="Info Processador", command=self.mostrar_info_processador)
        
        self.janela.config(menu=menu_bar)

        
    def apagar_elementos(self): 
        """Função que irá limpar as tabelas e labels, conforme muda a pagina
        """
        for widget in self.janela.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()
                
    def mostrar_infos_arquivos(self):
        """Função que chama a pagina Info Arqs com uma thread
        """
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: InfoArqs(self.janela))
        thread.start()
    
    def mostrar_infos_sistema(self):
        """Função que chama a pagina Info sistema com uma thread
        """
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: InfoSistema(self.janela))
        thread.start()
        
    def mostrar_mem_infos(self):
        """Função que chama a pagina memoria infos com uma thread
        """
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: MemInfo(self.janela))
        thread.start()
        
    def mostrar_process_infos(self):
        """Função que chama a pagina preocess infos com uma thread
        """
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: ProcessInfo(self.janela))
        thread.start()
        
    def mostrar_info_processador(self):
        """Função que chama a pagina Info processador com uma thread
        """
        self.apagar_elementos()
        thread = threading.Thread(target=lambda: InfoProcessador(self.janela))
        thread.start()
        
    
