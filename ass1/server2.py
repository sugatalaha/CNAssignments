import socket
from checksum import check_checksum
from crc import check_remainder

def main():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.bind(('', 9988))
    sockfd.listen(5)

    print("Waiting for connections...")

    check_sum_err = 0
    crc_err = 0
    flag = False

    while True:
        newsockfd, _ = sockfd.accept()
        print("Connection accepted")
        i = 0

        while True:
            buffer0 = newsockfd.recv(256).decode().strip()
            if not buffer0:
                print("Error receiving checksum or connection closed")
                break

            checksum = buffer0

            chunks = []
            while True:
                buffer = newsockfd.recv(256).decode().strip()
                if not buffer:
                    print("Error receiving message")
                    break

                while buffer:
                    chunk = buffer[:16]
                    buffer = buffer[16:]
                    if chunk == "EOF":
                        break
                    chunks.append(chunk)
                if chunk == "EOF":
                    break

            if check_checksum(chunks, checksum):
                check_sum_err += 1

            buffer2 = newsockfd.recv(256).decode().strip()
            if not buffer2:
                print("Error receiving CRC key or connection closed")
                break

            key = buffer2

            crc_chunks = []
            chunk_size = 16 + len(key) - 1

            while True:
                buffer = newsockfd.recv(256).decode().strip()
                if not buffer:
                    print("Error receiving CRC message")
                    break

                while buffer:
                    chunk = buffer[:chunk_size]
                    buffer = buffer[chunk_size:]
                    if chunk == "EOF":
                        break
                    crc_chunks.append(chunk)
                if chunk == "EOF":
                    break

            if check_remainder(crc_chunks, key):
                crc_err += 1

            if i == 999:
                flag = True
                break
            i += 1

        newsockfd.close()
        if flag:
            break

    sockfd.close()
    print(f"Checksum errors passed: {check_sum_err}")
    print(f"CRC errors passed: {crc_err}")

if __name__ == "__main__":
    main()
