import time

import client_connection
from inventory import Inventory
from time import sleep
from random import randrange as rand
from abc import abstractmethod
from client_connection import ClientConnection
from serverIO import ServerIO

class Player:
    def __init__(self, name: str, kind: str, client):
        self.name = name
        self.number = None
        self.life = 2
        self.inventory = Inventory()
        self.cuffed = False
        self.client = client
        self.kind = kind
    @abstractmethod
    def decide_shot(self) -> int:
        pass

    @abstractmethod
    def decide_action(self) -> str:
        pass

    @abstractmethod
    def decide_item(self, game) -> int:
        pass

    @abstractmethod
    def decide_other_player(self) -> int:
        pass

    def decide(self, game) -> int:
        action = self.decide_action()
        while action != "shoot" and not game.shotgun.is_empty():
            if action == "use_item":
                item_number = self.decide_item(game)
                self.use_item(item_number, game)
            elif action == "look":
                game.serverIO.print_items()
            action = self.decide_action()
        if action == "shoot":
            return self.decide_shot()
        return self.number

    def use_item(self, item_number, game):
        used_item = self.inventory.use_item(item_number, game, self)
        if not used_item:
            self.client.print("Slot empty, choose another item")
            return 0
        return used_item

    def remove_life(self, amount: int):
        self.life -= amount

    def set_number(self, number):
        self.number = number

    def un_cuff(self):
        self.cuffed = False


class HumanPlayer(Player):
    def __init__(self, client: ClientConnection):
        super().__init__(client.player_name, 'player', client)

    def decide_shot(self) -> int:
        number = self.client.input("Player number to shoot?\n")
        return int(number)

    def decide_action(self) -> str:
        PLAYER_ACTIONS = ["shoot", "use_item", "look"]
        action = self.client.input("Shoot(1), Use item(2), look at inventories(3)\n")
        index = int(action)
        return PLAYER_ACTIONS[index - 1]

    def decide_item(self, game) -> int:
        if self.inventory.item_count() == 0:
            return False
        item_input = self.client.input("Which item do you want to use(1-4)?\n")
        item_count = int(item_input) - 1
        return item_count

    def decide_other_player(self) -> int:
        other_player_input = self.client.input("Pick another player\n")
        other_player = int(other_player_input)
        while other_player == self.number:
            self.client.print("Can't pick yourself")
            other_player_input = self.client.input("Pick another player\n")
            other_player = int(other_player_input)
        return other_player


class IaPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name, 'ia', client_connection.MockClientConnection())

    def set_server_io(self, serverIo):
        self.serverIo = serverIo
    def decide_shot(self):
        self.serverIO.send_text_to_all_clients(f"IA player grabs the shotgun with malicious intent")
        sleep(1)
        who = rand(1, 3)
        self.serverIO.send_text_to_all_clients(f"{who}")
        return who

    def decide_action(self) -> str:
        self.serverIO.send_text_to_all_clients(f"{self.name} looks at you with a grin")
        time.sleep(2)
        if self.inventory.is_full():
            return "use_item"
        if self.inventory.item_count() == 0:
            return "shoot"
        AI_ACTIONS = ["shoot", "use_item"]
        action = rand(0, len(AI_ACTIONS))
        return AI_ACTIONS[action]

    def decide_item(self, _game) -> int:
        self.serverIO.send_text_to_all_clients(f"{self.name} looks at the table")
        if self.inventory.item_count() == 0:
            return 0
        item_indexes = []
        for i in range(len(self.inventory.item_names)):
            if self.inventory.item_names[i] != "empty":
                item_indexes.append(i)
        random_index = rand(0, len(item_indexes))
        self.serverIO.send_text_to_all_clients(f"{self.name} uses item {item_indexes[random_index] + 1}")
        time.sleep(2)
        return item_indexes[random_index]

    def decide_other_player(self) -> int:
        other_players = [1, 2]
        other_players.remove(self.number)
        random_index = rand(0, len(other_players))
        return other_players[random_index]
