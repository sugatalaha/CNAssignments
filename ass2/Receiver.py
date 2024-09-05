import socket
from ass1.crc import *
PORT=8000
divisor="100000100110000010001110110110111"
receiver_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    receiver_socket.connect((socket.gethostname(),8000))
    print("Connection established with sender...")
    while True:
        data=receiver_socket.recv(1024)
        data=data.strip()
        if len(data)>0:
            data=data.decode()#[2:-1]
            print("Data received")
            if check_remainder(data,divisor):
                last_index=96+8
                frame_seq_no=data[96:last_index]
                print("Frame received:",int(frame_seq_no,2))
                print("Correct data received. Sending acknowledgement...")
                receiver_socket.sendall(frame_seq_no.encode())
            else:
                print("Data discarded")
                print("Waiting for retransmission...")
        else:
            print("No more data! Connection closing...")
            receiver_socket.close()
except:
    print("Connection refused")
finally:
    receiver_socket.close()
