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

char* read_sys_info(const char* f_path, uint32_t string_size)
{
    // Buffer used store info
    char* info = (char*)calloc(string_size, sizeof(char));
    
    // Opening file
    int file_d = open(f_path, O_RDONLY); // File descriptor
    if (file_d < 0) { 
        perror("r1"); 
        exit(1);
        return "";
    }

    size_t data_size = string_size / 8;
    size_t size = read(file_d, info, data_size);
    info[size] = '\0'; // To be read as string

    // Closing file
    if (close(file_d) < 0) { 
        perror("c1"); 
        exit(1);
        return "";
    } 

    return info;
}

char* version_info()
{
    return read_sys_info("/proc/version", 2048);
}