import sys
import socket
from _thread import *

if __name__ == '__main__':
    msg = str(input("Enter your name:\n"))
    host = "127.0.0.1"
    port = 5000
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target = (host, port)
    conn.connect(target)
    conn.send(msg.encode('UTF-8'))
    while True:
        pass
