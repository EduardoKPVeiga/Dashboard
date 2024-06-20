import decode

def main():
    #print(list_proc_running())
    #print(decode.memory_info_d())
    #print(proc_memory_usage())
    #print(decode.clk_per_second_d())
    print(decode.cpu_usage_d())

def list_proc_running():
    # Read subdirectories
    process_list = decode.read_dir()
    process_names_list = []

    # Add all process' names
    for proc in process_list:
        process_names_list.append(proc[0][1])

    return process_names_list

def proc_memory_usage():
    process_list = decode.read_dir()
    process_mem_usage_list = []

    # Add all process' names
    for proc in process_list:
        proc_mem = []
        proc_mem.append(proc[0][1])

        # Add only process name and memory usage
        for item in proc:
            if (item[0] == "VmSize"):
                proc_mem.append(decode.remove(item[1], " "))
                break

        process_mem_usage_list.append(proc_mem)
    
    return process_mem_usage_list

if __name__ == "__main__":
    main()