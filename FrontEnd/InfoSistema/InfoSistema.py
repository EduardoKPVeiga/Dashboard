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

        self.title1 = ttk.Label(self.janela, text="", font=("Arial", 14))
        self.title2 = ttk.Label(self.janela, text="", font=("Arial", 14))

        self.tabela = ttk.Treeview(self.janela, columns=('Major', 'Minor', 'Blocks', 'Name'), show='headings')
        
        self.tabela.heading('Major', text='Major')
        self.tabela.heading('Minor', text='Minor')
        self.tabela.heading('Blocks', text='Blocks')
        self.tabela.heading('Name', text='Name')
        
        self.tabela.column('Major', width=150, anchor='center')
        self.tabela.column('Minor', width=100, anchor='center')
        self.tabela.column('Blocks', width=50, anchor='center')
        self.tabela.column('Name', width=50, anchor='center')

        self.title1.pack(padx=10, pady=10)
        self.title2.pack(padx=10, pady=10)

        self.atualizar_label()
    
    def atualizar_label(self):
        """Função que vai atualizar os labels a cada 5 segundos, das informações do sistema
        """

        try:
            self.version = interpretador.version_info_d()
            print(self.version)
            self.title1.config(text=self.version[0])
            self.title2.config(text=self.version[1])

            for item in self.tabela.get_children():
                self.tabela.delete(item)

            self.partitions = interpretador.partitions_info()      
            for partition in self.partitions:
                valores = []
                for item in partition:
                    valores.append(item)
                self.tabela.insert('', 'end', values=valores)
            
            self.tabela.pack(padx=10, pady=10, expand=True, fill='both')

            if self.tabela.winfo_exists():
                self.janela.after(5000, self.atualizar_tabela)

        except:
            print("Erro ao tentar atualizar a pagina InfoSistema")