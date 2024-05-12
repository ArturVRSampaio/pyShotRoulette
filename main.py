import shutil

import colorama
import time
import art
from random import randrange as rand, shuffle

import items
from helpers import clear_screen
from player import HumanStrategy, IaStrategy, Player
from shotgun import Bullet, Shotgun


class Game:
    def __init__(self, players: list):
        self.round = 1
        self.max_life_round = 2
        self.last_round = 3
        self.players = players
        for number, player in enumerate(players):
            player.set_number(number + 1)
        self.shotgun = Shotgun()

    def print_separator(self):
        print("-" * 10 + "\n")

    def print_round(self):
        print("\n")
        print("I   II  III ")
        print("    " * (self.round - 1) + "X" + "    " * (3 - self.round))
        self.print_separator()

    def print_player_health(self):
        for player in sorted(self.players, key=lambda player: player.number):
            print(f"{player.name} ({player.number})")
            print(player.life)
        self.print_separator()

    def print_bullets(self, bullets: list):
        shuffle(bullets)
        bullet_types_string = ""
        for bullet in bullets:
            if bullet.type == "blank":
                bullet_types_string += colorama.Fore.WHITE
            else:
                bullet_types_string += colorama.Fore.RED
            bullet_types_string += f"*{bullet.type}* "
        print("bullets")
        print(bullet_types_string)
        print(colorama.Style.RESET_ALL)

    def print_items(self):
        for player in self.players:
            print(f"{player.name} inventory")
            print("-" * shutil.get_terminal_size().columns)
            player.inventory.print_items()
            print("-" * shutil.get_terminal_size().columns)

    def reset_player_lives(self, amount):
        for player in self.players:
            player.life = amount

    def reset_game(self):
        self.round += 1
        self.max_life_round = self.round * 2
        self.reset_player_lives(self.max_life_round)
        if self.round <= self.last_round:
            self.print_round()

        time.sleep(2)
        clear_screen()

    def get_player_by_number(self, number):
        for player in self.players:
            if player.number == number:
                return player
        raise Exception("Player not found")

    def play(self):
        self.print_round()
        time.sleep(2)
        clear_screen()

        while self.round <= self.last_round:
            shotgun_rounds_amount = rand(0, 7)

            for player in self.players:
                for _ in range(0, 2):
                    item = items.generate_item()
                    player.inventory.add_item(item)

            bullets = [Bullet("live"), Bullet("blank")]
            for _ in range(shotgun_rounds_amount):
                bullets.append(Bullet())
            self.print_round()
            self.print_bullets(bullets)
            self.shotgun.load(bullets)
            time.sleep(3)
            clear_screen()
            self.print_items()
            time.sleep(3)
            clear_screen()

            while (
                self.has_minimum_live_players() and len(self.shotgun.magazine_tube) > 0
            ):
                self.print_player_health()
                self.shotgun.print_shotgun()
                player = self.get_turn_player()

                if player.cuffed:
                    player.un_cuff()
                    self.next_player()
                    continue

                player_to_shoot_number = player.decide(game)
                if player_to_shoot_number == None:
                    self.next_player()
                    continue
                player_to_shoot = self.get_player_by_number(player_to_shoot_number)

                damage = self.shotgun.shot()

                if not (player_to_shoot == player and damage == 0):
                    self.next_player()

                player_to_shoot.remove_life(damage)
                time.sleep(2)
                clear_screen()

            if not self.has_minimum_live_players():
                self.winner()
                self.reset_game()

    def next_player(self):
        self.players.append(self.players.pop(0))

    def has_minimum_live_players(self) -> bool:
        alive_players = 0
        for player in self.players:
            if player.life > 0:
                alive_players += 1
        return alive_players >= 2

    def get_turn_player(self) -> Player:
        return self.players[0]

    def winner(self):
        for player in self.players:
            if player.life > 0:
                for i in range(0, 3):
                    print(colorama.Fore.GREEN)
                    art.tprint(f"{player.name} wins", space=2, font="small")
                    print(colorama.Style.RESET_ALL)
                    time.sleep(0.7)
                    clear_screen()
                    print("\n" * 7)
                    time.sleep(0.7)
                    clear_screen()


if __name__ == "__main__":
    clear_screen()
    player1 = Player(HumanStrategy(), "Human")
    player2 = Player(IaStrategy(), "IA")

    game = Game([player1, player2])

    game.play()
