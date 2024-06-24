# import tkinter as tk
from tkinter import ttk
from BackEnd.interpretadorC import interpretador

class InfoArqs:
    def __init__(self, janela):
        self.janela = janela
        # Cria a tabela
        self.tabela = ttk.Treeview(self.janela, columns=('Name',  'Links', 'Owner', 'Group', 'Size', 'Last Modified','Mode'), show='headings')
        self.tabela.heading('Name', text='Name')
        self.tabela.heading('Mode', text='Mode')
        self.tabela.heading('Links', text='Links')
        self.tabela.heading('Owner', text='Owner')
        self.tabela.heading('Group', text='Group')
        self.tabela.heading('Size', text='Size')
        self.tabela.heading('Last Modified', text='Last Modified')
        
        # Define o estilo para a tag 'gray_background'
        self.tabela.tag_configure('Diretorio', background='lightblue')
        self.tabela.tag_configure('Arquivo', background='lightgray')
        
        # Variável para armazenar o diretório atual
        self.diretorio_atual = "/"
        
        # Carrega os dados iniciais da raiz do sistema de arquivos
        self.atualizar_tabela(self.diretorio_atual)

        # Configura a tabela na janela
        self.tabela.pack(padx=10, pady=10)
        # Adiciona o botão "Voltar"
        self.botao_voltar = ttk.Button(janela, text="Voltar", command=self.voltar_diretorio)
        self.botao_voltar.pack(padx=10, pady=10)

        # Configura o evento de seleção
        self.tabela.bind('<ButtonRelease-1>', self.mostrar_detalhes)

        # Inicia a atualização periódica da tabela
        self.atualizar_periodicamente()
        
    def mostrar_detalhes(self, event):
        # Função para exibir os detalhes do item selecionado
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
            print("assim que fica:", self.diretorio_atual)
            self.atualizar_tabela(self.diretorio_atual)

    def atualizar_tabela(self, diretorio):
        self.dados = interpretador.directory_info_py_to_dictionary(interpretador, diretorio)
        # Limpa itens anteriores da tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Inserindo os novos dados na tabela
        var = 1
        for chave, detalhes in self.dados.items():
            if var == 1:
                var = 0
                continue
            # print(f"chave: {chave} detalhes['Mode']: {detalhes['Mode']}")
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
        # Método para voltar um diretório
        print("self.diretorio_atual:",self.diretorio_atual)
        if self.diretorio_atual != "/":
            partes = self.diretorio_atual.rstrip('/').split('/')
            self.diretorio_atual = '/' if len(partes) == 1 else '/'.join(partes[:-1]) + '/'
            self.atualizar_tabela(self.diretorio_atual + '/')
    
    def atualizar_periodicamente(self):
        # Atualiza a tabela a cada 5 segundos
        print("Atualizou...")
        self.atualizar_tabela(self.diretorio_atual)
        self.janela.after(5000, self.atualizar_periodicamente)