ENCODING = "UTF-8"


class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        data = connection.recv(1024)
        self.player_name = data.decode(ENCODING)

    def print(self, line: str) -> None:
        line += ";"
        self.connection.send("print;".encode(ENCODING))
        self.connection.send(line.encode(ENCODING))

    def clear(self) -> None:
        self.connection.send("clear;".encode(ENCODING))

    def input(self, input_text) -> str:
        input_text += ";"
        self.connection.send("input;".encode(ENCODING))
        self.connection.send(input_text.encode(ENCODING))
        response = self.connection.recv(1024)
        return response.decode(ENCODING)

    def close(self) -> None:
        self.connection.close()


class MockClientConnection:
    def print(self, line) -> None:
        pass

    def clear(self):
        pass

    def input(self, input_text):
        raise Exception("Mocked client can't get input")
