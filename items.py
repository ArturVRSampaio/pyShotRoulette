import time

import colorama

from random import randrange as rand

from helpers import load_ascii_art_as_lines
from shotgun import Bullet


# Validates if file has 20 lines and 40 characters per line
# loads it into a list of lines without newline characters
def load_item(fname: str) -> list:
    item_lines = load_ascii_art_as_lines(fname)
    remove_newline_character = lambda x: x.replace("\n", "").replace("\r", "")

    formatted_lines = list(map(remove_newline_character, item_lines))
    if len(formatted_lines) < 20:
        raise ValueError(f"Item file {fname} must have 20 lines")

    for line in formatted_lines:
        if len(line) != 40:
            raise ValueError(f"Item file {fname} must have 40 characters per line")

    return formatted_lines


class Item:
    def __init__(self, item_name: str, item_effect: callable):
        self.item_name = item_name
        self.art = load_item(f"assets/art/items/{item_name}.txt")
        self.item_effect = item_effect

    def use(self, game, player) -> bool:
        return self.item_effect(game, player)


def adrenaline_effect(game, player):
    print(f"{player.name} takes a deep breath and injects the suspicious needle")
    game.print_items()
    time.sleep(1)
    player_number = player.strategy.decide_other_player(player)
    player_to_get_item = game.get_player_by_number(player_number)
    print(f"the adrenaline rush lets him grab on of {player_to_get_item.name}'s items")
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


def beer_effect(game, player):
    print(f"{player.name} drinks a beer and pumps the shotgun...", end="", flush=True)
    time.sleep(1)
    print("to reveal a", end=" ")
    bullet = game.shotgun.pump_magazine()
    if bullet.type == "blank":
        print(colorama.Fore.WHITE + "*blank*" + colorama.Style.RESET_ALL + " round")
    else:
        print(colorama.Fore.RED + "*live*" + colorama.Style.RESET_ALL + " round")
    time.sleep(0.5)
    return True


def cigarette_effect(game, player):
    print(f"{player.name} lights a cigarette and takes a puff...")
    time.sleep(0.5)
    if player.life < game.max_life_round:
        player.life += 1
    game.print_player_health()
    return True


def handcuff_effect(game, player):
    print(f"{player.name} raises handcuffs looking for a victim...")
    time.sleep(0.5)
    player_number = player.strategy.decide_other_player(player)
    player_to_handcuff = game.get_player_by_number(player_number)
    print(f"and cuffs {player_to_handcuff.name}")
    if player_to_handcuff.cuffed:
        return False
    player_to_handcuff.cuffed = True
    return True


def inverter_effect(game, player):
    print(f"{player.name} spins the inverter up")
    if game.shotgun.magazine_tube[0].type == "blank":
        game.shotgun.magazine_tube[0] = Bullet("live")
    else:
        game.shotgun.magazine_tube[0] = Bullet("blank")
    return True


def magnifier_effect(game, player):
    print(
        f"{player.name} looks through the magnifier into the chamber...",
        end="",
        flush=True,
    )
    time.sleep(0.5)
    game.shotgun.magazine_tube[0].print_bullet()
    return True


def phone_effect(game, player):
    print(f"{player.name} hears an ominous voice on the phone...", end="", flush=True)
    time.sleep(0.5)
    bullet_number = rand(0, len(game.shotgun.magazine_tube))
    print(
        f"It says: buLlEt nuMbER {colorama.Fore.BLUE}{bullet_number + 1}{colorama.Style.RESET_ALL} iS a",
        end=" ",
    )
    game.shotgun.magazine_tube[bullet_number].print_bullet()
    return True


def pill_effect(game, player):
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


def saw_effect(game, player):
    if not game.shotgun.sawn_off:
        print(f"{player.name} grabs a saw and saws off the shotgun barrel")
        game.shotgun.saw_off()
        game.shotgun.print_shotgun()
    return True


all_items = {
    "adrenaline": Item("adrenaline", adrenaline_effect),
    "beer": Item("beer", beer_effect),
    "cigarette": Item("cigarette", cigarette_effect),
    "handcuff": Item("handcuff", handcuff_effect),
    "inverter": Item("inverter", inverter_effect),
    "magnifier": Item("magnifier", magnifier_effect),
    "phone": Item("phone", phone_effect),
    "pill": Item("pill", pill_effect),
    "saw": Item("saw", saw_effect),
}


# Assuming all items have 20 lines and 40 characters per line
empty_item_art = []
for _ in range(20):
    line = " " * 40
    empty_item_art.append(line)


def generate_item():
    ALL_ITEMS = list(filter(lambda x: x != "empty", all_items.keys()))
    random_index = rand(0, len(ALL_ITEMS))
    return ALL_ITEMS[random_index]
