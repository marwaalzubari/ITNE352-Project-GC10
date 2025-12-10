import socket
import threading
import json
SERVER_ADDR=("127.0.0.1",50555)

# function to start the client
def start_client():
     client_socket = socket.socket(family=socket.AF_INET, type= socket.SOCK_STREAM)#create socket

     #connect to the server
     client_socket.connect(SERVER_ADDR)
     print(f"connected to server {SERVER_ADDR}")

     #sent the username to the server
     username=input("Enter your username:")
     client_socket.sendall(username.encode("utf-8"))