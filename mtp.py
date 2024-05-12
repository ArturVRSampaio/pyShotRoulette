from socket import socket


ENCODING = "UTF-8"
BYTE_ORDER = "big"


def send_message(connection: socket, message_string: str) -> None:
    message_size = len(message_string)
    connection.send(message_size.to_bytes(4, byteorder=BYTE_ORDER))
    connection.send(message_string.encode(ENCODING))


def get_message(connection: socket) -> str:
    message_size = int.from_bytes(connection.recv(4), byteorder=BYTE_ORDER)
    return connection.recv(message_size).decode(ENCODING)
