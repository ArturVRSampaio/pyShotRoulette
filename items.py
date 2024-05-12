import time

import colorama

import config

from random import randrange as rand

from helpers import load_ascii_art_as_lines
from shotgun import Bullet
from abc import ABC, abstractmethod


# loads it into a list of lines without newline characters
def load_item_art(fname: str) -> list:
    item_lines = load_ascii_art_as_lines(fname)
    remove_newline_character = lambda x: x.replace("\n", "").replace("\r", "")

    formatted_lines = list(map(remove_newline_character, item_lines))
    width = config.CONFIG["itemArtWidth"]
    height = config.CONFIG["itemArtHeight"]

    if len(formatted_lines) < height:
        raise ValueError(f"Item file {fname} must have {height} lines")

    for line in formatted_lines:
        if len(line) != width:
            raise ValueError(f"Item file {fname} must have {width} characters per line")

    return formatted_lines


class AbstractItem:
    art: list[str]
    item_name: str

    def __init__(self):
        folder = config.CONFIG["itemArtFolder"]
        self.art = load_item_art(f"{folder}/{self.item_name}.txt")

    @abstractmethod
    def use(self, game, player) -> bool:
        raise Exception("Not implemented")


class Adrenaline(AbstractItem):
    item_name = "adrenaline"

    def use(self, game, player):
        print(f"{player.name} takes a deep breath and injects the suspicious needle")
        game.print_items()
        time.sleep(1)
        player_number = player.strategy.decide_other_player(player)
        player_to_get_item = game.get_player_by_number(player_number)
        print(
            f"the adrenaline rush lets him grab on of {player_to_get_item.name}'s items"
        )
        time.sleep(1)
        if player_to_get_item.inventory.item_count() == 0:
            print(f"but {player_to_get_item.name} has no items to be stolen...")
            return False
        item_number = player.strategy.decide_item(game, player_to_get_item)
        if player_to_get_item.inventory.item_names[item_number] == "adrenaline":
            print(
                f"but fumbles and doesn't manage to grab {player_to_get_item.name}'s adrenaline shot..."
            )
            return False
        return player_to_get_item.inventory.use_item(item_number, game, player)


class Beer(AbstractItem):
    item_name = "beer"

    def use(self, game, player):
        print(
            f"{player.name} drinks a beer and pumps the shotgun...", end="", flush=True
        )
        time.sleep(1)
        print("to reveal a", end=" ")
        bullet = game.shotgun.pump_magazine()
        if bullet.type == "blank":
            print(colorama.Fore.WHITE + "*blank*" + colorama.Style.RESET_ALL + " round")
        else:
            print(colorama.Fore.RED + "*live*" + colorama.Style.RESET_ALL + " round")
        time.sleep(0.5)
        return True


class Cigarette(AbstractItem):
    item_name = "cigarette"

    def use(self, game, player):
        print(f"{player.name} lights a cigarette and takes a puff...")
        time.sleep(0.5)
        if player.life < game.max_life_round:
            player.life += 1
        game.print_player_health()
        return True


class Handcuff(AbstractItem):
    item_name = "handcuff"

    def use(self, game, player):
        print(f"{player.name} raises handcuffs looking for a victim...")
        time.sleep(0.5)
        player_number = player.strategy.decide_other_player(player)
        player_to_handcuff = game.get_player_by_number(player_number)
        print(f"and cuffs {player_to_handcuff.name}")
        if player_to_handcuff.cuffed:
            return False
        player_to_handcuff.cuffed = True
        return True


class Inverter(AbstractItem):
    item_name = "inverter"

    def use(self, game, player):
        print(f"{player.name} spins the inverter up")
        if game.shotgun.magazine_tube[0].type == "blank":
            game.shotgun.magazine_tube[0] = Bullet("live")
        else:
            game.shotgun.magazine_tube[0] = Bullet("blank")
        return True


class Magnifier(AbstractItem):
    item_name = "magnifier"

    def use(self, game, player):
        print(
            f"{player.name} looks through the magnifier into the chamber...",
            end="",
            flush=True,
        )
        time.sleep(0.5)
        game.shotgun.magazine_tube[0].print_bullet()
        return True


class Phone(AbstractItem):
    item_name = "phone"

    def use(self, game, player):
        print(
            f"{player.name} hears an ominous voice on the phone...", end="", flush=True
        )
        time.sleep(0.5)
        bullet_number = rand(0, len(game.shotgun.magazine_tube))
        print(
            f"It says: buLlEt nuMbER {colorama.Fore.BLUE}{bullet_number + 1}{colorama.Style.RESET_ALL} iS a",
            end=" ",
        )
        game.shotgun.magazine_tube[bullet_number].print_bullet()
        return True


class Pill(AbstractItem):
    item_name = "pill"

    def use(self, game, player):
        print(f"{player.name} takes a pill...")
        time.sleep(1)
        chance = rand(0, 100)
        if chance < 50:
            player.life += 2
        else:
            player.life -= 1
        if player.life > game.max_life_round:
            player.life = game.max_life_round
        if player.life < 0:
            player.life = 0
        game.print_player_health()
        return True


class Saw(AbstractItem):
    item_name = "saw"

    def use(self, game, player):
        if not game.shotgun.sawn_off:
            print(f"{player.name} grabs a saw and saws off the shotgun barrel")
            game.shotgun.saw_off()
            game.shotgun.print_shotgun()
        return True


all_items = {
    "adrenaline": Adrenaline(),
    "beer": Beer(),
    "cigarette": Cigarette(),
    "handcuff": Handcuff(),
    "inverter": Inverter(),
    "magnifier": Magnifier(),
    "phone": Phone(),
    "pill": Pill(),
    "saw": Saw(),
}

empty_item_art = []
for _ in range(config.CONFIG["itemArtHeight"]):
    line = " " * config.CONFIG["itemArtWidth"]
    empty_item_art.append(line)


def generate_item():
    ALL_ITEMS = list(filter(lambda x: x != "empty", all_items.keys()))
    random_index = rand(0, len(ALL_ITEMS))
    return ALL_ITEMS[random_index]
