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
