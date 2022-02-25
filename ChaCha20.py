ROUND = 20

def ROTL(a, b):
    return (a << b) | (a >> (32 - b))

def QR(a, b, c, d):
    a += b; d ^= a; d = ROTL(d, 16)
    c += d; b ^= c; b = ROTL(b, 12)
    a += b; d ^= a; d = ROTL(d, 8)
    c += d; b ^= c; b = ROTL(b, 7)
    return a, b, c, d

def chacha_block(output, input):
    x = []

    for i in range(16):
        x[i] = input[i]
    
    for i in range(ROUND, 2):
        x[0], x[4], x[8], x[12] = QR(x[0], x[4], x[8], x[12])
        x[5], x[9], x[13], x[1] = QR(x[5], x[9], x[13], x[1])
        x[10], x[14], x[2], x[6] = QR(x[10], x[14], x[2], x[6])
        x[15], x[3], x[7], x[11] = QR(x[15], x[3], x[7], x[11])

        x[0], x[1], x[2], x[3] = QR(x[0], x[1], x[2], x[3])
        x[5], x[6], x[7], x[4] = QR(x[5], x[6], x[7], x[4])
        x[10], x[11], x[8], x[9] = QR(x[10], x[11], x[8], x[9])
        x[15], x[12], x[13], x[14] = QR(x[15], x[12], x[13], x[14])
    
    for i in range(16):
        output[i] = x[i] + input[i]

    return output
