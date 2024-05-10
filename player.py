import time
from helpers import clear_screen
from inventory import Inventory
from time import sleep
from random import randrange as rand


class Strategy:
    def decide_shot(self) -> int:
        pass

    def decide_action(self, player) -> str:
        pass

    def decide_item(self, game, player):
        pass

    def decide_other_player(self, player):
        pass


class Player:
    def __init__(self, strategy: Strategy, name: str):
        self.strategy = strategy
        self.life = 2
        self.name = name
        self.number = None
        self.inventory = Inventory()
        self.cuffed = False

    def decide(self, game):
        action = self.strategy.decide_action(self)
        while action != "shoot":
            if action == "use_item":
                item_count = self.strategy.decide_item(game, self)
                self.use_item(item_count, game)
            elif action == "look":
                game.print_items()
            action = self.strategy.decide_action(self)
        return self.strategy.decide_shot()

    def use_item(self, item_count, game):
        used_item = self.inventory.use_item(item_count, game, self)
        if not used_item:
            print("Slot empty, choose another item")
            return 0
        return used_item

    def remove_life(self, amount: int):
        self.life -= amount

    def set_number(self, number):
        self.number = number

    def un_cuff(self):
        print(f"{self.name} struggles to break free from his shackles...")
        time.sleep(1)
        clear_screen()
        self.cuffed = False


class HumanStrategy(Strategy):
    def decide_shot(self):
        return int(input("Player number to shoot?\n"))

    def decide_action(self, player: Player):
        PLAYER_ACTIONS = ["shoot", "use_item", "look"]
        index = int(input("Shoot(1), Use item(2), look at inventories(3)\n"))
        return PLAYER_ACTIONS[index - 1]

    def decide_item(self, game, player):
        if player.inventory.item_count() == 0:
            return False
        item_count = int(input("Which item do you want to use(1-4)?\n")) - 1
        return item_count

    def decide_other_player(self, player):
        other_player = int(input("Pick another player\n"))
        while other_player == player.number:
            print("Can't cuff yourself")
            other_player = int(input("Pick another player\n"))
        return other_player


class IaStrategy(Strategy):
    def decide_shot(self):
        print(f"IA player grabs the shotgun with malicious intent")
        sleep(1)
        who = rand(1, 3)
        print(f"{who}")
        return who

    def decide_action(self, ai_player: Player):
        print(f"{ai_player.name} looks at you with a grin")
        time.sleep(2)
        if ai_player.inventory.is_full():
            return "use_item"
        if ai_player.inventory.item_count() == 0:
            return "shoot"
        AI_ACTIONS = ["shoot", "use_item"]
        action = rand(0, len(AI_ACTIONS))
        return AI_ACTIONS[action]

    def decide_item(self, _game, player):
        print(f"{player.name} looks at the table")
        if player.inventory.item_count() == 0:
            return 0
        item_indexes = []
        for i in range(len(player.inventory.item_names)):
            if player.inventory.item_names[i] != "empty":
                item_indexes.append(i)
        random_index = rand(0, len(item_indexes))
        print(f"{player.name} uses item {item_indexes[random_index] + 1}")
        time.sleep(2)
        return item_indexes[random_index]

    def decide_other_player(self, player):
        other_players = [1, 2]
        other_players.remove(player.number)
        random_index = rand(0, len(other_players))
        return other_players[random_index]
