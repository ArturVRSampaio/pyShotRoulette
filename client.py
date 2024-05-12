import socket
from helpers import clear_screen

if __name__ == '__main__':
    buffer = ""
    msg = str(input("Enter your name:\n"))
    host = "127.0.0.1"
    port = 5000
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target = (host, port)
    connection.setblocking(True)
    connection.connect(target)
    connection.send(msg.encode('UTF-8'))
    print("Waiting for game to start")
    while True:
        data = connection.recv(1024)
        text = data.decode('UTF-8')
        buffer += text
        msgs = buffer.split(';')
        action = None
        if len(msgs) > 0:
            action = msgs[0]
            msgs.pop(0)
            for msg in msgs:
                buffer += msg + ";"

        match action:
            case 'print':
                complete = False
                msgs = []
                while not complete:
                    data = connection.recv(1024)
                    line = data.decode('UTF-8')
                    msgs = buffer.split(';')
                    if len(msgs) > 0:
                        for msg in msgs:
                            buffer += msg + ";"
                        complete = True
                line = msgs.pop(0)
                print(line)
            case 'clear':
                # clear_screen()
                print('clear')
            case 'input':
                data = connection.recv(1024)
                input_text = data.decode('UTF-8')
                # TODO: clear stdin
                input_data = input(input_text)
                connection.send(input_data.encode("UTF-8"))
            case _:
                print(f'chegou "{action}"')
