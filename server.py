import socket
import threading 
SERVER_ADDR=("127.0.0.1",50555)
server_socket=socket.socket(family=socket.AF_INET,type= socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)
server_socket.listen(5)
print(f"Server is listening on {SERVER_ADDR}...")

# function to handle each client 
def handle_client(conn, addr):
    name = conn.recv(1024).decode()
    print(f"[NEW USER] {name} connected.")
    
    while True:
    request = conn.recv(1024).decode()

    if request == "1":
        # get top headlines
    elif request == "2":
        # search news
    elif request == "3":
        # save as JSON
    elif request == "4":
        # send JSON file back
    elif request == "quit":
        break

        
            
    


    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"[{addr}] {data.decode('ascii')}")
        conn.sendall(b"Message received")

    conn.close()
    print(f"[DISCONNECTED] {addr}")
    
    #loop accept multi clients and make a thread for each one   
while True:
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
