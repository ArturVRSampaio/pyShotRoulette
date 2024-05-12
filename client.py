import socket
from helpers import clear_screen
from mtp import get_message, send_message


if __name__ == "__main__":
    buffer = ""
    msg = str(input("Enter your name:\n"))
    host = "127.0.0.1"
    port = 5000
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target = (host, port)
    connection.setblocking(True)
    connection.connect(target)
    send_message(connection, msg)
    print("Waiting for game to start")
    while True:
        action = get_message(connection)

        match action:
            case "print":
                line = get_message(connection)
                print(line)
            case "clear":
                clear_screen()
            case "input":
                input_text = get_message(connection)
                # TODO: clear stdin
                input_data = input(input_text)
                send_message(connection, input_data)
            case _:
                raise Exception(f'unexpected server action "{action}"')
