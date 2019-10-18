'''the server file for the chat application'''

import socket
import select

SOCKET_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET_SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET_SERVER.bind(("127.0.0.1", 8080))
SOCKET_SERVER.listen(10)
SOCKETS = [SOCKET_SERVER]

CLIENTS = {}
ADDRESSES = {}

while True:
    READ_S, WRITE_S, ERROR_S = select.select(SOCKETS, [], [])
    for ITEM in READ_S:
        if ITEM == SOCKET_SERVER:
            CONNECTION, CLIENT_ADDRESS = SOCKET_SERVER.accept()
            USERNAME = CONNECTION.recv(3999).decode("utf-8")
            CLIENTS.update({USERNAME: CLIENT_ADDRESS})
            ADDRESSES.update({CLIENT_ADDRESS: CONNECTION})
            print(f"a new connection from {USERNAME} at {CLIENT_ADDRESS}")
            print(CLIENTS)
            SOCKETS.append(CONNECTION)
        else:
            data = ITEM.recv(5000)
            data_str = data.decode("utf-8")
            if not data:
                ITEM.close()
                SOCKETS.remove(ITEM)
            elif data_str[-3:] == "bye":
                print("swiggity swooty!!")
                ITEM.close()
                SOCKETS.remove(ITEM)
            elif data_str[-7:] == "private":
                private_q = 'Enter "chat" to star a private chat, "message" to send a private message, or "exit" to keep sending to the main chat: '
                private_q = private_q.encode("utf-8")
                ITEM.send(private_q)
                while True: 
                    private_opt = ITEM.recv(5000)
                    private_opt = private_opt.decode("utf-8")
                    if private_opt [-4:] == "chat":
                        new_chat = "new chat"
                        new_chat = new_chat.encode("utf-8")
                        ITEM.send(new_chat)
                        break
                    elif private_opt [-7:] == "message":
                        new_msg = "new msg"
                        new_msg = new_msg.encode("utf-8")
                        ITEM.send(new_msg)
                        break
                    elif private_opt [-4:] == "exit":
                        break
                    else:
                        pvt_warn = "Please enter only 'chat', 'message', or 'exit'."
            else: 
                for X in ADDRESSES:
                    if ADDRESSES[X] == ITEM:
                        pass
                    elif not data:
                        SOCKETS.remove(ITEM)
                    elif data.decode("utf-8") == "bye":
                        print("oopsie")
                        ITEM.close()
                        SOCKETS.remove(ITEM)
                    else:
                        ADDRESSES[X].send(data)
SOCKET_SERVER.close()
