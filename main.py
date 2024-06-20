import decode

def main():
    process_list = decode.read_dir()
    for proc in process_list:
        for item in proc:
            print(item)
        print("\n")

if __name__ == "__main__":
    main()