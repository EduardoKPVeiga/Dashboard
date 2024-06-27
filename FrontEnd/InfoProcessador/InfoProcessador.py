from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class InfoProcessador:
    """Classe da pagina InfoProcessador que 
        tem como objetivo mostrar os seguintes dados:\n
            1-percentual de uso do processador\n
            2-percentual de tempo ocioso\n
            3-quantidade total de processos\n
            4-quantidade total de threads \n
    """
    def __init__(self, janela):
        """Função init: Inicializa tabela e label
        Args:
            janela (ttk): recebe a janela para fazer alterações da pagina
        """
        self.janela = janela
        self.label = ttk.Label(self.janela)
        self.tabela = ttk.Treeview(janela, columns=('Processador', 'Usando', 'Ocioso'), show='headings')
        self.tabela.heading('Processador', text='Processador')
        self.tabela.heading('Usando', text='% Usando')
        self.tabela.heading('Ocioso', text='% Ocioso')
        self.tabela.column('Processador', anchor='center')
        self.tabela.column('Usando', anchor='center')
        self.tabela.column('Ocioso', anchor='center')
        
        self.tabela.config(height=20)
        self.tabela.pack(padx=10, pady=10)
        self.label.pack(padx=1, pady=1)
        self.atualizar_pagina()
    
    def atualizar_pagina(self):
        """Função para atualizar elementos da pagina a cada 5 segundos:\n
            -> Tabela\n
            -> Label
        """
        try:
            if self.tabela:
                for item in self.tabela.get_children():
                    self.tabela.delete(item)
        
            self.percents = interpretador.cpu_usage_sysinfo(interpretador)
            self.threads = interpretador.qtd_threads_running(interpretador)
            self.processos = interpretador.qtd_proc_running_sysinfo(interpretador)
            
            self.label.config(text=(
                f"Quantidade de Threads: {self.threads}\n"
                f"Quantidade de Processos: {self.processos}"
            ))
            
            for item in self.percents:
                processor = item['Processador']
                percent_usando = f"{item['Usando']:.2f}"
                percent_ocioso = f"{item['Ocioso']:.2f}"
                self.tabela.insert('', 'end', text='', values=(processor, percent_usando, percent_ocioso))
                
            if self.tabela.winfo_exists():
                self.janela.after(5000, self.atualizar_pagina)
        except Exception:
            print(f"A troca de contexto ocasionou um erro na atualização de dados em InfoProcessador")
       