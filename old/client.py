import sys
import socket
from _thread import *

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 5000
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target = (host, port)
    conn.connect(target)

    msg = str(input("Envie uma mensagem para o servidor:\n"))
    conn.send(msg.encode('UTF-8'))
    data = conn.recv(1024)
    reply = data.decode('UTF-8')
    print("Servidor respondeu: " + reply)
    conn.close()
