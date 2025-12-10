import socket
import threading 
import requests
import json 


SERVER_ADDR=("127.0.0.1",50555)
API_KEY = "ae701edbf7d847d4bb8de291a026194d"



#---- (Top Headlines function for request 1) ----#

def get_top_headlines(limit=15 , country="us"):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}"
    try:
        #send the request with timeout to avoid blocking the server 
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data= response.json()
        # check if the response are valid 
        if data.get("status")!="ok":
            return{"error":"non-ok status","details":data}
        #to limit the number of articles (15)
        articles= data.get("articles",[])[:limit]
        #bulid shortcut for each element 
        short=[]
        for a in articles:
            short.append({
                "source": a.get("source", {}).get("name"),
                "author": a.get("author"),
                "title": a.get("title")  
            })
            return{"status":"ok","totalResults": data.get("totalResults"), "articles": short}
        #to handle errors
    except Exception as e:
        return {"error": "Failed to fetch headlines", "details": str(e)}
    

# function search depanding on keyword for request 2 
def search_news(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": "Failed to fetch headlines", "details": str(e)}

# function to save JSON to file for request 3 
def save_json_for_client(data, client_name, option_id, group_id="GC10"):
    filename = f"{client_name}_{option_id}_{group_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

# function to handle each client 
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    name = conn.recv(1024).decode().strip()
    print(f"[NEW USER] {name} connected.")
    last_result = None
    last_result_brief = None
    
    while True:
        try:
            request = conn.recv(1024).decode().strip()
        except:
            # client closed connection suddenly
            break
        
        if not request:
            break

        if request == "1":
            # top headlines
            news = get_top_headlines()
            brief,full=make_headlines_list(news,limit=15)
            last_result_full=full
            last_result_brief=brief
            
            send_with_len(conn,json.dumps({"list":brief}).encode("utf-8"))
           

            sel_data=recv_with_len(conn)
            if not sel_Data:
                break
            sel=sel_data.decode().strip()
            if sel.lower()=="back":
                continue
            try:
                idx = int(sel) - 1
                details = full[idx]
                send_with_len(conn, json.dumps({"details": details}).encode("utf-8"))
                
                save_json_for_client(details, name, "1")
            except Exception as e:
                send_with_len(conn, json.dumps({"error": str(e)}).encode("utf-8"))
        elif request == "2":
            # search news 
            try:
                keyword = conn.recv(1024).decode()
            except:
                break

            news = search_news(keyword)
            last_result = news
            conn.sendall(json.dumps(news).encode())

        elif request == "3":
            # save as JSON
            if last_result:
                save_json(last_result)
                conn.sendall(b"JSON saved successfully!")
            else:
                conn.sendall(b"No data to save!")

        elif request == "4":
            # send JSON file back
            try:
                with open("saved_news.json", "r", encoding="utf-8") as f:
                    content = f.read()
                conn.sendall(content.encode())
            except:
                conn.sendall(b"No saved JSON found!")

        elif request.lower() == "quit":
            break

        else:
            conn.sendall(b"Invalid request. Choose 1, 2, 3, 4, or quit.")
    
    conn.close()
    print(f"[DISCONNECTED] {name}")



# function to start the server 
def start_server():
    server_socket = socket.socket(family=socket.AF_INET, type= socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDR)
    server_socket.listen(5)
   
    print(f"Server is listening on {SERVER_ADDR}...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  


start_server()

def make_headlines_list(api_json, limit=15):
    items = api_json.get("articles", [])[:limit]
    brief_list = []
    for i, art in enumerate(items, start=1):
        brief_list.append({
            "index": i,
            "source": art.get("source", {}).get("name"),
            "author": art.get("author"),
            "title": art.get("title")
        })
    return brief_list, items  # brief for list, items for full details

def log_request(client_name, request_type, params=None):
    params_str = ", ".join(f"{k}={v}" for k,v in (params or {}).items())
    print(f"[REQUEST] Client={client_name} | Type={request_type} | Params={params_str}")
