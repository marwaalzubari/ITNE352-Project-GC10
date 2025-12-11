import socket
import threading
import requests
import json
from datetime import datetime


SERVER_ADDR = ("127.0.0.1", 50555)
API_KEY = "ae701edbf7d847d4bb8de291a026194d"



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
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def search_by_category(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = limit_results(data.get("articles", []))
    return {
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def search_by_country(country):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = limit_results(data.get("articles", []))
    return {
        "brief_list": build_brief_list(articles),
        "full_articles": articles
    }


def list_all_headlines():
    url = f"https://newsapi.org/v2/top-headlines?apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = limit_results(data.get("articles", []))
    return {
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
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


def sources_by_country(country):
    url = f"https://newsapi.org/v2/top-headlines/sources?country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))

    return {
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


def sources_by_language(language):
    url = f"https://newsapi.org/v2/top-headlines/sources?language={language}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))

    return {
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }


def list_all_sources():
    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    sources = limit_sources(data.get("sources", []))

    return {
        "brief_list": build_sources_brief_list(sources),
        "full_list": sources
    }

########################################## (handle_client) #################################################

def handle_client(conn, addr):
    print(f"[Connected] {addr}")
    client_name = conn.recv(1024).decode().strip()
    print(f"[Client Connected] {client_name} from {addr}")

    while True:
        # ================= Main Menu Layer ====================
        main_option = conn.recv(1024).decode().strip()
        if not main_option:
            break

        # -------------------- Option 1 ------------------------
        if main_option == "1":
            conn.send("HEADLINES_MENU".encode())  # tell client to show submenu

            while True:
                sub_option = conn.recv(1024).decode().strip()
                if not sub_option:
                    break

                if sub_option == "1.1":
                    conn.send("SEND_KEYWORD".encode())
                    keyword = conn.recv(1024).decode()

                    results = search_by_keyword(keyword)
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                elif sub_option == "1.2":
                    conn.send("SEND_CATEGORY".encode())
                    category = conn.recv(1024).decode()

                    results = search_by_category(category)
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                elif sub_option == "1.3":
                    conn.send("SEND_COUNTRY".encode())
                    country = conn.recv(1024).decode()

                    results = search_by_country(country)
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                elif sub_option == "1.4":
                    results = list_all_headlines()
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(get_details(results["full_articles"], idx)).encode())

                elif sub_option == "1.5":
                    conn.send("BACK".encode())
                    break  # back to main menu

                else:
                    conn.send("INVALID".encode())

        # -------------------- Option 2 ------------------------
        elif main_option == "2":
            conn.send("SOURCES_MENU".encode())  # tell client to show submenu

            while True:
                sub_option = conn.recv(1024).decode().strip()
                if not sub_option:
                    break

                if sub_option == "2.1":
                    conn.send("SEND_CATEGORY".encode())
                    category = conn.recv(1024).decode()

                    results = sources_by_category(category)
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(build_sources_details(results["full_list"][idx])).encode())

                elif sub_option == "2.2":
                    conn.send("SEND_COUNTRY".encode())
                    country = conn.recv(1024).decode()

                    results = sources_by_country(country)
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(build_sources_details(results["full_list"][idx])).encode())

                elif sub_option == "2.3":
                    conn.send("SEND_LANGUAGE".encode())
                    language = conn.recv(1024).decode()

                    results = sources_by_language(language)
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(build_sources_details(results["full_list"][idx])).encode())

                elif sub_option == "2.4":
                    results = list_all_sources()
                    conn.send(json.dumps(results["brief_list"]).encode())

                    idx = int(conn.recv(1024).decode())
                    conn.send(json.dumps(build_sources_details(results["full_list"][idx])).encode())

                elif sub_option == "2.5":
                    conn.send("BACK".encode())
                    break  # back to main menu

                else:
                    conn.send("INVALID".encode())


        # -------------------- Option 3 ------------------------
        elif main_option == "3":
            conn.send("BYE".encode())
            print(f"[QUIT] {addr} disconnected")
            break

        else:
            conn.send("INVALID".encode())

    conn.close()
    print(f"[Disconnected] {addr}")



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
