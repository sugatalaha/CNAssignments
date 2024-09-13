import socket
from ass1 import crc
import time

divisor="100000100110000010001110110110111"
PORT=8000
rn=0
print("Selective Repeat ARQ")
receiver_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
receiver_socket.connect((socket.gethostname(),PORT))
print("Connected to sender")

try:
    while True:
        data=receiver_socket.recv(1024).decode()
        if not data:
            print("Connection closing...")
            break
        else:
            print("Data received")
            if crc.check_remainder(data,divisor):
                print("Data not corrupted")
                end_index=96+8
                frame_no=int(data[96:end_index],2)
                print(f"Frame number received is {frame_no}")
                print(f"Frame number needed {rn}")
                time.sleep(2.0)
                if rn==frame_no:
                    print("Frame number is correct. Sending acknowledgement...",frame_no)
                    receiver_socket.sendall(("1"+format(rn,"08b")).encode())
                    rn+=1
                else:
                    print("Frame numbers dont match")
                    print("Sending nack ",rn)
                    receiver_socket.sendall(("0"+format(rn,"08b")).encode())
            else:
                print("Frame found corrupted")
                print("Sending nack ",rn)
                nack="0"+format(rn,"08b")
                receiver_socket.sendall(nack.encode())
except Exception as e:
    print("An error occured:",e)
finally:
    receiver_socket.close()