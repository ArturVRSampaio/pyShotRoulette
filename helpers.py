import os


def clear_screen():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def load_ascii_art(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def load_ascii_art_as_lines(file_path: str) -> list:
    with open(file_path, "r") as file:
        return file.readlines()
