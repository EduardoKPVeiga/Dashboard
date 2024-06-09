import ctypes

_sys = ctypes.CDLL("./sys_call.so")

def main():
    global _sys
    _sys.hello()

if __name__ == "__main__":
    main()