import ctypes

_sys = ctypes.CDLL("./sys_call.so")
_sys.version_info.restype = ctypes.c_char_p;

def main():
    global _sys
    var = _sys.version_info()
    print("version info: ", var);

if __name__ == "__main__":
    main()