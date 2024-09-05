import socket
import random
import checksum,crc

PORT=8000
DIVISOR=100010011

sender_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sender_socket.bind((socket.gethostname(),PORT))
sender_socket.listen(5)
print("Sender is listening...")
conn,conn_address=sender_socket.accept()
if conn:
    print(f"Sender connected to {conn_address}")
    for i in range(1000):
        number_of_errors=random.randint()
        with open("ass1/data.txt") as f:
            dataword=f.read(1024)
            check_sum=checksum.generate_checksum(4)
            crc_remainder=crc.mod2div(dataword,DIVISOR)
            datawordcrc=dataword
            dataword+=check_sum
            datawordcrc+=crc_remainder