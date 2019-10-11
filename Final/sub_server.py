#Sub-Server // Worker-Server

import socket
import dill as pickle
import sys

name=socket.gethostname()
ip= socket.gethostbyname(name)
port=1234
HEADER_LENGTH=10
WORKER_INDEN="Server-Socket".encode("utf-8")
worker_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
worker_socket.connect((ip,port))
worker_length=f"{len(WORKER_INDEN):<{HEADER_LENGTH}}".encode("utf-8")
worker_socket.send(worker_length+WORKER_INDEN)

while True:
    try:
        print("Not Received")
        message_length=int(worker_socket.recv(HEADER_LENGTH).strip().decode("utf-8"))
        print("Received")
        message=worker_socket.recv(message_length)
        messagex=pickle.loads(message)
        print(messagex)
        messagex.processed_data=messagex.function(messagex.data)
        message=pickle.dumps(messagex)
        message_length=f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        print(message_length)
        worker_socket.send(message_length+message)
    except Exception as e:
        print("Server must have ended the connection")
        print(e)
        worker_socket.close()
        sys.exit()
    