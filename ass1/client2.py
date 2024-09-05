import socket
import random
import time
from checksum import generate_checksum
from crc import encode_data
from time import sleep

def inject_error(text, number):
    if number == 0:
        return text
    text_list = list(text)
    for _ in range(number):
        x = random.randint(0, len(text) - 1)
        text_list[x] = '1' if text_list[x] == '0' else '0'
    return ''.join(text_list)

def inject_burst_error(text, x):
    if x <= 0 or not text:
        return text

    start_index = random.randint(0, len(text) - x)
    text_list = list(text)

    for i in range(x):
        if start_index + i == len(text):
            return
        text_list[start_index + i] = '1' if text_list[start_index + i] == '0' else '0'

    return ''.join(text_list)

def send_data(sock, data):
    try:
        sock.sendall(data.encode())
    except socket.error:
        print("Error sending data!")

def main():
    HOST = "127.0.0.1"
    PORT = 9988
    PKT_SIZE = 16

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except socket.error:
        print("Error connecting to server!")
        return

    key = input("Enter Key for CRC: ")

    num_error_bits = int(input("Enter number of isolated error bits: "))
    burst_error_bits = int(input("Enter size of burst error bits: "))

    random.seed(time.time())

    for _ in range(1000):
        random_size = 20 + random.randint(0, 290)
        enc_text = ''.join(random.choice('01') for _ in range(random_size))

        actual_len = len(enc_text)
        if actual_len % PKT_SIZE != 0:
            enc_text += '0' * (PKT_SIZE - (actual_len % PKT_SIZE))

        chunks = [enc_text[i:i + PKT_SIZE] for i in range(0, len(enc_text), PKT_SIZE)]
        #print(chunks)
        #print("\n")
        checksum = generate_checksum(chunks)
       # print(0)
        sleep(0.005)
        send_data(sock, checksum)
        sleep(0.005)
       # print(1)
        newtext = inject_error(enc_text, num_error_bits)
        newtext = inject_burst_error(newtext, burst_error_bits)

        chunks2 = [newtext[i:i + PKT_SIZE] for i in range(0, len(newtext), PKT_SIZE)]

        for chunk in chunks2:
            sleep(0.005)
            send_data(sock, chunk)
       # print(2)
        send_data(sock, "EOF")

        chunks3 = encode_data(chunks, key)
        temp = ''.join(chunks3)

        final = inject_error(temp, num_error_bits)
        final = inject_burst_error(final, burst_error_bits)

        size = len(chunks3[0])
        chunks4 = [final[i:i + size] for i in range(0, len(final), size)]

        sleep(0.005)
        send_data(sock, key)
        sleep(0.005)
        for chunk in chunks4:
            sleep(0.005)
            send_data(sock, chunk)

        send_data(sock, "EOF")

    sock.close()

if __name__ == "__main__":
    main()
