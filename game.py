import time
from random import randrange as rand
import colorama
import items
from client_connection import ClientConnection
from player import HumanPlayer, IaPlayer, Player
from shotgun import Bullet, Shotgun
from serverIO import ServerIO


class Game:
    def __init__(self, players: list):
        self.round = 1
        self.max_life_round = 2
        self.last_round = 3
        self.players = players
        for number, player in enumerate(players):
            player.set_number(number + 1)
        self.shotgun = Shotgun()
        self.serverIO = ServerIO(players)
        self.serverIO.send_clear_to_all_clients()

    def reset_player_lives(self, amount):
        for player in self.players:
            player.life = amount

    def reset_game(self):
        self.round += 1
        self.max_life_round = self.round * 2
        self.reset_player_lives(self.max_life_round)
        if self.round <= self.last_round:
            self.serverIO.print_round(self.round)

        time.sleep(2)
        self.serverIO.send_clear_to_all_clients()

    def get_player_by_number(self, number):
        for player in self.players:
            if player.number == number:
                return player
        raise Exception("Player not found")

    def play(self):
        self.serverIO.print_round(self.round)
        time.sleep(2)
        self.serverIO.send_clear_to_all_clients()

        while self.round <= self.last_round:
            shotgun_rounds_amount = rand(0, 7)

            for player in self.players:
                for _ in range(0, 2):
                    item = items.generate_item()
                    player.inventory.add_item(item)

            bullets = [Bullet("live"), Bullet("blank")]
            for _ in range(shotgun_rounds_amount):
                bullets.append(Bullet())
            self.serverIO.print_round(self.round)
            self.serverIO.print_bullets(bullets)
            self.shotgun.load(bullets)
            time.sleep(3)
            self.serverIO.send_clear_to_all_clients()
            self.serverIO.print_items()
            time.sleep(3)
            self.serverIO.send_clear_to_all_clients()

            while (
                self.has_minimum_live_players() and len(self.shotgun.magazine_tube) > 0
            ):
                self.serverIO.print_player_health()
                self.serverIO.send_text_to_all_clients(self.shotgun.serialize())
                player = self.get_turn_player()

                if player.cuffed:
                    self.serverIO.print_un_cuff(player)
                    player.un_cuff()
                    self.next_player()
                    continue

                player_to_shoot_number = player.decide(self)
                player_to_shoot = self.get_player_by_number(player_to_shoot_number)

                damage = self.shotgun.shot()

                match damage:
                    case 2:
                        self.serverIO.send_text_to_all_clients(
                            colorama.Fore.RED + "BANG!" + colorama.Style.RESET_ALL
                        )
                    case 1:
                        self.serverIO.send_text_to_all_clients(
                            colorama.Fore.RED + "BANG!" + colorama.Style.RESET_ALL
                        )
                    case 0:
                        self.serverIO.send_text_to_all_clients(
                            colorama.Fore.WHITE + "*click*" + colorama.Style.RESET_ALL
                        )

                if not (player_to_shoot == player and damage == 0):
                    self.next_player()

                player_to_shoot.remove_life(damage)
                time.sleep(2)
                self.serverIO.send_clear_to_all_clients()

            if not self.has_minimum_live_players():
                self.serverIO.winner()
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


def start(client_connections: list[ClientConnection]):
    players: list[Player] = []

    for client in client_connections:
        players.append(HumanPlayer(client))

    game = Game(players)
    game.play()