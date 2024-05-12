import sys
import socket

if __name__ == "__main__":
    HOST = ""
    PORTA = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORTA))
    except socket.error as msg:
        print()
        raise Exception(
            f"Erro ao criar socket. Erro de codigo: {str(msg[0])} Message {msg[1]}"
        )
    print("Socket criado")

    # backlog de 10
    s.listen(10)

    while True:
        print("Socket esperando conexão")
        conn, addr = s.accept()

        ip, port = str(addr[0]), str(addr[1])
        print(f"Conectado com: {ip}:{port}\n")

        print("Esperando request do cliente")
        data = conn.recv(1024)
        request = data.decode("UTF-8")
        print("Cliente enviou: " + request)

        response = request[::-1]
        print("Respondendo: '" + response + "'")

        conn.send(response.encode("UTF-8"))
        conn.close()
    s.close()
