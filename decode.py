import ctypes

global _sys
_sys = ctypes.CDLL("./sys_call.so")

_sys.read_sys_info.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
_sys.read_sys_info.restype = ctypes.c_char_p

_sys.read_dir_info.restype = ctypes.c_char_p
_sys.read_dir_info.argtypes = [ctypes.c_char_p]

def remove(string, char):
    return string.replace(char, "")

def memory_info_d():
    result = _sys.read_sys_info("/proc/meminfo", 16 * 1024)
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

def read_dir():
    result = _sys.read_dir_info("/proc/".encode('utf-8'))
    
    result_v = []
    result_string = ""
    result_v_process = []

    result_string = result.decode('utf-8')
    result_v = result_string.split("\n")

    # Returns only process IDs
    for item in result_v:
        if item.isnumeric() == True:
            result_v_process.append(item)

    # Search for process name
    return read_process_names(result_v_process)

def read_process_names(list_proc: list):
    result_string = ""
    process = []
    path = "/proc/"

    for proc in list_proc:
        result = _sys.read_sys_info((path + proc + "/status").encode('utf-8'), (16 * 1024))
        result_string = result.decode('utf-8')

        # List with the information of a single process
        process_list_items = result_string.split("\n")

        # Matrix with the information of a single process
        process_matrix_items = []

        for process_item in process_list_items:
            # Split only in the first occurrence
            process_matrix_items.append(remove(process_item, "\t").split(":", 1)) # Because some names may have ':' in them

        process.append(process_matrix_items)

    return process