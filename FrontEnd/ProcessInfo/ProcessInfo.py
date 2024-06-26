from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class ProcessInfo:
    """Classe responsável por mostrar a pagina de Informações dos processos
    """
    def __init__(self, janela):
        """Função init, Inicializa a tabela
        Args:
            janela (tkk): receba a janela, para fazer as alterações da pagina
        """
        self.janela = janela
        self.tabela = ttk.Treeview(self.janela, columns=('Name', 'State', 'Pid', 'PPid', 'Uid', 'Gid', 'VmSize', 'VmRSS', 'Threads', 'voluntary_ctxt_switches', 'nonvoluntary_ctxt_switches', ), show='headings')
        
        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        """Função que vai atualizar a tabela a cada 5 segundos
        """
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        lista = interpretador.process_status_d(interpretador)
        self.dados = interpretador.filtrando_dados_process(lista)       
        
        for col in self.dados[0].keys():
            self.tabela.heading(col, text=col)
            
        for processo in self.dados:
            self.tabela.insert('', 'end', values=list(processo.values()))
        
        self.tabela.pack(padx=10, pady=10, expand=True, fill='both')
        self.janela.after(5000, self.atualizar_tabela)
            