import socket
import json
import tkinter as tk
from tkinter import messagebox


SERVER_ADDR=("127.0.0.1",50555)
BUF_SIZE=4096

countries = ["au","ca","jp","ae","sa","kr","us","ma"]
languages = ["ar","en"]
categories = ["business","general","health","science","sports","technology"]

# ---------------- Socket helpers ----------------
def recv_text(sock):
    return sock.recv(BUF_SIZE).decode("utf-8", errors="replace").strip()

def recv_json(sock):
    data = sock.recv(BUF_SIZE).decode("utf-8", errors="replace")
    return json.loads(data)

# ---------------- GUI Client ----------------
class NewsClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("News Service System")
        self.sock = None
        self.full_list = []

        self.build_login_screen()

    # ---------- Screens ----------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def build_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Username").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Button(self.root, text="Connect", command=self.connect).pack(pady=10)

    def build_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Main Menu").pack(pady=10)
        tk.Button(self.root, text="Search Headlines", width=25, command=self.headlines_menu).pack(pady=5)
        tk.Button(self.root, text="List Sources", width=25, command=self.sources_menu).pack(pady=5)
        tk.Button(self.root, text="Quit", width=25, command=self.quit).pack(pady=5)
        
   # ---------- Connection ----------
    def connect(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Username required")
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(SERVER_ADDR)
            self.sock.sendall(username.encode())
            self.build_main_menu()
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))  
    # ---------- Headlines ----------
    def headlines_menu(self):
        self.sock.sendall(b"1")
        recv_text(self.sock)  # HEADLINES_MENU

        self.clear_screen()
        tk.Label(self.root, text="Headlines Menu").pack(pady=10)

        tk.Button(self.root, text="Search by Keyword", command=lambda: self.param_request("1.1", None)).pack()
        tk.Button(self.root, text="Search by Category", command=lambda: self.param_request("1.2", categories)).pack()
        tk.Button(self.root, text="Search by Country", command=lambda: self.param_request("1.3", countries)).pack()
        tk.Button(self.root, text="List All Headlines", command=lambda: self.simple_request("1.4")).pack()
        tk.Button(self.root, text="Back", command=self.build_main_menu).pack(pady=10)     
        # ---------- Sources ----------
    def sources_menu(self):
        self.sock.sendall(b"2")
        recv_text(self.sock)  # SOURCES_MENU

        self.clear_screen()
        tk.Label(self.root, text="Sources Menu").pack(pady=10)

        tk.Button(self.root, text="Search by Category", command=lambda: self.param_request("2.1", categories)).pack()
        tk.Button(self.root, text="Search by Country", command=lambda: self.param_request("2.2", countries)).pack()
        tk.Button(self.root, text="Search by Language", command=lambda: self.param_request("2.3", languages)).pack()
        tk.Button(self.root, text="List All Sources", command=lambda: self.simple_request("2.4")).pack()
        tk.Button(self.root, text="Back", command=self.build_main_menu).pack(pady=10)
    # ---------- Requests ----------
    def simple_request(self, option):
        self.sock.sendall(option.encode())
        server_req = recv_text(self.sock)
        if server_req == "INVALID":
            return
        self.show_list(recv_json(self.sock), option)

    def param_request(self, option, allowed):
        self.sock.sendall(option.encode())
        server_req = recv_text(self.sock)

        self.clear_screen()
        tk.Label(self.root, text=f"{server_req}: Enter value").pack()
        
        entry = tk.Entry(self.root,width=50)
        entry.pack(pady=5)

        def send_param():
            value = entry.get().strip().lower()
            if not value:
                messagebox.showerror("Error", "Invalid value")
                return
             
            if allowed is not None and value not in allowed:
                messagebox.showerror("Error", f"Invalid value. Allowed: {allowed}")
                return
            self.sock.sendall(value.encode())
            self.show_list(recv_json(self.sock), option)

        tk.Button(self.root, text="Send", command=send_param).pack()  
        tk.Button(self.root, text="Back", command=self.headlines_menu).pack()       
# ---------- Display ----------
    def show_list(self, items):
        self.full_list = items
        self.clear_screen()

        listbox = tk.Listbox(self.root, width=80)
        for i, item in enumerate(items):
            text = item.get("title") or item.get("name")
            listbox.insert(tk.END, f"{i}) {text}")
        listbox.pack()
    
        def show_details():
            if not listbox.curselection():
                return
            idx = listbox.curselection()[0]
            self.sock.sendall(str(idx).encode())
            detail = recv_json(self.sock)
            self.show_details_screen(detail)

        tk.Button(self.root, text="Show Details", command=show_details).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.build_main_menu).pack()

    def show_details_screen(self, detail):
        self.clear_screen()
        text = tk.Text(self.root, width=80, height=20)
        for k, v in detail.items():
            text.insert(tk.END, f"{k}: {v}\n")
        text.pack()
        tk.Button(self.root, text="Back", command=self.build_main_menu).pack(pady=10)
 # ---------- Quit ----------
    def quit(self):
        try:
            self.sock.sendall(b"3")
        except:
            pass
        self.sock.close()
        self.root.destroy()
# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NewsClientGUI(root)
    root.mainloop()