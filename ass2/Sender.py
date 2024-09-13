import uuid
import random
import time
import socket
import threading
from ass1.crc import *
from ass1.ErrorInjection import *

divisor = "100000100110000010001110110110111"
is_timeout_occured = False
PORT = 8000

def framing(data, i):
    source_mac_address = bin(uuid.getnode())[2:].zfill(48)
    dest_mac_address = bin(uuid.getnode())[2:].zfill(48)
    frame_seq_no = format(i, "08b")
    header = source_mac_address + dest_mac_address + frame_seq_no
    modified_data = header + data + "0" * (len(divisor) - 1)
    trailer = mod2div(modified_data, divisor)
    final_frame = header + data + trailer
    return final_frame

def does_nothing():
    pass

def channel(codeword):
    number_of_errors = 0
    if random.randint(0,1):
        number_of_errors=random.randint(1,len(codeword))
    modified_codeword = insertError(codeword,number_of_errors)
    interval = random.uniform(0, 3)
    time.sleep(interval)
    return modified_codeword

def wait_for_ack(client_socket,ret_list):
    try:
        # Wait for ACK frame
        time.sleep(1)
        ack_data = client_socket.recv(1024).decode()  # Buffer size is 1024 bytes
        if ack_data:
            print("Acknowledgement received")
            ret_list.append(True)
    except socket.timeout:
        print(f"Timeout waiting for ACK for Frame")
    except ConnectionAbortedError:
        print("Connection was closed while waiting for ACK.")
    except OSError as e:
        print(f"Error receiving ACK: {e}")

def corrupted(frame):
    return int(mod2div(frame, divisor), 2) != 0

def send():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sender_socket.bind((socket.gethostname(), PORT))
        sender_socket.listen(5)
        print("Sender is listening...")
        global client_socket
        client_socket, client_address = sender_socket.accept()
        return_list=[]
        print(f'Connection established with address {client_address}')
        with open('ass2/data.txt') as f:
            i = 0
            while True:
                print("Outer loop running...")
                data = f.readline()
                data=data.strip()
                if len(data)==0:
                    break
                print("Data to be sent:",data)
                data = data.strip()
                codeword = framing(data, i)
                print("Sending Frame number:", i)
                while True:
                    print("Inner loop running...")
                    timer = threading.Timer(5.0,does_nothing)
                    timer.start()
                    timer.deamon=True
                    modified_codeword = channel(codeword)
                    client_socket.sendall(modified_codeword.encode())
                    try:
                        # acknowledgement = client_socket.recv(1024).decode()
                        can_break_loop=False
                        ack_thread = threading.Thread(target=wait_for_ack,args=(client_socket,return_list,))
                        ack_thread.daemon=True
                        ack_thread.start()
                        # Wait for the ACK thread to complete or timeout
                        ack_thread.join(timeout=2)
                        if(len(return_list)>0):
                            can_break_loop=return_list[0]
                        if can_break_loop:
                            timer.cancel()
                            return_list.clear()
                            i+=1
                            break
                        print("Timer expired! Resending Data frame:",i)
                    except socket.error as e:
                        print(f"Socket error: {e}")                    

    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        timer.join(timeout=2)
        ack_thread.join(timeout=2)
            
        print("Closing connection...")
        sender_socket.close()

if __name__ == "__main__":
    send()
