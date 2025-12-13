import socket
import json

SERVER_ADDR=("127.0.0.1",50555)
BUF_SIZE = 4096 # larger because is recieves bigger data from the server 

# parameters from table 2 in the document
countries = ["au","ca","jp","ae","sa","kr","us","ma"]
languages = ["ar","en"]
categories = ["business","general","health","science","sports","technology"]

"""menu"""

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

"""receiving functions"""

#receive a text message from the server
def recv_text(sockt):
    return sockt.recv(BUF_SIZE).decode("utf-8",errors="replace").strip()

#receive json data from the server and convert it to object understood in python
def recv_json(sockt): 
     data= sockt.recv(BUF_SIZE).decode("utf-8",errors="replace")
     return json.loads(data)

"""displaying functions"""
"""
headline
"""
#display list of headlines
def display_all_headlines(item):
     print("\t \t \t Headlines lists")
     i=0
     for j in item:
          print(f"{i}) Source: {j['source']} Author: {j['author']}")
          print(f"   Title : {j['title']}")
          i += 1
     print()

#display a detailed entry of selected headline
def display_specific_headline(item):
     print("\t \t \t Headline list")
     print(f"Source       : {item['source']}")
     print(f"Author       : {item['author']}")
     print(f"Title        : {item['title']}")
     print(f"URL          : {item['url']}")
     print(f"Description  : {item['description']}")
     print(f"Publish date : {item['publish_date']}")
     print(f"Publish time : {item['publish_time']}")
     print("\t \t \t New entry")

"""
source
"""
#display list of sources
def display_all_sources(item):
     print("\t \t \t sources lists")
     i=0
     for j in item:
          print(f"{i}) {j['name']}")
          i += 1
     print()

#display a detailed entry of selected source
def display_specific_source(item):
     print("\t \t \t Source list")
     print(f"Name        : {item['name']}")
     print(f"Country     : {item['country']}")
     print(f"Description : {item['description']}")
     print(f"URL         : {item['url']}")
     print(f"Category    : {item['category']}")
     print(f"Language    : {item['language']}")
     print("\t \t \t New entry")


# function to start the client
def start_client():
     client_socket = socket.socket(family=socket.AF_INET, type= socket.SOCK_STREAM)#create socket

     #connect to the server
     client_socket.connect(SERVER_ADDR)
     print(f"connected to server {SERVER_ADDR}")

     #sent the username to the server
     username=input("Enter your username:")
     client_socket.sendall(username.encode("utf-8"))
