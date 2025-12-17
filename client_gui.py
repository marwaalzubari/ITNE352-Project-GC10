import socket
import json
import tkinter as tk
from tkinter import messagebox

SERVER_ADDR = ("127.0.0.1", 50555)
BUF_SIZE = 4096

countries = ["au", "ca", "jp", "ae", "sa", "kr", "us", "ma"]
languages = ["ar", "en"]
categories = ["business", "general", "health", "science", "sports", "technology"]

# ---------------- Socket helpers ----------------
#functions help to communicate with the server
def recv_text(sock):
    return sock.recv(BUF_SIZE).decode("utf-8", errors="replace").strip()

def recv_json(sock):
    while True:
        data = sock.recv(BUF_SIZE).decode("utf-8", errors="replace").strip()
        if not data:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            continue

# ---------------- GUI Client ----------------
#bulid the user interface
class NewsClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("News Service System")
        self.sock = None #store the server connection
        self.last_items = None #store the last search results
        self.build_login_screen() #start with the login screen

    # ---------- Screens ----------
    #for screen managment
    def clear_screen(self):
        #remove all widgets from the window before showing a new screen
        for widget in self.root.winfo_children():
            widget.destroy()
    #type client name screen
    def build_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Username").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Button(self.root, text="Connect", command=self.connect).pack(pady=10)
    # function to the main menu screen after enter user name
    def build_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Main Menu").pack(pady=10)
        tk.Button(self.root, text="Search Headlines", width=25, command=self.headlines_menu).pack(pady=5)
        tk.Button(self.root, text="List Sources", width=25, command=self.sources_menu).pack(pady=5)
        tk.Button(self.root, text="Quit", width=25, command=self.quit).pack(pady=5)

    # ----------  server Connection ----------
    def connect(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Username required")
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(SERVER_ADDR)# Connect to the server
            self.sock.sendall(username.encode())# Send username to the server
            self.build_main_menu()# Go to main menu
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    # ---------- Headlines menus ----------
    def headlines_menu(self):
        self.sock.sendall(b"1")#Send code for headlines to server
        recv_text(self.sock)  # Receive a server message

        self.clear_screen()
        tk.Label(self.root, text="Headlines Menu").pack(pady=10)
        tk.Button(self.root, text="Search by Keyword", command=lambda: self.param_request("1.1", None)).pack()
        tk.Button(self.root, text="Search by Category", command=lambda: self.param_request("1.2", categories)).pack()
        tk.Button(self.root, text="Search by Country", command=lambda: self.param_request("1.3", countries)).pack()
        tk.Button(self.root, text="List All Headlines", command=lambda: self.simple_request("1.4")).pack()
        tk.Button(self.root, text="Back", command=self.back_to_main).pack(pady=10)

    # ---------- Sources menus ----------
    def sources_menu(self):
        self.sock.sendall(b"2")# Send code for sources to server
        recv_text(self.sock)  #  Receive a server message
        self.clear_screen()
        tk.Label(self.root, text="Sources Menu").pack(pady=10)
        tk.Button(self.root, text="Search by Category", command=lambda: self.param_request("2.1", categories)).pack()
        tk.Button(self.root, text="Search by Country", command=lambda: self.param_request("2.2", countries)).pack()
        tk.Button(self.root, text="Search by Language", command=lambda: self.param_request("2.3", languages)).pack()
        tk.Button(self.root, text="List All Sources", command=lambda: self.simple_request("2.4")).pack()
        tk.Button(self.root, text="Back", command=self.back_to_main).pack(pady=10)

    # ----------  sending Requests to the server ----------
    def simple_request(self, option):
        # Request that doesn't need input (e.g., list all headlines)
        self.sock.sendall(option.encode())
        recv_text(self.sock)  # Receive server message
        items = recv_json(self.sock)# Receive data as JSON
        if items is not None:
            self.show_list(items)

    def param_request(self, option, allowed):
        # Request that requires user input (keyword, country, category...)
        self.sock.sendall(option.encode())
        server_req = recv_text(self.sock)

        self.clear_screen()
        tk.Label(self.root, text=f"{server_req}: Enter value").pack()
        entry = tk.Entry(self.root, width=50)
        entry.pack(pady=5)

        def send_param():
            value = entry.get().strip().lower()
            if not value:
                return
            if allowed and value not in allowed:
                messagebox.showerror("Error", f"Allowed: {allowed}")
                return
            self.sock.sendall(value.encode())
            items = recv_json(self.sock)
            if items is not None:
                self.show_list(items)

        tk.Button(self.root, text="Send", command=send_param).pack()
        tk.Button(self.root, text="Back", command=self.back_to_main).pack()

    # ---------- Display results ----------
    def show_list(self, items):
        self.last_items = items #save results for back navigation
        self.clear_screen()

        if not items:
            tk.Label(self.root, text="No results found").pack(pady=20)
            tk.Button(self.root, text="Back", command=self.back_to_main).pack()
            return

        listbox = tk.Listbox(self.root, width=80)
        for i, item in enumerate(items):
            text = item.get("title") or item.get("name")
            listbox.insert(tk.END, f"{i}) {text}")
        listbox.pack()
    
        def show_details():
            if not listbox.curselection():
                return
            idx = listbox.curselection()[0]
            self.sock.sendall(str(idx).encode())#Send selected index to server
            detail = recv_json(self.sock)# Receive details
            if detail:
                self.show_details_screen(detail)

        tk.Button(self.root, text="Show Details", command=show_details).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.back_to_main).pack()
    # function to Show details of a headline or source
    def show_details_screen(self, detail):
        self.clear_screen()
        text = tk.Text(self.root, width=80, height=20)
        for k, v in detail.items():
            text.insert(tk.END, f"{k}: {v}\n")
        text.pack()
        tk.Button(self.root, text="Back", command=self.back_to_list).pack(pady=10)

    # ---------- navigation ----------
    def back_to_list(self):
        try:
            self.sock.sendall(b"BACK")#notify server of going back
            recv_text(self.sock)
        except:
            pass
        if self.last_items:
            self.show_list(self.last_items)

    def back_to_main(self):
        self.build_main_menu()

    # ---------- Quit ----------
    def quit(self):
        try:
            self.sock.sendall(b"3")#notify server of exit
        except:
            pass
        self.sock.close()
        self.root.destroy()


# ---------------- Run application----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NewsClientGUI(root)
    root.mainloop()




