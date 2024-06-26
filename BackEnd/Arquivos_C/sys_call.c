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
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <pwd.h>
#include <grp.h>
#include <time.h>

// extern int errno;

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

uint64_t clk_per_second()
{
    return (uint64_t)sysconf(_SC_CLK_TCK);
}

void format_permissions(mode_t mode, char *str) {
    str[0] = (S_ISDIR(mode)) ? 'd' : '-';
    str[1] = (mode & S_IRUSR) ? 'r' : '-';
    str[2] = (mode & S_IWUSR) ? 'w' : '-';
    str[3] = (mode & S_IXUSR) ? 'x' : '-';
    str[4] = (mode & S_IRGRP) ? 'r' : '-';
    str[5] = (mode & S_IWGRP) ? 'w' : '-';
    str[6] = (mode & S_IXGRP) ? 'x' : '-';
    str[7] = (mode & S_IROTH) ? 'r' : '-';
    str[8] = (mode & S_IWOTH) ? 'w' : '-';
    str[9] = (mode & S_IXOTH) ? 'x' : '-';
    str[10] = '\0';
}

char* read_shell_info(const char* directory, size_t string_size) {
    DIR *dir;
    struct dirent *entry;
    struct stat file_stat;
    struct passwd *pw;
    struct group *gr;
    char timebuf[64];
    char perm[11];
    char *output = (char*)malloc(string_size);
    if (output == NULL) {
        perror("malloc failed");
        return NULL;
    }
    memset(output, 0, string_size);

    dir = opendir(directory);
    if (dir == NULL) {
        perror("opendir failed");
        free(output);
        return NULL;
    }

    size_t total_read = 0;
    while ((entry = readdir(dir)) != NULL) {
        char filepath[1024];
        snprintf(filepath, sizeof(filepath), "%s/%s", directory, entry->d_name);

        if (stat(filepath, &file_stat) == -1) {
            perror("stat failed");
            continue;
        }

        format_permissions(file_stat.st_mode, perm);
        pw = getpwuid(file_stat.st_uid);
        gr = getgrgid(file_stat.st_gid);
        strftime(timebuf, sizeof(timebuf), "%b %d %H:%M", localtime(&file_stat.st_mtime));

        char line[1024];
        int len = snprintf(line, sizeof(line), "%s %lu %s %s %5ld %s %s\n",
                           perm, file_stat.st_nlink, pw->pw_name, gr->gr_name,
                           file_stat.st_size, timebuf, entry->d_name);

        if (total_read + len >= string_size) {
            break;
        }

        strcat(output, line);
        total_read += len;
    }

    closedir(dir);
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
    return read_shell_info(comand, 4098);
}

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


// int main(){
//     printf("%s", version_info());
//     return 0;
// }