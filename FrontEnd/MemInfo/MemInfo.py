from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class MemInfo:
    
    def __init__(self, janela):
        self.janela = janela
        self.tabela = ttk.Treeview(janela, columns=('Memoria', 'Espaço'), show='headings')
        self.tabela.heading('Memoria', text='Memoria')
        self.tabela.heading('Espaço', text='Espaço')
        
        self.tabela.pack(padx=10, pady=10, expand=True, fill='both')

        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        self.dados = interpretador.memory_info_d(interpretador)
        
        # Limpa itens anteriores da tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Inserindo os novos dados na tabela
        for item in self.dados:
            self.tabela.insert('', 'end', values=item)
            
        self.janela.after(5000, self.atualizar_tabela) # ele demora 5 sec para fazer a primeira vez
            
            