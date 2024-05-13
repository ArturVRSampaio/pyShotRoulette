import time
from random import shuffle

import art
import shutil
import colorama

from helpers import int2roman


class ServerIO:
    def __init__(self, players: list):
        self.players = players

    def send_text_to_all_clients(self, text: str) -> None:
        for player in self.players:
            player.client.print(text)

    def send_clear_to_all_clients(self) -> None:
        for player in self.players:
            player.client.clear()

    def winner(self) -> None:
        for player in self.players:
            if player.life > 0:
                for i in range(0, 3):
                    self.send_text_to_all_clients(colorama.Fore.GREEN)
                    result = art.text2art(f"{player.name} wins", space=2, font="small")
                    self.send_text_to_all_clients(result)
                    self.send_text_to_all_clients(colorama.Style.RESET_ALL)
                    time.sleep(0.7)
                    self.send_clear_to_all_clients()
                    self.send_text_to_all_clients("\n" * 7)
                    time.sleep(0.7)
                    self.send_clear_to_all_clients()

    def print_separator(self) -> None:
        self.send_text_to_all_clients("-" * 10 + "\n")

    def print_round(self, round: int, max_round: int) -> None:
        all_rounds_roman = []
        for i in range(1, max_round + 1):
            all_rounds_roman.append(int2roman(i))
        max_str_size = max(map(len, all_rounds_roman))
        rounds_text = ""
        for i in range(0, max_round):
            spaces = " " * (max_str_size - len(all_rounds_roman[i]) + 1)
            rounds_text += all_rounds_roman[i] + spaces
        self.send_text_to_all_clients("\n")
        self.send_text_to_all_clients(rounds_text)
        current_round_space = " " * (max_str_size)
        space_left = (current_round_space + " ") * (round - 1)
        space_right = (current_round_space + " ") * (max_round - round - 1)
        current_round_symbol = "X" + current_round_space
        self.send_text_to_all_clients(space_left + current_round_symbol + space_right)
        self.print_separator()

    def print_player_health(self) -> None:
        for player in sorted(self.players, key=lambda player: player.number):
            self.send_text_to_all_clients(f"{player.name} ({player.number})")
            self.send_text_to_all_clients(str(player.life))
        self.print_separator()

    def print_bullets(self, bullets: list) -> None:
        shuffle(bullets)
        bullet_types_string = ""
        for bullet in bullets:
            if bullet.type == "blank":
                bullet_types_string += colorama.Fore.WHITE
            else:
                bullet_types_string += colorama.Fore.RED
            bullet_types_string += f"*{bullet.type}* "
        self.send_text_to_all_clients("bullets")
        self.send_text_to_all_clients(bullet_types_string)
        self.send_text_to_all_clients(colorama.Style.RESET_ALL)

    def print_items(self) -> None:
        for player in self.players:
            self.send_text_to_all_clients(f"{player.name} inventory")
            self.send_text_to_all_clients("-" * shutil.get_terminal_size().columns)
            self.send_text_to_all_clients(player.inventory.serialize_items())
            self.send_text_to_all_clients("-" * shutil.get_terminal_size().columns)

    def print_un_cuff(self, player) -> None:
        self.send_text_to_all_clients(
            f"{player.name} struggles to break free from his shackles..."
        )
        time.sleep(2)
        self.send_clear_to_all_clients()
