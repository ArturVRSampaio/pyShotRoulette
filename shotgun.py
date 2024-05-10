import time
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

    def pump_magazine(self):
        if len(self.magazine_tube) == 0:
            print(colorama.Fore.WHITE + "*click*" + colorama.Style.RESET_ALL)
            time.sleep(1)
            print("It seems the shotgun is empty...")
            time.sleep(1)
            return None
        bullet = self.magazine_tube.pop(0)
        return bullet

    def shot(self) -> int:
        bullet = self.pump_magazine()
        if bullet == None:
            return 0
        shot_damage = self.damage
        self._un_saw()
        if bullet.type == "live":
            print(colorama.Fore.RED + "BANG!" + colorama.Style.RESET_ALL)
            return shot_damage
        print(colorama.Fore.WHITE + "*click*" + colorama.Style.RESET_ALL)
        return 0

    def saw_off(self):
        self.damage = 2
        self.sawn_off = True

    def _un_saw(self):
        self.damage = 1
        self.sawn_off = False

    def print_shotgun(self):
        if self.sawn_off:
            print(self.sawed_shotgun_art)
        else:
            print(self.shotgun_art)


class Bullet:
    possible_bullets = ["blank", "live"]

    def __init__(self, type=None):
        if not type:
            self.type = Bullet.possible_bullets[rand(0, 2)]
        else:
            self.type = type

    def print_bullet(self):
        if self.type == "blank":
            print(colorama.Fore.WHITE + "*blank*" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + "*live*" + colorama.Style.RESET_ALL)
