def txt_to_bytes(txt):
    return bytes(txt, 'utf-8')

def bytes_to_txt(bytes_):
    for i in range(len(bytes_)):
        bytes_[i] = bytes_[i].encode(encoding='utf-8')

def main():
    txt = "hola mundo"
    bytes_ = [3840405848, 358169534, 534581052, 3295748290]
    bytes01 = bytes_to_txt(bytes_)
    print(bytes01)
    


if __name__ == "__main__":
    main()