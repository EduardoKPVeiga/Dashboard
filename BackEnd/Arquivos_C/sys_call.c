/****************************************************************************

Linux System Calls
To compile use: cc -fPIC -shared -o sys_call.so sys_call.c

 FLAGS:

-> Open();
    O_RDONLY    // It will Open the file in read-only mode.
 
****************************************************************************/

#include <errno.h> 
#include <fcntl.h> 
#include <stdio.h> 
#include <unistd.h> 
#include <stdint.h>
#include <stdlib.h>

extern int errno;

char* read_sys_info(const char* f_path, uint32_t string_size) //read_files_info
{
    // Buffer used store info
    char* info = (char*)calloc(string_size, sizeof(char));
    
    // Opening file
    int file_d = open(f_path, O_RDONLY); // File descriptor
    if (file_d < 0) { 
        perror("r1"); // Message error print
        exit(1); // Program ended with error (return)
    }

    size_t data_size = string_size / 8;
    size_t size = read(file_d, info, data_size);
    info[size] = '\0'; // To be read as string

    // Closing file
    if (close(file_d) < 0) { 
        perror("c1"); 
        exit(1);
    } 

    return info;
}

char* read_shell_info(const char* f_path, uint32_t string_size)
{
    // Buffer usado para armazenar a saída do comando
    char* output = (char*)calloc(string_size, sizeof(char));
    if (output == NULL) {
        perror("calloc");
        exit(EXIT_FAILURE);
    }

    // Abrindo um pipe para executar o comando shell
    FILE* pipe = popen(f_path, "r");
    if (pipe == NULL) {
        perror("popen");
        exit(EXIT_FAILURE);
    }

    // Lendo a saída do comando a partir do pipe
    size_t total_bytes_read = 0;
    size_t bytes_read;
    while ((bytes_read = fread(output + total_bytes_read, sizeof(char), string_size - total_bytes_read - 1, pipe)) > 0) {
        total_bytes_read += bytes_read;
        if (total_bytes_read >= string_size - 1) {
            // Se chegamos ao limite do buffer, interrompemos a leitura
            break;
        }
    }

    // Adicionando um terminador nulo ao final da saída
    output[total_bytes_read] = '\0';

    // Fechando o pipe
    if (pclose(pipe) == -1) {
        perror("pclose");
        exit(EXIT_FAILURE);
    }

    return output;

}

char* version_info()
{
    return read_sys_info("/proc/version", 2048);
}

char* memory_info()
{
    return read_sys_info("/proc/meminfo", 4098);
}

char* directory_info(char* comand)
{
    printf("teste:%s", comand);
    return read_shell_info(comand, 4098);
}

// int main (){
//     printf("%s", directory_info("/bin/ls -lh"));
//     return 0;
// }
