from random import randrange as rand, shuffle

possible_bullets = ['blank', 'live']


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
            return shot_damage
        return 0

    def saw_off(self):
        self.damage = 2

    def _un_saw(self):
        self.damage = 1


class Bullet():
    type = ''

    def __init__(self):
        self.type = possible_bullets[rand(0, 2)]


class Human_strategy:
    def decide(self):
        return int(input("Player 1 or 2?\n")) - 1


class IA_strategy:
    def decide(self):
        print('ooga booga ia shoots')
        return rand(0, 2)


class Player:
    life = 0
    strategy = None

    def __init__(self, strategy):
        self.strategy = strategy
        self.life = 6

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

    def print_round(self):
        print("I   II  III ")
        print("    " * (self.round - 1) + "X" + "    " * (3 - self.round))
        print("-" * 20)

    def print_player_health(self):
        for key, player in enumerate(self.players):
            print(f"player {key}")
            print(player.life)

    def play(self):
        self.print_round()

        while (self.round <= self.last_round):
            if not self.has_minimum_live_players():
                self.winner()
                self.round += 1
                self.turn = 0
                for player in self.players:
                    player.life = 6
                self.print_round()


            # rand quatidade de bala
            shotgun_rounds = rand(2, 8)
            # new pela quantidade
            bullets = []
            for new_bullet in range(shotgun_rounds):
                bullets.append(Bullet())
            #print bullets
            print('bullets')
            for bullet in bullets:
                print(f"*{bullet.type}* ")

            # carrregar a 12
            self.shotgun.load(bullets)

            while self.has_minimum_live_players() and len(self.shotgun.magazine_tube) > 0:
                self.print_player_health()
                player = self.get_turn_player()
                player_to_shoot = self.players[player.decide()]
                damage = self.shotgun.shot()

                player_to_shoot.remove_life(damage)

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
                print(f"player {key + 1} wins")


if __name__ == '__main__':
    player1 = Player(Human_strategy)
    player2 = Player(IA_strategy)

    game = Game([player1, player2])

    game.play()
