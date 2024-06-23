from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class ProcessInfo:
    
    def __init__(self, janela):
        self.janela = janela
        self.tabela = ttk.Treeview(self.janela, columns=('Name', 'State', 'Pid', 'PPid', 'Uid', 'Gid', 'VmSize', 'VmRSS', 'Threads', 'voluntary_ctxt_switches', 'nonvoluntary_ctxt_switches', ), show='headings')
        
        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        # Limpa itens anteriores da tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        lista = interpretador.process_status_d(interpretador)
        self.dados = interpretador.filtrando_dados_process(lista)       
        
        for col in self.dados[0].keys():
            self.tabela.heading(col, text=col)
            
        for processo in self.dados:
            self.tabela.insert('', 'end', values=list(processo.values()))
        
        self.tabela.pack(padx=10, pady=10, expand=True, fill='both')
        print("Tabela Atualizada")
        self.janela.after(5000, self.atualizar_tabela) # ele demora 5 sec para fazer a primeira vez
            
            