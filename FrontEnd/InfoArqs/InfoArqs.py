import tkinter as tk
from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class InfoArqs:
    """Classe InfoArqs responsável por permitir navegação na árvore de diretórios
        e também Listar os arquivos contidos em um diretório, 
        juntamente com os atributos de cada arquivo
    """
    def __init__(self, janela):
        """função init: Inicializa a tabela, varivaies importantes usadas na pagina e o botão

        Args:
            janela (tkk): recebe a janela, para fazer modificações na pagina
        """
        self.janela = janela
        self.tabela = ttk.Treeview(self.janela, columns=('Name',  'Links', 'Owner', 'Group', 'Size', 'Last Modified','Mode'), show='headings')
        self.tabela.heading('Name', text='Name')
        self.tabela.heading('Mode', text='Mode')
        self.tabela.heading('Links', text='Links')
        self.tabela.heading('Owner', text='Owner')
        self.tabela.heading('Group', text='Group')
        self.tabela.heading('Size', text='Size')
        self.tabela.heading('Last Modified', text='Last Modified')
        self.tabela.column('Name', anchor='center')
        self.tabela.column('Links', anchor='center')
        self.tabela.column('Owner', anchor='center')
        self.tabela.column('Group', anchor='center')
        self.tabela.column('Size', anchor='center')
        self.tabela.column('Last Modified', anchor='center')
        self.tabela.column('Mode', anchor='center')
        self.tabela.tag_configure('Diretorio', background='lightblue')
        self.tabela.tag_configure('Arquivo', background='lightgray')
        
        self.diretorio_atual = "/"
        
        self.atualizar_tabela(self.diretorio_atual)
        
        self.tabela.pack(padx=10, pady=10)
        
        self.botao_voltar = ttk.Button(janela, text="Voltar", command=self.voltar_diretorio)
        self.botao_voltar.pack(padx=10, pady=10)
        self.tabela.bind('<ButtonRelease-1>', self.mostrar_detalhes)
        self.atualizar_periodicamente()
        
    def mostrar_detalhes(self, event):
        """Função que vai selecionar o diretorio para atualizar,
        caso pressionado algum item na tabela, que não seja um arquivo
        Args:
            event : evento de pressionar algum item
        """
        item = self.tabela.identify_row(event.y)
        if 'Arquivo'  in self.tabela.item(item, 'tags'):
            return
        
        selecionado = self.tabela.selection()
        if selecionado:
            item = self.tabela.item(selecionado[0])
            linha = item['text']
            detalhes = self.dados[linha]


            nome = detalhes['Name'].split(" ")
            self.diretorio_atual = self.diretorio_atual + nome[0] +'/'
            self.atualizar_tabela(self.diretorio_atual)

    def atualizar_tabela(self, diretorio):
        """Função responsável por atualizar os itens da tabela:
        Args:
            diretorio (string): recebe o diretorio que vai atualizar a tabela
        """
        self.dados = interpretador.directory_info_py_to_dictionary(interpretador, diretorio)
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for chave, detalhes in self.dados.items():
            if detalhes['Mode'][0] != 'd':
                self.tabela.insert('', 'end', text=chave,tags=('Arquivo',), values=(
                    detalhes['Name'],
                    detalhes['Links'],
                    detalhes['Owner'],
                    detalhes['Group'],
                    detalhes['Size'],
                    detalhes['Last Modified'],
                    detalhes['Mode'],
                ))
            else:
                self.tabela.insert('', 'end', text=chave,tags=('Diretorio',), values=(
                    detalhes['Name'],
                    detalhes['Links'],
                    detalhes['Owner'],
                    detalhes['Group'],
                    detalhes['Size'],
                    detalhes['Last Modified'],
                    detalhes['Mode'],
                ))

        
    def voltar_diretorio(self):
        """Função do botão para retornar o diretório anterior
        """
        if self.diretorio_atual != "/":
            partes = self.diretorio_atual.rstrip('/').split('/')
            self.diretorio_atual = '/' if len(partes) == 1 else '/'.join(partes[:-1]) + '/'
            self.atualizar_tabela(self.diretorio_atual + '/')
    
    def atualizar_periodicamente(self):
        """Função para atualizar a cada 5 segundos
        """
        self.atualizar_tabela(self.diretorio_atual)
        self.janela.after(5000, self.atualizar_periodicamente)