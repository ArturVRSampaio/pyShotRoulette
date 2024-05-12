import socket

import main

from client_connection import ClientConnection

if __name__ == "__main__":
    waiting_players = True
    host = ""
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(True)
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
            should_start = input("Write y to start the game...")
            if should_start.lower() == 'y':
                waiting_players = False
        except:
            print("Failed to connect")

    print('game start')
    main.start(player_connections)
    for player_connection in player_connections:
        player_connection.close()
