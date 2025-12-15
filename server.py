import socket
import threading
import requests
import json
from datetime import datetime


SERVER_ADDR = ("127.0.0.1", 50555)
API_KEY = "ae701edbf7d847d4bb8de291a026194d"
GROUP_ID = "GC10"  


#  function to log requests on server screen
def log_request(client_name, option, params=None):
    print("\n[REQUEST]")
    print(f" Client : {client_name}")
    print(f" Option : {option}")
    if params:
        print(f" Params : {params}")
    print("-----------------------------------")


#  function to save full JSON API response
def save_json(client_name, option, data):
    filename = f"{client_name}_{option}_{GROUP_ID}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"[Saved JSON] {filename}")


#####################################(Option 1 – Headlines)#######################################

def limit_results(articles):
    return articles[:15] if len(articles) > 15 else articles


def build_brief_list(articles):
    brief = []
    for a in articles:
        brief.append({
            "source": a["source"]["name"],
            "author": a.get("author", "N/A"),
            "title": a.get("title", "No title")
        })
    return brief


def build_details(article):
    if article.get("publishedAt"):
        dt = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
        publish_date = dt.date().isoformat()
        publish_time = dt.time().isoformat(timespec='seconds')
    else:
        publish_date = "N/A"
        publish_time = "N/A"

    return {
        "source": article["source"]["name"],
        "author": article.get("author", "N/A"),
        "title": article.get("title", "N/A"),
        "url": article.get("url", "N/A"),
        "description": article.get("description", "N/A"),
        "publish_date": publish_date,
        "publish_time": publish_time
    }


def search_by_keyword(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = limit_results(data.get("articles", []))
    return {
        "data": data,  # >>> ADD (needed for saving)
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def search_by_category(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = limit_results(data.get("articles", []))
    return {
        "data": data,
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def search_by_country(country):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = limit_results(data.get("articles", []))
    return {
        "data": data,
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def list_all_headlines():
    url = f"https://newsapi.org/v2/top-headlines?apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = limit_results(data.get("articles", []))
    return {
        "data": data,
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def get_details(full_articles, index):
    if index < 0 or index >= len(full_articles):
        return None
    return build_details(full_articles[index])


####################################################(Option 2 – Sources)####################################################

def limit_sources(sources):
    return sources[:15] if len(sources) > 15 else sources


def build_sources_brief_list(sources):
    brief = []
    for s in sources:
        brief.append({
            "name": s.get("name", "N/A")
        })
    return brief


def build_sources_details(source):
    return {
        "name": source.get("name", "N/A"),
        "country": source.get("country", "N/A"),
        "description": source.get("description", "N/A"),
        "url": source.get("url", "N/A"),
        "category": source.get("category", "N/A"),
        "language": source.get("language", "N/A")
    }


def sources_by_category(category):
    url = f"https://newsapi.org/v2/top-headlines/sources?category={category}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))
    return {
        "data": data,
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


def sources_by_country(country):
    url = f"https://newsapi.org/v2/top-headlines/sources?country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))
    return {
        "data": data,
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


def sources_by_language(language):
    url = f"https://newsapi.org/v2/top-headlines/sources?language={language}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))
    return {
        "data": data,
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


def list_all_sources():
    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))
    return {
        "data": data,
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


########################################## (handle_client) #################################################

#handle client connection and process all menu options 
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] client connected from  {addr}")

    # receive client name
    client_name = conn.recv(1024).decode().strip()
    print(f"[Client Name] {client_name}")

    while True:
        main_option = conn.recv(1024).decode().strip()
        if not main_option:
            break

        # -------------------- Option 1 ------------------------
        if main_option == "1":
            conn.send("HEADLINES_MENU".encode())

            while True:
                sub_option = conn.recv(1024).decode().strip()
                if not sub_option:
                    break

                # 1.1 Search by keyword
                if sub_option == "1.1":
                    conn.send("SEND_KEYWORD".encode())
                    keyword = conn.recv(1024).decode().strip()

                    log_request(client_name, "1.1 Headlines Keyword", {"keyword": keyword})

                    results = search_by_keyword(keyword)
                    save_json(client_name, "1.1", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())


                # 1.2 Search by category
                elif sub_option == "1.2":
                    conn.send("SEND_CATEGORY".encode())
                    category = conn.recv(1024).decode().strip()

                    log_request(client_name, "1.2 Headlines Category", {"category": category})

                    results = search_by_category(category)
                    save_json(client_name, "1.2", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                # 1.3 Search by country
                elif sub_option == "1.3":
                    conn.send("SEND_COUNTRY".encode())
                    country = conn.recv(1024).decode().strip()

                    log_request(client_name, "1.3 Headlines Country", {"country": country})

                    results = search_by_country(country)
                    save_json(client_name, "1.3", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                # 1.4 List all headlines
                elif sub_option == "1.4":
                    log_request(client_name, "1.4 List All Headlines")

                    results = list_all_headlines()
                    save_json(client_name, "1.4", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                # Back
                elif sub_option == "1.5":
                    conn.send("BACK".encode())
                    break

                else:
                    conn.send("INVALID".encode())

        # -------------------- Option 2 ------------------------
        elif main_option == "2":
            conn.send("SOURCES_MENU".encode())

            while True:
                sub_option = conn.recv(1024).decode().strip()
                if not sub_option:
                    break
                #2.1
                if sub_option == "2.1":
                    conn.send("SEND_CATEGORY".encode())
                    category = conn.recv(1024).decode().strip()

                    log_request(client_name, "2.1 Sources Category", {"category": category})

                    results = sources_by_category(category)
                    save_json(client_name, "2.1", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())
                #2.2 
                elif sub_option == "2.2":
                    conn.send("SEND_COUNTRY".encode())
                    country = conn.recv(1024).decode().strip()

                    log_request(client_name, "2.2 Sources Country", {"country": country})

                    results = sources_by_country(country)
                    save_json(client_name, "2.2", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())
                #2.3
                elif sub_option == "2.3":
                    conn.send("SEND_LANGUAGE".encode())
                    language = conn.recv(1024).decode().strip()

                    log_request(client_name, "2.3 Sources Language", {"language": language})

                    results = sources_by_language(language)
                    save_json(client_name, "2.3", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())
                 #2.4
                elif sub_option == "2.4":
                    log_request(client_name, "2.4 List All Sources")

                    results = list_all_sources()
                    save_json(client_name, "2.4", results["data"])

                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx_data = conn.recv(1024).decode().strip()

                    if idx_data == "BACK":
                      continue  

                    idx = int(idx_data)
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())
                #2.5
                elif sub_option == "2.5":
                    conn.send("BACK".encode())
                    break

                else:
                    conn.send("INVALID".encode())

        elif main_option == "3":
            conn.send("BYE".encode())
            print(f"[QUIT] {client_name} disconnected")
            break

        else:
            conn.send("INVALID".encode())

    conn.close()
    print(f"[Disconnected] {client_name}")


####################################(Start Server)############################

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDR)
    server_socket.listen(5)

    print(f"Server is listening on {SERVER_ADDR}...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


start_server()
