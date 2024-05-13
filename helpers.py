import os
import socket
import sys
import random


def clear_screen():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def load_ascii_art(file_path: str) -> str:
    with open(resource_path(file_path), "r") as file:
        return file.read()


def load_ascii_art_as_lines(file_path: str) -> list:
    with open(resource_path(file_path), "r") as file:
        return file.readlines()


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def int2roman(num: int) -> str:
    num_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    roman = ""

    while num > 0:
        for i, r in num_map:
            while num >= i:
                roman += r
                num -= i

    return roman
