import decode
import time

def list_proc_running_sysinfo():
    # Read subdirectories
    process_list = decode.process_status_d()
    process_names_list = []

    # Add all process' names
    for proc in process_list:
        process_names_list.append(proc[0][1])

    return process_names_list

def cpu_usage_sysinfo():
    cpu_usage_prev = decode.cpu_usage_since_boot_d()
    time.sleep(0.5)
    cpu_usage_actual = decode.cpu_usage_since_boot_d()
    
    cpu_usage = []
 
    # Convert to %
    for i in range(len(cpu_usage_actual)):
        cpu_usage_value = (cpu_usage_actual[i][1] - cpu_usage_prev[i][1]) / (cpu_usage_actual[i][2] - cpu_usage_prev[i][2])
        cpu_usage_value = (1 - cpu_usage_value) * 100
        cpu_usage.append([cpu_usage_actual[i][0], cpu_usage_value])

    return cpu_usage

def proc_info_sysinfo():
    proc_status = decode.process_status_d()

    proc_info = []

    # Extract the information from 'status'
    for proc in proc_status:
        data = []
        for item in proc:
            if item[0] == "Name" or item[0] == "State" or item[0] == "Tgid" or item[0] == "VmSize" or item[0] == "Threads":
                if item[0] == "VmSize":
                    data.append([item[0], decode.remove(item[1], " ")])
                else:
                    data.append([item[0], item[1]])
        proc_info.append(data)

    #[[["Name", "Name1"], ["State", "State1"], ["Tgid", "ID1"], ["VmSize", "VmSize1"], ["Threads", "Threads1"]], ... , [["Name", "NameN"], ["State", "StateN"], ["Tgid", "IDN"], ["VmSize", "VmSizeN"], hreads", "ThreadsN"]]]
    return proc_info

def qtd_proc_running_sysinfo():
    return len(list_proc_running_sysinfo())

def qtd_threads_running():
    total_threads = 0
    proc_info = proc_info_sysinfo()

    # Search for "Thread" atribute
    for proc in proc_info:
        for item in proc:
            if item[0] == "Threads":
                total_threads += int(item[1])

    return total_threads

