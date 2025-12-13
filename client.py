import socket
import threading
import json

SERVER_ADDR=("127.0.0.1",50555)
BUF_SIZE = 4096 # larger than the client because is recieves bigger data from the server 

# parameters from table 2 in the document
countries = ["au","ca","jp","ae","sa","kr","us","ma"]
languages = ["ar","en"]
categories = ["business","general","health","science","sports","technology"]

"""""""""""""""""""""""""""menu"""""""""""""""""""""""""""

# display the main menu options
def main_menu():
     print("\t \t \t Main Menu") 
     print("1- Search headlines ") 
     print("2- List of sources ") 
     print("3- Quit ") 

# display the submenu of 1- Search headlines
def headlines_menu():
     print("\t \t \t Headlines Menu")
     print("1.1- Search for keywords ")
     print("1.2- Search by category ") 
     print("1.3- Search by country ")
     print("1.4- List all new headlines ")
     print("1.5- Back to the main menu ")

# display the submenu of 2- List of sources
def sources_menu():
     print("\t \t \t Sources Menu")
     print("2.1- Search by category ")
     print("2.2- Search by country ") 
     print("2.3- Search by language ")
     print("2.4- List all ")
     print("2.5- Back to the main menu ")

"""""""""""""""""""""""""""receiving functions"""""""""""""""""""""""""""

#receive a text message from the server
def recv_text(socket):
    return socket.recv(BUF_SIZE).decoode("utf-8",errors="replace").strip()

#receive json data from the server and convert it to object understood in python
def recv_json(socket): 
     data= socket.recv(BUF_SIZE).decode("utf-8",errors="replace")
     return json.loads(data)

"""""""""""""""""""""""""""displaying functions"""""""""""""""""""""""""""

#display list of headlines
def display_headlines_list(item):
     print("\t \t \t Headlines list")
     for i, item in enumerate(item):
          

# function to start the client
def start_client():
     client_socket = socket.socket(family=socket.AF_INET, type= socket.SOCK_STREAM)#create socket

     #connect to the server
     client_socket.connect(SERVER_ADDR)
     print(f"connected to server {SERVER_ADDR}")

     #sent the username to the server
     username=input("Enter your username:")
     client_socket.sendall(username.encode("utf-8"))
