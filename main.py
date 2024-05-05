import os
import colorama
import time
import art
from random import randrange as rand, shuffle

possible_bullets = ['blank', 'live']

def clear():
    # print('\n' *100)
    os.system("cls" if os.name == "nt" else "clear")

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
        if bullet.type == 'live':
            print(colorama.Fore.RED +'BANG!' + colorama.Style.RESET_ALL)
            return shot_damage
        print(colorama.Fore.WHITE + '*click*' + colorama.Style.RESET_ALL)
        return 0

    def saw_off(self):
        self.damage = 2

    def _un_saw(self):
        self.damage = 1


class Bullet():
    type = ''

    def __init__(self, type = None):
        if not type:
            self.type = possible_bullets[rand(0, 2)]
        else:
            self.type = type

class Human_strategy:
    def decide(self):
        return int(input("Player 1 or 2?\n")) - 1


class IA_strategy:
    def decide(self):
        print(f'IA player grabs the shotgun with malicious intent')
        time.sleep(1)
        who = rand(0, 2)
        print(f'{who + 1}')
        return rand(0, 2)


class Player:
    life = 0
    strategy = None

    def __init__(self, strategy):
        self.strategy = strategy
        self.life = 2

    def decide(self):
        return self.strategy.decide(self)

    def remove_life(self, amount: int):
        self.life -= amount


class Game:
    round = 1
    last_round = 3
    players = []
    turn = 0
    shotgun = None

    def __init__(self, players: list):
        self.players = players
        self.shotgun = Shotgun()

    def print_separator(self):
        print("-" * 20 + '\n')

    def print_round(self):
        print("I   II  III ")
        print("    " * (self.round - 1) + "X" + "    " * (3 - self.round))
        self.print_separator()

    def print_player_health(self):
        for key, player in enumerate(self.players):
            print(f"player {key + 1}")
            print(player.life)
        self.print_separator()

    def print_bullets(self, bullets: list):
        shuffle(bullets)
        bullet_types_string = ''
        for bullet in bullets:
            if bullet.type == 'blank':
                bullet_types_string += colorama.Fore.WHITE
            else:
                bullet_types_string += colorama.Fore.RED
            bullet_types_string += f"*{bullet.type}* "
        print('bullets')
        print(bullet_types_string)
        print(colorama.Style.RESET_ALL)

    def reset_player_lives(self, amount):
        for player in self.players:
            player.life = amount


    def reset_game(self):
        self.round += 1
        self.turn = 0
        self.reset_player_lives(self.round * 2)
        self.print_round()

        time.sleep(2)
        clear()

    def play(self):
        self.print_round()
        time.sleep(2)
        clear()

        while (self.round <= self.last_round):
            if not self.has_minimum_live_players():
                self.winner()
                self.reset_game()


            shotgun_rounds_amount = rand(0, 7)

            bullets = [Bullet('live'), Bullet('blank')]
            for new_bullet in range(shotgun_rounds_amount):
                bullets.append(Bullet())
            self.print_round()
            self.print_bullets(bullets)
            self.shotgun.load(bullets)
            time.sleep(3)
            clear()


            while self.has_minimum_live_players() and len(self.shotgun.magazine_tube) > 0:
                self.print_player_health()
                player = self.get_turn_player()
                player_to_shoot = self.players[player.decide()]
                damage = self.shotgun.shot()

                player_to_shoot.remove_life(damage)
                time.sleep(2)
                clear()


    def has_minimum_live_players(self) -> bool:
        alive_players = 0
        for player in self.players:
            if player.life > 0:
                alive_players += 1

        return alive_players >= 2

    def get_turn_player(self) -> Player:
        n_players = len(self.players)
        turn_player = self.players[self.turn]
        self.turn = (self.turn + 1) % n_players
        return turn_player

    def winner(self):
        for key, player in enumerate(self.players):
            if player.life > 0:
                print(colorama.Fore.GREEN)
                art.tprint(f"player {key + 1} wins", space=2)
                print(colorama.Style.RESET_ALL)
                time.sleep(2)
                clear()


if __name__ == '__main__':
    clear()
    player1 = Player(Human_strategy)
    player2 = Player(IA_strategy)

    game = Game([player1, player2])

    game.play()
