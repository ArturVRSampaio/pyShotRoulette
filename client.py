import socket
from helpers import clear_screen, read_config
from mtp import get_message, send_message


config_file = "config.json"
default_config = {"serverHost": "localhost", "serverPort": 5000}
CONFIG = read_config("config.json", default_config)


if __name__ == "__main__":
    buffer = ""
    msg = input("Enter your name:\n")

    host = CONFIG["serverHost"]
    port = CONFIG["serverPort"]

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
                input_data = input(input_text)
                send_message(connection, input_data)
            case "":
                clear_screen()
                print("Server closed connection")
                break
            case _:
                clear_screen()
                print(f'unexpected server action "{action}"')
                break
    input("Press enter to exit")
