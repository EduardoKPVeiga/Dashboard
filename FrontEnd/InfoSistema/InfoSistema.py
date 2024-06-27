from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class InfoSistema:
    """Classe responsável por mostrar Informações do sistema
    """
    def __init__(self, janela):
        """Função Init: Inicializa as Labels

        Args:
            janela (ttk): receba a janela, para fazer as alterações da pagina
        """
        self.janela = janela
        self.label = ttk.Label(self.janela, text="Inicializando...", font=("Arial", 14)) # pq isso ta qui?
        self.label.pack(padx=10, pady=10)
        self.atualizar_label()
    
    def atualizar_label(self):
        """Função que vai atualizar os labels a cada 5 segundos, das informações do sistema
        """
        try:
            dados = interpretador.version_info_d()
            self.label.config(text=f"Dados do sistema: {dados}")
            if self.label.winfo_exists():
                self.janela.after(5000, self.atualizar_label)
        except Exception:
            print(f"A troca de contexto ocasionou um erro na atualização de dados em InfoSistema")