import socket
from ass2.Sender import framing,channel,divisor,does_nothing
import threading
import time

PORT=8000

receive_event=threading.Event()
stop_event=threading.Event()

def received(ack_received,sn,sf):
    print("Acknowledgement array status:")
    for i in range(sf,sn):
        print(i,ack_received[i])
        if not ack_received[i]:
            return False
    return True

def wait_for_ack(conn,ack_received):
    try:
        while not stop_event.is_set():
            receive_event.wait()
            ack=conn.recv(1024)
            ack=ack.decode()
            if ack:
                frame_no=int(ack[-8:],2)-1
                print(f"Acknowledgement received {frame_no}")
                ack_received[frame_no]=1
            else:
                print("No acknowledgement from receiver side")
    except Exception as e:
        print("Error in receiving ack:",e)

def send(m):
    window_size=pow(2,m)-1
    sn=0
    sf=0
    stored_frames=[]
    ack_received=[0]*(100*window_size)
    sender_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender_socket.bind((socket.gethostname(),PORT))
    try:
        sender_socket.listen(5)
        print("Sender is listening...")
        conn,conn_address=sender_socket.accept()
        if not conn:
            print("No connection can be established")
        else:
            print(f"Connection established with {conn_address}")
            ack_thread=threading.Thread(target=wait_for_ack,args=(conn,ack_received,))
            ack_thread.daemon=True
            ack_thread.start()
            receive_event.set()
            with open("ass2/data.txt") as f:
                while True:
                    if sn-sf>=window_size :
                        print("Window size full")
                        while True:
                            stop_event.set()
                            if received(ack_received,sn,sf):
                                print("All frames in window received")
                                break
                            print(f"Time out occured! Resending frames from {sf} to {sn-1}")
                            temp=sf
                            while temp<sn:
                                stop_event.clear()
                                time.sleep(2.0)
                                stop_event.set()
                                frame=stored_frames[temp]
                                modified_codeword=channel(frame)
                                conn.sendall(modified_codeword.encode())
                                print(f"Sent frame {temp}")
                                temp+=1
                            stop_event.clear()
                            time.sleep(6.0)
                        sf+=1
                        stop_event.clear()
                    dataword=f.readline().strip()
                    if len(dataword)==0:
                        print("All data sending complete")
                        break
                    codeword=framing(dataword,sn)
                    stored_frames.append(codeword)
                    sn+=1
                    modified_codeword=channel(codeword)
                    conn.sendall(modified_codeword.encode())
    except Exception as e:
        print("Error occured while connecting:",e)
    finally:
        print("Connection closing...")
        sender_socket.close()

if __name__=="__main__":
    m=int(input("Enter the parameter m:"))
    send(m)