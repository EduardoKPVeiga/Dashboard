from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class MemInfo:
    """Classe responsável por mostrar a pagina de inforações de memoria
    """
    def __init__(self, janela):
        """Função init, inicializa a tabela

        Args:
            janela (tkk): receba a janela, para fazer as devidas alterações da pagina
        """
        self.janela = janela
        self.tabela = ttk.Treeview(janela, columns=('Memoria', 'Espaço'), show='headings')
        self.tabela.heading('Memoria', text='Memoria')
        self.tabela.heading('Espaço', text='Espaço')
        
        self.tabela.pack(padx=10, pady=10, expand=True, fill='both')
        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        """Função que vai atualizar a cada 5 segundos a tabela
        """
        self.dados = interpretador.memory_info_d(interpretador)
        try:
            for item in self.tabela.get_children():
                self.tabela.delete(item)


            for item in self.dados:
                self.tabela.insert('', 'end', values=item)
            if self.tabela.winfo_exists():
                self.janela.after(5000, self.atualizar_tabela)
        except Exception:
            print(f"A troca de contexto ocasionou um erro na atualização de dados em MemInfo")
            
            