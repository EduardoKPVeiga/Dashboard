import ctypes
import time

global _sys
_sys = ctypes.CDLL("./sys_call.so")

_sys.read_sys_info.restype = ctypes.c_char_p
_sys.read_sys_info.argtypes = [ctypes.c_char_p, ctypes.c_uint32]

_sys.read_dir_info.restype = ctypes.c_char_p
_sys.read_dir_info.argtypes = [ctypes.c_char_p]

_sys.clk_per_second.restype = ctypes.c_uint64

def clk_per_second_d():
    return _sys.clk_per_second()

def remove(string, char):
    return string.replace(char, "")

def memory_info_d():
    result = _sys.read_sys_info("/proc/meminfo".encode('utf-8'), (16 * 1024))
    result_string = result.decode('utf-8')
    result_v = result_string.split("\n")
    result_m = []

    for line in result_v:
        line = remove(line, " ")
        result_m.append(line.split(":"))

    return result_m

def version_info_d():
    result = _sys.read_sys_info("/proc/version", 2 * 1024)
    result_string = result.decode('utf-8')
    return result_string

def read_dir_d():
    result = (_sys.read_dir_info("/proc/".encode('utf-8'))).decode('utf-8')
    
    result_v = []
    result_v_process = []

    result_v = result.split("\n")

    # Returns only process IDs
    for item in result_v:
        if item.isnumeric() == True:
            result_v_process.append(item)

    # Search for process name
    return process_names_d(result_v_process)

def process_names_d(list_proc: list):
    result = ""
    process = []
    path = "/proc/"

    for proc in list_proc:
        result = (_sys.read_sys_info((path + proc + "/status").encode('utf-8'), (16 * 1024))).decode('utf-8')

        # List with the information of a single process
        process_list_items = result.split("\n")

        # Matrix with the information of a single process
        process_matrix_items = []

        for process_item in process_list_items:
            # Split only in the first occurrence
            process_matrix_items.append(remove(process_item, "\t").split(":", 1)) # Because some names may have ':' in them

        process.append(process_matrix_items)

    return process

def cpu_usage_d():
    cpu_usage_prev = cpu_usage_since_boot_d()
    time.sleep(0.5)
    cpu_usage_actual = cpu_usage_since_boot_d()
    
    cpu_usage = []

    for i in range(len(cpu_usage_actual)):
        cpu_usage_value = (cpu_usage_actual[i][1] - cpu_usage_prev[i][1]) / (cpu_usage_actual[i][2] - cpu_usage_prev[i][2])
        cpu_usage_value = (1 - cpu_usage_value) * 100
        cpu_usage.append([cpu_usage_actual[i][0], cpu_usage_value])

    return cpu_usage

def cpu_usage_since_boot_d():
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