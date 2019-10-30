import dill as pickle
import socket
import threading
from threading import Thread
import errno
import sys
import time 
import copy

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
                if(len(online_servers)>1):
                    server_socket1=online_servers.pop(0)
                    server_socket2=online_servers.pop(0)
                    modify_list.release()
                    break
                else:
                    pass
                modify_list.release()
                time.sleep(0.5)
            
            object_decode=pickle.loads(objectx)
            object_decode1=copy.deepcopy(object_decode)
            object_decode2=copy.deepcopy(object_decode)
            print(object_decode)
            indexx=len(object_decode.data)
            
            object_decode1.data=object_decode.data[0:int(indexx/2)]
            object_decode2.data=object_decode.data[int(indexx/2):indexx]
            
            print(object_decode1.data,object_decode1)
            print(object_decode2.data,object_decode2)
            
            objectx1=pickle.dumps(object_decode1)
            objectx2=pickle.dumps(object_decode2)
            
            objectx_length=f"{len(objectx):<{HEADER_LENGTH}}".encode("utf-8")
            
            objectx1_length=f"{len(objectx1):<{HEADER_LENGTH}}".encode("utf-8")
            objectx2_length=f"{len(objectx2):<{HEADER_LENGTH}}".encode("utf-8")
            
            server_socket1.send(objectx1_length+objectx1)
            server_socket2.send(objectx2_length+objectx2)
            print("Sent")
            
            
            objectx1_length=int(server_socket1.recv(HEADER_LENGTH).strip().decode("utf-8"))
            objectx1=server_socket1.recv(objectx1_length)
            objectx1=pickle.loads(objectx1)
            print("Here")
            print(objectx1)
            
            objectx2_length=int(server_socket2.recv(HEADER_LENGTH).strip().decode("utf-8"))
            print("Here1")
            print(objectx2_length)
            objectx2=server_socket2.recv(objectx2_length)
            print("Here2")
            objectx2=pickle.loads(objectx2)
            print("Received")
            
            #Combine Function 
            object_decode.data=[]
            object_decode.data.append(objectx1.processed_data)
            object_decode.data.append(objectx2.processed_data)
            
            object_decode.processed_data=object_decode.function(object_decode.data)
            objectx=pickle.dumps(object_decode)
            objectx_length=f"{len(objectx):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(objectx_length+objectx)
            print("Sent to Client")
            
            modify_list.acquire()
            online_servers.append(server_socket1)
            online_servers.append(server_socket2)
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