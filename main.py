import decode
import system_info as sys_i

def main():
    #print(list_proc_running())
    #print(decode.memory_info_d())
    #print(proc_memory_usage())
    #print(decode.clk_per_second_d())
    print(sys_i.qtd_threads_running())

if __name__ == "__main__":
    main()