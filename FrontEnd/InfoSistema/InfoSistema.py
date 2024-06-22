from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class InfoSistema:
    def __init__(self, janela):
        self.janela = janela
        
        self.label = ttk.Label(self.janela, text="Inicializando...", font=("Arial", 14))
        self.label.pack(padx=10, pady=10)
        
        # Chama a função para atualizar o conteúdo do label a cada 5 segundos
        self.atualizar_label()
    
    def atualizar_label(self):
        # Obtém os novos dados do interpretador
        dados = interpretador.version_info_d()
        
        # Atualiza o texto do label com os novos dados
        self.label.config(text=f"Dados do sistema: {dados}")
        print(dados)
        
        # Agenda a próxima atualização após 5 segundos
        self.janela.after(5000, self.atualizar_label)