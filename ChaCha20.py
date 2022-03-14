from conversor import txt_to_bytes, bytes_to_txt

ROUND = 20
CHACHA20K = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

# Chacha20 cipher

# Rotate a 32-bit word left by n bits
def ROTL(a, b):
    return ((a << b) | (a >> (32 - b))) & 0xffffffff


# Quarter round with hex numbers
def QR(a, b, c, d):
    a = a + b & 0xffffffff
    d = ROTL(d ^ a, 16)
    c = c + d & 0xffffffff
    b = ROTL(b ^ c, 12)
    a = a + b & 0xffffffff
    d = ROTL(d ^ a, 8)
    c = c + d & 0xffffffff
    b = ROTL(b ^ c, 7)
    return a, b, c, d

# Quarter round for states
def inner_block(state):
    # Odd round
    state[0], state[4], state[8], state[12] = QR(state[0], state[4], state[8], state[12])
    state[1], state[5], state[9], state[13] = QR(state[1], state[5], state[9], state[13])
    state[2], state[6], state[10], state[14] = QR(state[2], state[6], state[10], state[14])
    state[3], state[7], state[11], state[15] = QR(state[3], state[7], state[11], state[15])
    # Even round
    state[0], state[5], state[10], state[15] = QR(state[0], state[5], state[10], state[15])
    state[1], state[6], state[11], state[12] = QR(state[1], state[6], state[11], state[12])
    state[2], state[7], state[8], state[13] = QR(state[2], state[7], state[8], state[13])
    state[3], state[4], state[9], state[14] = QR(state[3], state[4], state[9], state[14])
    return state

# Chacha20 block
def chacha20_block(S, output=False):
    X = []
    X = S[:]
    for i in range(0, ROUND, 2):
        X = inner_block(X)

    if output:
        print("\n\nEstado final tras las 20 iteraciones:")
        for i in range(16):
            if i == 4 or i == 8 or i == 12:
                print()
            print("{:08x}".format(X[i]), end=" ")

    for i in range(16):
        X[i] = ((X[i] + S[i]) & 0xffffffff)
    return X

def chacha20_encrypt(key, counter, nonce, plaintext, output=False):
    # Initialization
    S = []
    for i in range(4):
        S.append(CHACHA20K[i])
    for i in range(8):
        S.append(key[i])
    S.append(counter)
    for i in range(3):
        S.append(nonce[i])
    # Encryption
    ciphertext = []
    for i in range(0, len(plaintext), 64):
        S = chacha20_block(S, output)
        for j in range(64):
            if i + j >= len(plaintext):
                break
            ciphertext.append((plaintext[i + j] ^ S[j]) & 0xffffffff)
    return ciphertext


def main():

    print("\n\n¿Quieres los valores por defecto? (S/n)")
    default = input()
    if default == "s" or default == "S" or default == "":
        key = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c, 0x13121110, 0x17161514, 0x1b1a1918, 0x1f1e1d1c]
        count = 0x00000001
        nonce = [0x09000000, 0x4a000000, 0x00000000]
    else:
        key = input("\n\nIntroduce la clave en forma de 8 palabras en hexadecimal: ")
        key = key.split(" ")
        if len(key) != 8:
            print("\n\nLa clave debe ser de 256 bits")
            return
        for i in range(8):
            key[i] = key[i].replace(":", "")
            aux = []
            for j in range(8, 0, -2):
                aux.append(key[i][j - 2:j])
            key[i] = int("".join(aux), 16)

        count = input("\n\nIntroduce el contador en forma de 1 palabra en hexadecimal: ")
        count = count.replace(":", "")
        aux = []
        for i in range(8, 0, -2):
            aux.append(count[i - 2:i])
        count = int("".join(aux), 16)

        nonce = input("\n\nIntroduce el nonce en forma de 3 palabras en hexadecimal: ")
        nonce = nonce.split(" ")
        if len(nonce) != 3:
            print("\n\nEl nonce debe ser de 96 bits")
            return
        for i in range(3):
            nonce[i] = nonce[i].replace(":", "")
            aux = []
            for j in range(8, 0, -2):
                aux.append(nonce[i][j - 2:j])
            nonce[i] = int("".join(aux), 16)


    
    
    S = [   CHACHA20K[0], CHACHA20K[1], CHACHA20K[2], CHACHA20K[3],
            key[0], key[1], key[2], key[3],
            key[4], key[5], key[6], key[7],
            count, nonce[0], nonce[1], nonce[2]
        ]
    print("\n\nEstado inicial:")
    for i in range(16):
        if i == 4 or i == 8 or i == 12:
            print()
        print("{:08x}".format(S[i]), end=" ")
    Sol = chacha20_block(S, True)
    print("\n\nSolucion:")
    for i in range(16):
        if i == 4 or i == 8 or i == 12:
            print()
        print("{:08x}".format(Sol[i]), end=" ")
    
    # Input plaintext
    plaintext = input("\n\nIntroduce el texto plano: ")
    # Convert text to bytes in hexadecimal
    plaintext = txt_to_bytes(plaintext)
    # Encrypt
    cipherbytes = chacha20_encrypt(key, count, nonce, plaintext)
    # Convert hexadecimal to text
    ciphertext = ''.join(["{:02x}".format(x) for x in cipherbytes])
    # Print ciphertext in hexadecimal 
    outcipher = ""
    for i in range(0, len(ciphertext) - 8, 8):
        outcipher += ciphertext[i:i+8] + ":"
    outcipher += ciphertext[len(ciphertext) - 8:]
    print("\n\nCifrado:")
    print(outcipher)
    print(cipherbytes)
    # Decrypt
    plainbytes = chacha20_encrypt(key, count, nonce, cipherbytes)
    # Convert bytes in hexadecimal
    plaintext = bytes_to_txt(plainbytes)
    # Convert hexadecimal to text
    # Print plaintext
    print("\n\nTexto plano:")
    print(plaintext)
    print(plainbytes)

if __name__ == "__main__":
    main()