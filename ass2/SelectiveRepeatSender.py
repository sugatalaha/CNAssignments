import socket
import time
import threading
from ass2.Sender import channel, framing

PORT = 8000
frames_sent = []
pending_frames =set()

def recv_ack(conn):
    global pending_frames
    packet = conn.recv(1024).decode().strip()
    if packet:
        if packet[-9] == '1':  # Assuming the 9th bit represents ACK/NACK, check as string
            frame_no = int(packet[-8:], 2)
            print("Acknowledgement received for frame ", frame_no)
            if frame_no in pending_frames:
                pending_frames.remove(frame_no)  # Remove from pending_frames
        else:
            nack_no = int(packet[-8:], 2)
            print("Nack received for frame ", nack_no)
            if nack_no not in pending_frames:
                pending_frames.add(nack_no)  # Add to pending_frames if NACK received

def send(m):
    global pending_frames
    global frames_sent
    try:
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.bind((socket.gethostname(), PORT))
        sender_socket.listen(5)
        print("Sender is listening...")
        conn, conn_address = sender_socket.accept()
        if not conn:
            print("No connection found")
            return
        else:
            print(f"Connection established with {conn_address}")
        
        with open('ass2/data.txt') as f:
            sn = 0  # Next frame number to send
            sf = 0  # Frame number of the first frame in the window
            sw = pow(2, m - 1)  # Size of the sliding window (2^(m-1))
            while True:
                if sn-sf>=sw:
                    while len(pending_frames)>0:
                        print("Pending frames:",pending_frames)
                        for nack_no in pending_frames.copy():
                            if nack_no>=sf and nack_no<=sn:
                                print("Resending frame ", nack_no)
                                modified_frame=channel(frames_sent[nack_no])
                                conn.sendall(modified_frame.encode())
                            recv_ack(conn)
                    sf+=1
                else:
                    dataword=f.readline().strip()
                    if not dataword and len(pending_frames)==0:
                        print("No more data to send")
                        break
                    elif not dataword and len(pending_frames)>0:
                        while len(pending_frames)>0:
                            print("Pending frames:",pending_frames)
                            for nack_no in pending_frames.copy():
                                if nack_no>=sf and nack_no<=sn:
                                    print("Resending frame ", nack_no)
                                    modified_frame=channel(frames_sent[nack_no])
                                    conn.sendall(modified_frame.encode())
                                recv_ack(conn)
                    else:
                        codeword=framing(dataword,sn)
                        print("Sending frame number ",sn)
                        sn+=1
                        frames_sent.append(codeword)
                        modified_codeword=channel(codeword)
                        conn.sendall(modified_codeword.encode())
                        recv_ack(conn)
    except Exception as e:
        print("Error occurred while connecting:", e)
    finally:
        sender_socket.close()


if __name__ == "__main__":
    m = int(input("Enter the parameter m: "))
    send(m)




