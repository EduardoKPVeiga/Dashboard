import ctypes
import time
_sys = ctypes.CDLL("./BackEnd/Arquivos_C/sys_call.so")  

class interpretador():
    # As funções alterão as variaveis e o front-end usa as variaveis
    
    def __init__(self):
        # _sys = ctypes.CDLL("./BackEnd/Arquivos_C/sys_call.so")  
        
        _sys.directory_info.restype = ctypes.c_char_p
        
        _sys.read_sys_info.restype = ctypes.c_char_p
        _sys.read_sys_info.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        # Read the pseudo filesystem and subdirectories
        
        # CPU clock per second
        

        
        
    
    def clk_per_second_d():
        _sys.clk_per_second.restype = ctypes.c_uint64
        return _sys.clk_per_second()
        
    def remove(string, char):
        return string.replace(char, "")
    
    def memory_info_d(self):
        _sys.read_sys_info.restype = ctypes.c_char_p
        _sys.read_sys_info.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        result = (_sys.read_sys_info("/proc/meminfo".encode('utf-8'), (16 * 1024))).decode('utf-8')
        result_v = result.split("\n")
        result_m = []

        for line in result_v:
            line = self.remove(line, " ")
            result_m.append(line.split(":"))

        return result_m
        
    def version_info_d():
        _sys.version_info.restype = ctypes.c_char_p
        return _sys.version_info()
    
    def read_proc_ids_d():
        _sys.read_dir_info.restype = ctypes.c_char_p
        _sys.read_dir_info.argtypes = [ctypes.c_char_p]
        result = (_sys.read_dir_info("/proc/".encode('utf-8'))).decode('utf-8')
        
        result_v = []
        result_v_process = []

        result_v = result.split("\n")

        # Returns only process IDs
        for item in result_v:
            if item.isnumeric() == True:
                result_v_process.append(item)

        return result_v_process

    def process_status_d(self):
        _sys.read_sys_info.restype = ctypes.c_char_p
        _sys.read_sys_info.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        result = ""
        process = []
        path = "/proc/"

        proc_id_list = self.read_proc_ids_d() # tem que colocar aqui tbm


        for proc in proc_id_list:
            result = (_sys.read_sys_info((path + proc + "/status").encode('utf-8'), (16 * 1024))).decode('utf-8')

            # List with the information of a single process
            process_list_items = result.split("\n")

            # Matrix with the information of a single process
            process_matrix_items = []

            for process_item in process_list_items:
                # Split only in the first occurrence
                process_matrix_items.append(self.remove(process_item, "\t").split(":", 1)) # Because some names may have ':' in them

            process.append(process_matrix_items)

        return process
    
    def cpu_usage_since_boot_d():
        _sys.read_sys_info.restype = ctypes.c_char_p
        _sys.read_sys_info.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        cpu_usage = (_sys.read_sys_info("/proc/stat".encode('utf-8'), (4 * 1024))).decode('utf-8')
        cpu_usage_list = cpu_usage.split("\n")
        cpu_usage_matrix = []

        for i in range(9):
            cpu_usage_matrix.append(cpu_usage_list[i].split(" "))
        # CPU line has 2 ' '
        cpu_usage_matrix[0].pop(1)

        # clock per second, used to calculate the CPU usage
        clk_tck = _sys.clk_per_second()

        system_uptime_s = (_sys.read_sys_info("/proc/uptime".encode('utf-8'), 128)).decode('utf-8')
        system_uptime = system_uptime_s.split(" ")

        cpu_usage_calc = []
        for line in cpu_usage_matrix:
            total_time = 0
            for i in range(1,8):
                total_time += int(line[i])
            cpu_usage_calc.append([line[0], int(line[4]), total_time])

        return cpu_usage_calc
    
    def proc_memory_usage_d(self):
        process_list = self.process_status_d(self)
        process_mem_usage_list = []

        # Add all process' names
        for proc in process_list:
            proc_mem = []
            proc_mem.append(proc[0][1])

            # Add only process name and memory usage
            for item in proc:
                if (item[0] == "VmSize"):
                    proc_mem.append(self.remove(item[1], " "))
                    break

            process_mem_usage_list.append(proc_mem)
        
        return process_mem_usage_list
    
    def directory_info_py(Dict):
        _sys.directory_info.restype = ctypes.c_char_p
        return _sys.directory_info(Dict.encode('utf-8'))

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
                chave = f'{i}'
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

    def filtrando_dados_process(arry_process):
        """
        Retorna um dicionario com as informações mais importantes da função proces_status

        Args:
            arry_process (lista): lista dos elementos do process_status

        Returns:
            lista: retorna uma lista de dicionarios dos elementos
        """
        informacoes_importantes = []
        for processo in arry_process:
            info_processo = {}
            for atributo in processo:
                if len(atributo) == 2:  # Verifica se atributo é uma tupla de dois elementos
                    chave, valor = atributo
                    if chave in ['Name', 'State', 'Pid', 'PPid', 'Uid', 'Gid', 'VmSize', 'VmRSS', 'Threads', 'voluntary_ctxt_switches', 'nonvoluntary_ctxt_switches']:
                        info_processo[chave] = valor
            informacoes_importantes.append(info_processo)
        return informacoes_importantes

    def list_proc_running_sysinfo(self):
        # Read subdirectories
        process_list = self.process_status_d(self)
        process_names_list = []

        # Add all process' names
        for proc in process_list:
            process_names_list.append(proc[0][1])

        return process_names_list
        
    def cpu_usage_sysinfo(self):
        """Função que transforma lista de dados do processador uma lista de dicionarios

        Returns:
            lista: [{'Processador':'cpu', 'Usando':'33%', 'Ocioso': '66%'} ...]
        """
        cpu_usage_prev = self.cpu_usage_since_boot_d()
        time.sleep(0.5)
        cpu_usage_actual = self.cpu_usage_since_boot_d()
        
        cpu_usage = []

        for i in range(len(cpu_usage_actual)):
            user_diff = cpu_usage_actual[i][1] - cpu_usage_prev[i][1]
            system_diff = cpu_usage_actual[i][2] - cpu_usage_prev[i][2]
            total_diff = user_diff + system_diff
            
            if total_diff > 0:
                percent_usando = (user_diff / total_diff) * 100
                percent_ocioso = 100 - percent_usando
            else:
                percent_usando = 0
                percent_ocioso = 100

            cpu_usage.append({
                'Processador': cpu_usage_actual[i][0],
                'Usando': percent_usando,
                'Ocioso': percent_ocioso
            })

        return cpu_usage    

    def proc_info_sysinfo(self):
        """Função vai Transformar a chama de sistema desorganizada em uma lista organizada de dados relevantes

        Returns:
            lista: lista de informações relevantes para o sistema
        """
        proc_status = self.process_status_d(self)

        proc_info = []

        # Extract the information from 'status'
        for proc in proc_status:
            data = []
            for item in proc:
                if item[0] == "Name" or item[0] == "State" or item[0] == "Tgid" or item[0] == "VmSize" or item[0] == "Threads":
                    if item[0] == "VmSize":
                        data.append([item[0], self.remove(item[1], " ")])
                    else:
                        data.append([item[0], item[1]])
            proc_info.append(data)

        #[[["Name", "Name1"], ["State", "State1"], ["Tgid", "ID1"], ["VmSize", "VmSize1"], ["Threads", "Threads1"]], ... , [["Name", "NameN"], ["State", "StateN"], ["Tgid", "IDN"], ["VmSize", "VmSizeN"], hreads", "ThreadsN"]]]
        return proc_info

    def qtd_proc_running_sysinfo(self):
        """Função que retorna a quantidade de processos que estão rodando atualmente

        Returns:
            int: 333
        """
        return len(self.list_proc_running_sysinfo(self))

    def qtd_threads_running(self):
        """Função que retorna a quanitdade de threads que estão rodando

        Returns:
            int: 667
        """
        total_threads = 0
        proc_info = self.proc_info_sysinfo(self)

        # Search for "Thread" atribute
        for proc in proc_info:
            for item in proc:
                if item[0] == "Threads":
                    total_threads += int(item[1])

        return total_threads
    
def main ():
    # print("clk_per_second_d:", interpretador.clk_per_second_d())
    # print("memory_info_d:", interpretador.memory_info_d(interpretador))
    # print("version_info_d:", interpretador.version_info_d())
    # print("read_proc_ids_d:", interpretador.read_proc_ids_d())
    # lista = interpretador.process_status_d(interpretador)
    # primeiros_10_itens = lista[:2]
    # print("process_status_d:", interpretador.filtrando_dados_process(primeiros_10_itens))
    # print("cpu_usage_since_boot_d:", interpretador.cpu_usage_since_boot_d())
    # print("interpretador.proc_memory_usage_d:", interpretador.proc_memory_usage_d(interpretador))
    # print("list_proc_running_sysinfo:", interpretador.list_proc_running_sysinfo(interpretador))
    print("cpu_usage_sysinfo:", interpretador.cpu_usage_sysinfo(interpretador)) # uso do processador 2.
    # print("proc_info_sysinfo:", interpretador.proc_info_sysinfo(interpretador))
    # print("qtd_proc_running_sysinfo:", interpretador.qtd_proc_running_sysinfo(interpretador))
    # print("qtd_threads_running:", interpretador.qtd_threads_running(interpretador))
    
    
    
if __name__ == "__main__":
    main ()