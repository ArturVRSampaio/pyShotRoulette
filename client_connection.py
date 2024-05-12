from mtp import get_message, send_message


class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.player_name = get_message(self.connection)

    def print(self, line: str) -> None:
        send_message(self.connection, "print")
        send_message(self.connection, line)

    def clear(self) -> None:
        send_message(self.connection, "clear")

    def input(self, input_text: str) -> str:
        send_message(self.connection, "input")
        send_message(self.connection, input_text)
        response = get_message(self.connection)
        return response

    def close(self) -> None:
        self.connection.close()


class MockClientConnection:
    def print(self, line) -> None:
        pass

    def clear(self):
        pass

    def input(self, input_text):
        raise Exception("Mocked client can't get input")
