import ctypes
_sys = ctypes.CDLL("./BackEnd/Arquivos_C/sys_call.so")  
_sys.version_info.restype = ctypes.c_char_p
_sys.memory_info.restype = ctypes.c_char_p
_sys.directory_info.restype = ctypes.c_char_p

class interpretador():
    global _sys
    # var = _sys.version_info()
    # print("version info: ", var)
    # print("------------------------------")
    # var = _sys.memory_info()
    # print("Memory info: ", var)
    # print("------------------------------")
    # command = "ls -lh /"
    # var = _sys.directory_info(command.encode('utf-8'))
    # print("Memory directory_info: \n", var)
    # dictionary = helpers.arquivo_para_dicionario(var)
    # print(dictionary)
    # print(diretorio_atual())
    # print(directory_info("pwd"))

    def directory_info_py(comando):
        
        return _sys.directory_info(comando.encode('utf-8'))

    
    def arquivo_para_dicionario(arquivo_binario):
        # Decodifica o arquivo binário para string
        texto = arquivo_binario.decode('utf-8')
        
        # Divide o texto em linhas
        linhas = texto.split('\n')
        
        # Cria um dicionário onde cada linha é um elemento
        dicionario = {}
        
        # Adiciona a primeira linha como 'header' ou outra chave especial
        if linhas:
            dicionario['header'] = linhas[0]
        
        # Processa as demais linhas
        for i, linha in enumerate(linhas[1:], start=1):
            partes = linha.split()
            if len(partes) >= 9:
                chave = f'linha_{i}'
                dicionario[chave] = {
                    'Mode': partes[0],
                    'Links': partes[1],
                    'Owner': partes[2],
                    'Group': partes[3],
                    'Size': partes[4],
                    'Last Modified': ' '.join(partes[5:8]), # Combina os campos de data e hora
                    'Name': ' '.join(partes[8:]) # Combina os campos do nome (pode conter espaços)
                }
        
        return dicionario
    
    def directory_info_py_to_dictionary(self, comando):
        var = self.directory_info_py(comando)
        return self.arquivo_para_dicionario(var)
# if __name__ == "__main__":
#     main()

    # 'linha_2': 'lrwxrwxrwx   1 root root    7 set 27  2023 bin -> usr/bin',