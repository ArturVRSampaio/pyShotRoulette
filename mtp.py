from socket import socket


ENCODING = "UTF-8"
BYTE_ORDER = "big"


def send_message(connection: socket, message_string: str) -> None:
    message_size = len(message_string)
    connection.send(message_size.to_bytes(4, byteorder=BYTE_ORDER))
    connection.send(message_string.encode(ENCODING))


def get_message(connection: socket) -> str:
    size_data = connection.recv(4)
    while len(size_data) < 4:
        size_data += connection.recv(4 - len(size_data))
    message_size = int.from_bytes(size_data, byteorder=BYTE_ORDER)
    message_data = connection.recv(message_size)
    while len(message_data) < message_size:
        message_data += connection.recv(message_size - len(message_data))
    return message_data.decode(ENCODING)
