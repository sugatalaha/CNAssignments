import socket
from ass2.Sender import framing,channel
import threading
import time

PORT=8000
TIMEOUT=2.0

frame_timers={}

def recv(conn,ret_list):
    try:
        while True:
            ack=conn.recv(1024)
            ack=ack.decode()
            if ack:
                frame_no=int(ack[-8:],2)-1
                print(f"Acknowledgement received {frame_no}")
                ret_list.append(frame_no)
                for key in range(0,frame_no+1):
                    if not frame_timers[frame_no][2]:
                        frame_timers[frame_no][0].cancel()
            else:
                print("No acknowledgement from receiver side")
    except Exception as e:
        print("Error in receiving ack:",e)

def resend_frame_signal(frame_no):
    try:
        print(f"Timeout occured for frame number {frame_no}!")
        frame_timers[frame_no][2]=True
    except Exception as e:
        print("Error during timeout:",e)
def send(m):
    window_size=m
    sn=0
    sf=0
    stored_frames=[]
    ret_list=[]
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
            with open("ass2/data.txt") as f:
                while True:
                    print(f"Window starts at {sf} and ends at {sn}")
                    dataword=f.readline().strip()
                    if(len(dataword)==0):
                        print("No more data to send!")
                        if(sn-sf>=window_size):
                            for _, (t_thread,a_thread,flag) in frame_timers.items():
                                if not flag:
                                    if t_thread.is_alive():
                                        t_thread.join()
                                        t_thread.cancel()
                            if len(ret_list)>0:
                                while sf<ret_list[0]:
                                    sf+=1
                                ret_list.clear()
                            else:
                                for key in frame_timers.keys():
                                    if key>=sf and key<=sn:
                                        print(f"Resending frame {key}")
                                        frame_timers[key][2]=False
                                        frame_timers[key][0]=threading.Timer(TIMEOUT,resend_frame_signal,args=(key,))
                                        frame_timers[key][0].start()
                                        modified_codeword=channel(codeword)
                                        conn.send(modified_codeword.encode())
                        print("All acknowledgments received")
                        break
                    else:
                        if(sn-sf>=window_size):
                            for _, (t_thread,a_thread,flag) in frame_timers.items():
                                if not flag:
                                    if t_thread.is_alive():
                                        t_thread.join()
                            if len(ret_list)>0:
                                while sf<=ret_list[0]:
                                    sf+=1
                                ret_list.clear()
                            else:
                                for key in frame_timers.keys():
                                    if key>=sf and key<=sn:
                                        print(f"Resending frame {key}")
                                        frame_timers[key][2]=False
                                        frame_timers[key][0]=threading.Timer(TIMEOUT,resend_frame_signal,args=(key,))
                                        modified_codeword=channel(codeword)
                                        conn.send(modified_codeword.encode())
                        timer_thread=threading.Timer(TIMEOUT,resend_frame_signal,args=(sn,))
                        ack_thread=threading.Thread(target=recv,args=(conn,ret_list,))
                        timer_thread.daemon=True
                        ack_thread.daemon=True
                        frame_timers[sn]=[timer_thread,ack_thread,False]
                        codeword=framing(dataword,sn)
                        stored_frames.append(codeword)
                        frame_timers[sn][0].start()
                        frame_timers[sn][1].start()
                        print(f"Sending frame {sn}")
                        sn+=1
                        modified_codeword=channel(codeword)
                        conn.send(modified_codeword.encode())

    except Exception as excep:
        print("Error occured while connecting:",excep)
    finally:
        print("Connection closing...")
        sender_socket.close()

if __name__=="__main__":
    m=int(input("Enter the parameter N:"))
    time1=time.time()
    send(m)
    time2=time.time()
    print(f"Time of execution of GoBackN {time2-time1}")