# import tkinter as tk
from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class InfoArqs:
    def __init__(self, janela):
        
        # Cria a tabela
        self.tabela = ttk.Treeview(janela, columns=('Mode', 'Links', 'Owner', 'Group', 'Size', 'Last Modified', 'Name'))
        self.tabela.heading('#0', text='Linha')
        self.tabela.heading('Mode', text='Mode')
        self.tabela.heading('Links', text='Links')
        self.tabela.heading('Owner', text='Owner')
        self.tabela.heading('Group', text='Group')
        self.tabela.heading('Size', text='Size')
        self.tabela.heading('Last Modified', text='Last Modified')
        self.tabela.heading('Name', text='Name')
        
        # Variável para armazenar o diretório atual
        self.diretorio_atual = "/"
        
        # Carrega os dados iniciais da raiz do sistema de arquivos
        self.atualizar_tabela(self.diretorio_atual)

        # Configura a tabela na janela
        self.tabela.pack(padx=10, pady=10)

        # Configura o evento de seleção
        self.tabela.bind('<ButtonRelease-1>', self.mostrar_detalhes)

    def mostrar_detalhes(self, event):
        # Função para exibir os detalhes do item selecionado

        selecionado = self.tabela.selection()
        if selecionado:
            item = self.tabela.item(selecionado[0])
            linha = item['text']
            detalhes = self.dados[linha]

            # Obtém o nome do diretório/arquivo selecionado
            nome = detalhes['Name'].split(" ")
            # novo_diretorio += f'/{nome}'
            diretorio = self.diretorio_atual + nome[0] +'/'
            print("assim que fica:", diretorio)
            self.atualizar_tabela(diretorio)

    def atualizar_tabela(self, diretorio):
        # Atualiza os dados da tabela com base no diretório selecionado
        comando_ls = f"ls -lh {diretorio}"
        self.dados = interpretador.directory_info_py_to_dictionary(interpretador, comando_ls) # ->

        # Limpa itens anteriores da tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Inserindo os novos dados na tabela
        var = 1
        for chave, detalhes in self.dados.items():
            if var == 1:
                var = 0
                continue
            self.tabela.insert('', 'end', text=chave, values=(
                detalhes['Mode'],
                detalhes['Links'],
                detalhes['Owner'],
                detalhes['Group'],
                detalhes['Size'],
                detalhes['Last Modified'],
                detalhes['Name']
            ))

    def alterar_diretorio(self, novo_diretorio):
        # Método para alterar o diretório atual e atualizar a tabela
        self.diretorio_atual = novo_diretorio
        self.atualizar_tabela(novo_diretorio)