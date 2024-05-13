import colorama
from random import randrange as rand, shuffle

from helpers import load_ascii_art


class Shotgun:
    def __init__(self):
        self.shotgun_art = load_ascii_art("assets/art/shotgun/long.txt")
        self.sawed_shotgun_art = load_ascii_art("assets/art/shotgun/sawed.txt")
        self.magazine_tube = []
        self.damage = 1
        self.sawn_off = False

    def load(self, bullets: list):
        shuffle(bullets)
        self.magazine_tube = bullets

    def is_empty(self):
        return len(self.magazine_tube) == 0

    def pump_magazine(self):
        if self.is_empty():
            return None
        bullet = self.magazine_tube.pop(0)
        return bullet

    # -1 -> shotgun empty, 0 -> shot blank, 1 -> shot live
    def shot(self) -> int:
        bullet = self.pump_magazine()
        if bullet is None:
            return -1
        shot_damage = self.damage
        self._un_saw()
        if bullet.type == "live":
            return shot_damage
        return 0

    def saw_off(self):
        self.damage = 2
        self.sawn_off = True

    def _un_saw(self):
        self.damage = 1
        self.sawn_off = False

    def serialize(self) -> str:
        if self.sawn_off:
            return self.sawed_shotgun_art
        return self.shotgun_art


class Bullet:
    possible_bullets = ["blank", "live"]

    def __init__(self, type=None):
        if not type:
            self.type = Bullet.possible_bullets[rand(0, 2)]
        else:
            self.type = type

    def serialize(self):
        if self.type == "blank":
            return colorama.Fore.WHITE + "*blank*" + colorama.Style.RESET_ALL + ""
        else:
            return colorama.Fore.RED + "*live*" + colorama.Style.RESET_ALL + ""
