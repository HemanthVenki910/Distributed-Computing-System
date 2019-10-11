import dill as pickle
import socket
import threading
from threading import Thread
import errno
import sys
import time 

name=socket.gethostname()
ip=socket.gethostbyname(name)
port=1234
HEADER_LENGTH=10

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,port))
server_socket.listen(5)
sub_server_sockets={}
clients={}
online_servers=[]

modify_list=threading.Lock()

def handle_client(client_socket):
    while True:
        try:
            print("here once again")
            message_length=int((client_socket.recv(HEADER_LENGTH).strip()).decode("utf-8"))
            objectx=client_socket.recv(message_length)
            while True:
                modify_list.acquire()
                if(len(online_servers)>0):
                    server_socket=online_servers.pop(0)
                    modify_list.release()
                    break
                else:
                    pass
                modify_list.release()
                time.sleep(0.5)
            
            objectx_length=f"{len(objectx):<{HEADER_LENGTH}}".encode("utf-8")
            server_socket.send(objectx_length+objectx)
            print("Sent")
            objectx_length=int(server_socket.recv(HEADER_LENGTH).strip().decode("utf-8"))
            objectx=server_socket.recv(objectx_length)
            print("Received")
            objectx_length=f"{len(objectx):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(objectx_length+objectx)
            print("Sent to Client")
            
            modify_list.acquire()
            online_servers.append(server_socket)
            modify_list.release()
            
            print("Reavailable Server")
        except IOError as e:
            if e.errno!=errno.EAGAIN and e.errno!=errno.EWOULDBLOCK:
                print('READING ERROR , Client Must have Ended the Connection',str(e))
                server_socket.close()
                client_socket.close()
                break
        except Exception as e:
            client_socket.close()
            server_socket.close()
            print("Error I am here",e)
            break
        
def accept_incoming_connections():
    while True:
        try:
            socket_x,address=server_socket.accept()
            message_length=int((socket_x.recv(HEADER_LENGTH).strip()).decode("utf-8"))
            socket_type=socket_x.recv(message_length).decode("utf-8")
            if(socket_type=="Server-Socket"):
                print("Server-Socket")
                sub_server_sockets[socket_x]=address
                modify_list.acquire()
                online_servers.append(socket_x)
                modify_list.release()
                continue
            elif(socket_type == "Client-Socket"):
                print("Client-Socket")
                clients[socket_x]=address
                clientx=Thread(target=handle_client,args=(socket_x,))
                clientx.start()
            else:
                print("InValid Type of Connection")
                pass
        except Exception as e:
            print(e)
            continue

while True:
    Server=Thread(target=accept_incoming_connections)
    Server.start()
    Server.join()
    server_socket.close()    