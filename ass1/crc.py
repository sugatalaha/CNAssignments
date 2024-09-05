def xor_operation(a, b):
    return ''.join('0' if a[i] == b[i] else '1' for i in range(1, len(b)))

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor_operation(divisor, tmp) + dividend[pick]
        else:
            tmp = xor_operation('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor_operation(divisor, tmp)
    else:
        tmp = xor_operation('0' * pick, tmp)

    return tmp

def encode_data(chunks, key):
    l_key = len(key)
    enc_chunks = []

    for data in chunks:
        appended_data = data + '0' * (l_key - 1)
        remainder = mod2div(appended_data, key)
        codeword = data + remainder
        enc_chunks.append(codeword)

    return enc_chunks

def check_remainder(data, key):
    l_key = len(key)
    remainder = mod2div(data, key)
    if '1' in remainder:
        return False

    return True
