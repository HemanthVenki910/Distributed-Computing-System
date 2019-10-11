import tkinter as tk
import dill as pickle
import socket
from threading import Thread
from tkinter import ttk

name=socket.gethostname()
ip=socket.gethostbyname(name)
port=1234
HEADER_LENGTH=10

class ClientApp(tk.Tk):
    
    def __init__(self,*args,**kwargs):
        #Litreally Every Initial variable required
        self.frames={}
        self.username=""
        self.ip_number=""
        self.port_number=1234
        self.HEADER_SIZE=10
        self.client_socket=""
        
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)
        container.pack(side="top", fill="both", expand=False)
        container.grid_rowconfigure(1,weight=1)
        container.grid_columnconfigure(1,weight=1)
        for f in (LoginPage,DataPage):
            pagename=f.__name__
            frame=f(parent=container,controller=self)
            self.frames[pagename]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_Frame("LoginPage")
    
    def show_Frame(self,pagename):
        frame=self.frames[pagename]
        frame.tkraise()
        
class LoginPage(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        label1=tk.Label(self,text="Enter UserName")
        label1.grid(row=0,column=0)
        self.username=tk.StringVar()
        self.username_entry=tk.Entry(self,textvariable=self.username)
        self.username_entry.grid(row=0,column=1,columnspan=1)
        
        label2=tk.Label(self,text="Enter IP Number")
        label2.grid(row=1,column=0)
        self.ip_number=tk.StringVar()
        self.ip_number_entry=tk.Entry(self,textvariable=self.ip_number)
        self.ip_number_entry.grid(row=1,column=1,columnspan=1)
        
        label3=tk.Label(self,text="Enter Port Number")
        label3.grid(row=2,column=0)
        self.port_number=tk.StringVar()
        self.port_number_entry=tk.Entry(self,textvariable=self.port_number)
        self.port_number_entry.grid(row=2,column=1,columnspan=1)
        
        button1=tk.Button(self,text=" Connect ", command=lambda : self.send_details(),width=9)
        button1.grid(row=1,column=2)
        
        self.msg_list = tk.Listbox(self,width=50,height=2)
        self.msg_list.grid(row=3,column=0,columnspan=2)
    
    def send_details(self):
        if(len(self.username.get())):
            self.msg_list.delete(0,tk.END)
            username=self.username.get()
            if not len(self.ip_number.get()):
                ip_number=socket.gethostname()
                ip_number=socket.gethostbyname(ip_number)
            else:
                ip_number=self.ip_number.get()

            if not len(self.port_number.get()):
                port_number=1234
            else:
                port_number=int(self.port_number.get())
            try:
                self.controller.username=username
                self.controller.ip_number=ip_number
                self.controller.port_number=port_number
                self.controller.show_Frame("DataPage")
                
                datax="Client-Socket".encode("utf-8")
                message_length=f"{len(datax):<{HEADER_LENGTH}}".encode("utf-8")
                
                self.controller.client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.controller.client_socket.connect((ip_number,port_number))
                self.controller.client_socket.send(message_length+datax)
                
            except Exception as e:
                print(e)
                pass
        else:
            message="Enter a User Name"
            self.msg_list.insert(tk.END,message)
        
class DataPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        label1=tk.Label(self,text=f"The Data to Send",height=2)
        label1.grid(row=0,column=0)
        self.entry1_data=tk.StringVar()
        self.entry1=tk.Entry(self,textvariable=self.entry1_data,width=30)
        self.entry1.grid(row=0,column=1)
        
        button1=tk.Button(self,text="Sum of Numbers",command=lambda:self.send_data("Sum"),width=12)
        button1.grid(row=0,column=2)
        
        button2=tk.Button(self,text="Max Number",command=lambda:self.send_data("Maximum"),width=12)
        button2.grid(row=1,column=2)
        
        button3=tk.Button(self,text="Min Number",command=lambda:self.send_data("Minimum"),width=12)
        button3.grid(row=2,column=2)
        
        button4=tk.Button(self,text="Average",command=lambda:self.send_data("Average"),width=12)
        button4.grid(row=3,column=2)
        
        self.list1=tk.Listbox(self,height=6,width=35)
        self.list1.grid(row=2,column=0,columnspan=2,rowspan=6)
        s2=tk.Scrollbar(self,orient='horizontal')
        s2.grid(row=8,column=0,columnspan=2)
        self.list1.configure(xscrollcommand=s2.set)
        s2.configure(command=self.list1.xview)
    
    def receive_data(self):
        while True:
            try:
                message_length=int(self.controller.client_socket.recv(HEADER_LENGTH).strip().decode("utf-8"))
                message=self.controller.client_socket.recv(message_length)
                message=pickle.loads(message)
                message_data=message.processed_data
                self.final_data_processed=message_data
                self.final_data_sent=message.data
                break
            except IOError as e:
                print("Client has Exited",e)
                #if the Client has Exited to make sure that the operations proceed as usual we will have to create a new connection altogether 
                #TODO
                ip_number=self.controller.ip_number
                port_number=self.controller.port_number
                
                self.controller.client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.controller.client_socket.connect((ip_number,port_number))
                
                datax="Client-Socket".encode("utf-8")
                message_length=f"{len(datax):<{HEADER_LENGTH}}".encode("utf-8")
                
                self.controller.client_socket.send(message_length+datax)
                self.controller.client_socket.send(self.message_length+self.datax)
                continue
            except Exception as e:
                print("Unknown Error",e)
                break
    
    def send_data(self,oper):
        ip_number=self.controller.ip_number
        port_number=self.controller.port_number
        print(ip_number,port_number)
        try:
            datax=""
            if(oper=="Sum"):
                datax=Sum_Data(self.entry1_data.get())     #Place Where you are Sending the data
            elif(oper=="Maximum"):
                datax=Maximum(self.entry1_data.get())
            elif(oper=="Minimum"):
                datax=Minimum(self.entry1_data.get())
            elif(oper=="Average"):
                datax=Average(self.entry1_data.get())
            else:
                raise Custom_Error
            self.entry1.delete(0,tk.END)
            self.datax=pickle.dumps(datax)
            self.message_length=f"{len(self.datax):<{HEADER_LENGTH}}".encode("utf-8")
            self.controller.client_socket.send(self.message_length+self.datax)
            recv_thread=Thread(target=self.receive_data)
            recv_thread.start()
            recv_thread.join()
            self.list1.insert(tk.END,f"{self.final_data_sent} > {self.final_data_processed}")

        except socket.error as e:
            print("Socket Error Bruh",e)
            pass
        except Custom_Error as e:
            print(e)
            pass
        except Exception as e:
            print(e)
        
        
class Custom_Error(Exception):
    def __str__(self):
        print("Invalid Input")
    pass
class Sum_Data:
    def __init__(self,data):
        datax=data.split(' ')
        print(datax)
        self.data=[]
        for i in range(len(datax)):
            if datax[i] == '':
                continue
            self.data.append(float(datax[i]))
        print(self.data)
        self.processed_data=""
    
    def function(self,data):
        sumx=0
        for i in data:
            sumx+=i
        return sumx    
    def set_data(self,data):
        self.processed_data=data
    
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return str(f"Function to Perform Sum of Number")

class Maximum:
    def __init__(self,data):
        datax=data.split(' ')
        print(datax)
        self.data=[]
        for i in range(len(datax)):
            if datax[i] == '':
                continue
            self.data.append(float(datax[i]))
        print(self.data)
        self.processed_data=""
    
    def function(self,data):
        maxi=0
        for i in data:
            if i>maxi:
                maxi=i
        return maxi
    def set_data(self,data):
        self.processed_data=data
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return str(f"Function to Perform Maximum of Number")

class Minimum:
    def __init__(self,data):
        datax=data.split(' ')
        print(datax)
        self.data=[]
        for i in range(len(datax)):
            if datax[i] == '':
                continue
            self.data.append(float(datax[i]))
        print(self.data)
        self.processed_data=""
    
    def function(self,data):
        minx=data[0]
        for i in data:
            if(minx>i):
                minx=i
        return minx
    def set_data(self,data):
        self.processed_data=data
    
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return str(f"Function to Perform Minimum of Number")

class Average:
    def __init__(self,data):
        datax=data.split(' ')
        print(datax)
        self.data=[]
        for i in range(len(datax)):
            if datax[i] == '':
                continue
            self.data.append(float(datax[i]))
        print(self.data)
        self.processed_data=""
    
    def function(self,data):
        sumx=0
        for i in data:
            sumx+=i
        average=sumx/len(data)
        return average
    def set_data(self,data):
        self.processed_data=data
    
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return str(f"Function to Perform Average of Number")

if __name__=="__main__":
    app=ClientApp()
    app.title("Computation")
    app.minsize(350,150)
    app.mainloop()
        
            
            
            
        
    
        
        
        
            