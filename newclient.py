'''The client side python file of this chat application'''
import socket
import sys
import threading
import os

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 8080
NAME = input("Select a username: ")

CLIENT_SOCKET_ADDRESS = (HOST, PORT)
CLIENT_SOCKET.connect(CLIENT_SOCKET_ADDRESS)
print("Welcome to the chat, "+NAME+"!")
SERVER_INTRO = NAME.encode("utf-8")
CLIENT_SOCKET.send(SERVER_INTRO)
SOCKETS = [CLIENT_SOCKET]


def listen_thread():
    '''function listens listens to the server for incoming message'''
    msg_in = CLIENT_SOCKET.recv(1024)
    if not msg_in:
        print("truth is we out here")
        sys.exit()
    else:
        msg_in = msg_in.decode("utf-8")
        print(msg_in)

def write_thread():
    '''function checks for client input and sends it to the server'''
    msg_out = input()
    if msg_out == "private":
        os.system("start python private.py")
    else:
        msg_out = NAME+": "+input(NAME+": ")
        msg_out = msg_out.encode("utf-8")
        CLIENT_SOCKET.send(msg_out)
        sys.exit()

while True:
    try:
        X = threading.Thread(target=write_thread)
        X.daemon = True
        X.start()
        Y = threading.Thread(target=listen_thread)
        Y.daemon = True
        Y.start()
        X.join(.5)
        Y.join(.5)
    except socket.timeout:
        pass

CLIENT_SOCKET.close()
