import socket
import threading

import main

waiting_players = True


class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        data = connection.recv(1024)
        self.player_name = data.decode("UTF-8")
    def close(self):
        self.connection.close()


def thread_function():
    global waiting_players
    host = ""
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(0.5)
    server_socket.bind((host, port))
    server_socket.listen(10)

    print('Waiting for players to join')

    player_connections = []

    while waiting_players:
        try:
            connection, address = server_socket.accept()
            player = ClientConnection(connection, address)
            player_connections.append(player)
            print(f'{player.player_name} joined the game')

        except socket.timeout:
            pass
        except:
            print("Failed to connect")

    print('game start')
    main.start(player_connections)
    for player_connection in player_connections:
        player_connection.close()


if __name__ == "__main__":
    x = threading.Thread(target=thread_function, args=())
    x.start()
    input("Enter to start game...")
    waiting_players = False
    x.join()
