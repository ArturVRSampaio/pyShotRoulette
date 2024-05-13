import socket
import game
from threading import Thread

from client_connection import ClientConnection
from server_config import CONFIG

waiting_players = True


def main():
    global waiting_players
    waiting_players = True
    host = ""
    port = CONFIG["port"]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(2)
    server_socket.bind((host, port))
    server_socket.listen(10)

    print("Waiting for players to join")

    player_connections = []

    while waiting_players:
        try:
            connection, address = server_socket.accept()
            player = ClientConnection(connection, address)
            player_connections.append(player)
            print(f"{player.player_name} joined the game")
        except socket.timeout:
            pass
        except:
            print("Failed to connect")

    print("game start")
    game.start(player_connections)
    for player_connection in player_connections:
        player_connection.close()


if __name__ == "__main__":
    thread = Thread(target=main)
    print("Press enter to start the game")
    thread.start()
    input()
    waiting_players = False
    thread.join()
