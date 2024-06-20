/****************************************************************************

Linux System Calls
To compile use: cc -fPIC -shared -o sys_call.so sys_call.c

 FLAGS:

-> Open();
    O_RDONLY    // It will Open the file in read-only mode.

SYSTEMCALLS:

    Open();
    Read();
    Close();
    opendir();  // https://linux.die.net/man/3/opendir
    readdir();  // https://linux.die.net/man/3/readdir
    closedir(); // https://linux.die.net/man/3/closedir
 
****************************************************************************/

#include <errno.h> 
#include <fcntl.h> 
#include <stdio.h> 
#include <unistd.h> 
#include <stdint.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <libgen.h>
#include <string.h>

#define VERSION_INFO_SIZE 2 * 1024
#define MEMORY_INFO_SIZE 16 * 1024

extern int errno;

char* read_dir_info(const char* d_path)
{
    DIR *dirp;
    struct dirent *dp;

    if ((dirp = opendir(d_path)) == NULL)
    {
        perror("Cannot open directory");
        exit(1);
    }

    // Used to count the directories
    uint32_t string_dir_size = 0;
    while ((dp = readdir(dirp)) != NULL)
        string_dir_size += strlen(dp->d_name) + 1; // +1 for space or newline

    // Rewind directory stream to read again
    rewinddir(dirp);

    // Allocate memory for the directory names
    char *dir_names = calloc(string_dir_size + 1, sizeof(char)); // +1 for null terminator
    if (dir_names == NULL)
    {
        perror("Cannot allocate memory");
        closedir(dirp);
        exit(1);
    }

    // Read the directory entries again and concatenate them
    while ((dp = readdir(dirp)) != NULL)
    {
        strcat(dir_names, dp->d_name);
        strcat(dir_names, "\n"); // Add a newline or space after each name
    }
    closedir(dirp);

    return dir_names;
}

char* read_sys_info(const char* f_path, uint32_t string_size)
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

char* version_info()
{
    return read_sys_info("/proc/version", VERSION_INFO_SIZE);
}

char* memory_info()
{
    return read_sys_info("/proc/meminfo", MEMORY_INFO_SIZE);
}
