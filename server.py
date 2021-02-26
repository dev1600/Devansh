import socket
import threading

#HEADER is used cause the first  message to the server is message of 64 bytes to tell length of 
#actual message
HEADER =64
PORT =5050
SERVER = socket.gethostbyname(socket.gethostname()) #get the ip address of computer  name
#print(SERVER)
ADDR =(SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE ="!DISCONNECT"
#socket.SOCK_STREAM tells the data we are streaming
server =socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Tells socket what type of address we will be accepting
#we have bind this socket with this add by the below line
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    connected =True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                connect=False
        
            print(f"[{addr}] {msg}")
    conn.close()
        
def start():
    server.listen()
    print("[LISTENING] SERVER is listening")
    while True:
        #this line will wait for new  connection to server
        conn ,addr =server.accept()
        #multi thread implementation in python
        thread =threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
        
print("STARTING server is starting....")
start()