import tkinter as tk
from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class ProcessInfo:
    """Classe responsável por mostrar a página de Informações dos processos."""
    def __init__(self, janela):
        """Inicializa a tabela de processos na janela fornecida."""
        self.janela = janela
        self.tabela = ttk.Treeview(self.janela, columns=('Name', 'State', 'Pid', 'PPid', 'Uid', 'Gid', 'VmSize', 'VmRSS', 'voluntary_ctxt_switches', 'nonvoluntary_ctxt_switches'), show='headings')
        
        # Definindo os cabeçalhos das colunas
        self.tabela.heading('Name', text='Nome')
        self.tabela.heading('State', text='Estado')
        self.tabela.heading('Pid', text='Id')
        self.tabela.heading('PPid', text='Owner')
        self.tabela.heading('Uid', text='Group')
        self.tabela.heading('Gid', text='Size')
        self.tabela.heading('VmSize', text='Memória Virtual')
        self.tabela.heading('VmRSS', text='Memória Física')
        self.tabela.heading('voluntary_ctxt_switches', text='Trocas de Contexto Voluntárias')
        self.tabela.heading('nonvoluntary_ctxt_switches', text='Trocas de Contexto Involuntárias')

        # Definindo a largura das colunas e o alinhamento
        self.tabela.column('Name', width=150, anchor='center')
        self.tabela.column('State', width=100, anchor='center')
        self.tabela.column('Pid', width=50, anchor='center')
        self.tabela.column('PPid', width=50, anchor='center')
        self.tabela.column('Uid', width=50, anchor='center')
        self.tabela.column('Gid', width=50, anchor='center')
        self.tabela.column('VmSize', width=100, anchor='center')
        self.tabela.column('VmRSS', width=100, anchor='center')
        self.tabela.column('voluntary_ctxt_switches', width=150, anchor='center')
        self.tabela.column('nonvoluntary_ctxt_switches', width=150, anchor='center')

        self.atualizar_tabela()
        
    def atualizar_tabela(self):
        """Atualiza a tabela a cada 5 segundos."""
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Obtém os dados dos processos
        lista = interpretador.process_status_d(interpretador)
        self.dados = interpretador.filtrando_dados_process(lista)       

        for processo in self.dados:
            # Certifica-se de que todos os campos necessários estão presentes e não são None
            valores = (
                processo.get('Name', ''),
                processo.get('State', ''),
                processo.get('Pid', ''),
                processo.get('PPid', ''),
                processo.get('Uid', ''),
                processo.get('Gid', ''),
                processo.get('VmSize', ''),
                processo.get('VmRSS', ''),
                processo.get('voluntary_ctxt_switches', ''),
                processo.get('nonvoluntary_ctxt_switches', '')
            )
            # Insere os valores na tabela
            self.tabela.insert('', 'end', values=valores)
        
        # Empacota a tabela na janela e agenda a atualização novamente após 5 segundos
        self.tabela.pack(padx=10, pady=10, expand=True, fill='both')
        self.janela.after(5000, self.atualizar_tabela)