def add_binary_strings(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    result = ''
    carry = 0

    for i in range(max_len - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])
        total = bit_a + bit_b + carry
        result = str(total % 2) + result
        carry = total // 2

    if carry:
        result = '1' + result

    return result

def generate_checksum(chunks):
    res = ''
    size = len(chunks[0])

    for chunk in chunks:
        if res:
            res = add_binary_strings(res, chunk)
        else:
            res = chunk

    if len(res) > size:
        overflow = res[:len(res) - size]
        res = res[len(res) - size:]
        res = add_binary_strings(res, overflow)

    res = ''.join('1' if bit == '0' else '0' for bit in res)

    return res

def check_checksum(chunks, checksum):
    res = ''
    size = len(chunks[0])

    for chunk in chunks:
        if chunk:
            if res:
                res = add_binary_strings(res, chunk)
            else:
                res = chunk

    if len(res) > size:
        overflow = res[:len(res) - size]
        res = res[len(res) - size:]
        res = add_binary_strings(res, overflow)

    res = add_binary_strings(res, checksum)

    return all(bit == '1' for bit in res)
