import os
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
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def zalgoTextGenerator(text, intensity=5) -> str:
    zalgo_chars = [
        '\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310',
        '\u0352', '\u0357', '\u0351', '\u0307', '\u0308', '\u030a', '\u0342', '\u0343',
        '\u0344', '\u034a', '\u034b', '\u034c', '\u0303', '\u0302', '\u030c', '\u0350',
        '\u0300', '\u0301', '\u030b', '\u030f', '\u0312', '\u0313', '\u0314', '\u033d',
        '\u0309', '\u0363', '\u0364', '\u0365', '\u0366', '\u0367', '\u0368', '\u0369',
        '\u036a', '\u036b', '\u036c', '\u036d', '\u036e', '\u036f', '\u033e', '\u035b',
    ]

    zalgo_text = ''
    for char in text:
        zalgo_text += char
        for i in range(intensity):
            zalgo_text += random.choice(zalgo_chars)
    return zalgo_text
