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