import os
import colorama
import time
import art
from random import randrange as rand, shuffle
from helpers import clear_screen, load_ascii_art

possible_bullets = ["blank", "live"]

shotgun_art = load_ascii_art("assets/shotgun.txt")


def print_shotgun():
    print(shotgun_art)


sawed_shotgun_art = load_ascii_art("assets/sawed_shotgun.txt")


def print_sawed_shotgun():
    print(sawed_shotgun_art)


class Shotgun:
    magazine_tube = []
    damage = 1

    def load(self, bullets: list):
        shuffle(bullets)
        self.magazine_tube = bullets

    def pump_magazine(self):
        bullet = self.magazine_tube.pop(0)
        return bullet

    def shot(self) -> int:
        bullet = self.pump_magazine()
        shot_damage = self.damage
        self._un_saw()
        if bullet.type == "live":
            print(colorama.Fore.RED + "BANG!" + colorama.Style.RESET_ALL)
            return shot_damage
        print(colorama.Fore.WHITE + "*click*" + colorama.Style.RESET_ALL)
        return 0

    def saw_off(self):
        self.damage = 2

    def _un_saw(self):
        self.damage = 1


class Bullet:
    type = ""

    def __init__(self, type=None):
        if not type:
            self.type = possible_bullets[rand(0, 2)]
        else:
            self.type = type


class HumanStrategy:
    def decide(self):
        return int(input("Player number to shoot?\n"))


class IaStrategy:
    def decide(self):
        print(f"IA player grabs the shotgun with malicious intent")
        time.sleep(1)
        who = rand(1, 3)
        print(f"{who}")
        return who


class Player:
    life = 0
    strategy = None
    name = None
    number = None

    def __init__(self, strategy, name: str):
        self.strategy = strategy
        self.life = 2
        self.name = name

    def decide(self):
        return self.strategy.decide(self)

    def remove_life(self, amount: int):
        self.life -= amount

    def set_number(self, number):
        self.number = number


class Game:
    round = 1
    last_round = 3
    players = []
    shotgun = None

    def __init__(self, players: list):
        self.players = players
        for number, player in enumerate(players):
            player.set_number(number + 1)
        self.shotgun = Shotgun()

    def print_separator(self):
        print("-" * 20 + "\n")

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

    def reset_player_lives(self, amount):
        for player in self.players:
            player.life = amount

    def reset_game(self):
        self.round += 1
        self.reset_player_lives(self.round * 2)
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

            bullets = [Bullet("live"), Bullet("blank")]
            for _ in range(shotgun_rounds_amount):
                bullets.append(Bullet())
            self.print_round()
            self.print_bullets(bullets)
            self.shotgun.load(bullets)
            time.sleep(3)
            clear_screen()

            while (
                self.has_minimum_live_players() and len(self.shotgun.magazine_tube) > 0
            ):
                self.print_player_health()
                print_shotgun()
                player = self.get_turn_player()
                player_to_shoot = self.get_player_by_number(player.decide())

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
    player1 = Player(HumanStrategy, "humman")
    player2 = Player(IaStrategy, "IA")

    game = Game([player1, player2])

    game.play()
