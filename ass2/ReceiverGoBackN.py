import socket
from ass1 import crc

divisor="100000100110000010001110110110111"
PORT=8000

print("Go back N ARQ")
receiver_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
receiver_socket.connect((socket.gethostname(),PORT))
print("Connected to sender")
try:
    r_n=0
    while True:
        data=receiver_socket.recv(1024).strip()
        if len(data)==0:
            print("No more data")
            break
        data=data.decode()
        print("Data received")
        if crc.check_remainder(data,divisor):
            print("Data not corrupted")
            end_index=96+8
            frame_no=int(data[96:end_index],2)
            print(f"Frame number received is {frame_no}")
            print(f"Frame number needed {r_n}")
            if frame_no==r_n:
                r_n+=1
                frame_string=format(r_n,"08b")
                print("Sending acknowledgement...")
                receiver_socket.sendall(frame_string.encode())
            else:
                print("Frame numbers dont match. Waiting for retransmission...")
        else:
            print("Frame is corrupted")
except Exception as e:
    print("Error occured while connecting:",e)
finally:
    receiver_socket.close()
        