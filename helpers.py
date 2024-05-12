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
