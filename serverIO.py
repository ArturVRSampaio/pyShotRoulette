import shutil
import time
import art
import colorama
from random import shuffle


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
                    result, font, decoration = art.text2art(f"{player.name} wins", space=2, font="small")
                    self.send_text_to_all_clients(result)
                    self.send_text_to_all_clients(colorama.Style.RESET_ALL)
                    time.sleep(0.7)
                    self.send_clear_to_all_clients()
                    self.send_text_to_all_clients("\n" * 7)
                    time.sleep(0.7)
                    self.send_clear_to_all_clients()

    def print_separator(self) -> None:
        self.send_text_to_all_clients("-" * 10 + "\n")

    def print_round(self, round: int) -> None:
        self.send_text_to_all_clients("\n")
        self.send_text_to_all_clients("I   II  III ")
        self.send_text_to_all_clients("    " * (round - 1) + "X" + "    " * (3 - round))
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
        self.send_text_to_all_clients(f"{player.name} struggles to break free from his shackles...")
        time.sleep(1)
        self.send_clear_to_all_clients()
