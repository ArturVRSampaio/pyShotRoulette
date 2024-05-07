from helpers import clear_screen, load_ascii_art_as_lines


# Validates if file has 20 lines and 40 characters per line
# loads it into a list of lines without newline characters
def load_item(fname: str) -> list:
    item_lines = load_ascii_art_as_lines(fname)
    remove_newline_character = lambda x: x.replace("\n", "").replace("\r", "")

    formatted_lines = list(map(remove_newline_character, item_lines))
    if len(formatted_lines) < 20:
        raise ValueError(f"Item file {fname} must have 20 lines")

    for line in formatted_lines:
        if len(line) != 40:
            raise ValueError(f"Item file {fname} must have 40 characters per line")

    return formatted_lines


# Assuming all items have 20 lines and 40 characters per line
def empty_item() -> list:
    empty_item_lines = []
    for _ in range(20):
        line = " " * 40
        empty_item_lines.append(line)
    return empty_item_lines


class Inventory:
    item_lines = {
        "empty": empty_item(),
        "adrenaline": load_item("assets/adrenaline.txt"),
        "beer": load_item("assets/beer.txt"),
        "cigarette": load_item("assets/cigarette.txt"),
        "handcuff": load_item("assets/handcuff.txt"),
        "inverter": load_item("assets/inverter.txt"),
        "magnifier": load_item("assets/magnifier.txt"),
        "phone": load_item("assets/phone.txt"),
        "pill": load_item("assets/pill.txt"),
        "saw": load_item("assets/saw.txt"),
    }

    def __init__(self):
        self.items = ["empty", "empty", "empty", "empty"]

    def add_item(self, item: str):
        if item not in self.item_lines or item == "empty":
            raise ValueError(f"Item {item} could not be added to inventory")
        for i in range(len(self.items)):
            if self.items[i] == "empty":
                self.items[i] = item
                return
        raise ValueError("Inventory is full")

    def use_item(self, item: str):
        for i in range(len(self.items)):
            if self.items[i] == item:
                print(f"Using {item}")
                # TODO: Implement item effect on game
                self.items[i] = "empty"
        return False

    def is_full(self):
        return all(item != "empty" for item in self.items)

    def print_items(self):
        inventory_item_lines = [self.item_lines[item] for item in self.items]
        for i in range(20):
            print(" | ", end="")
            for item_line in inventory_item_lines:
                print(item_line[i], end=" | ")
            print()


clear_screen()

print(" " + "-" * 173)

inventory_p1 = Inventory()
inventory_p1.add_item("phone")
inventory_p1.add_item("pill")
inventory_p1.add_item("adrenaline")
inventory_p1.add_item("beer")
inventory_p1.print_items()

print(" " + "-" * 173)

inventory_p2 = Inventory()
inventory_p2.add_item("saw")
inventory_p2.add_item("cigarette")
inventory_p2.add_item("handcuff")
inventory_p2.print_items()

print(" " + "-" * 173)

inventory_p3 = Inventory()
inventory_p3.add_item("inverter")
inventory_p3.add_item("magnifier")
inventory_p3.print_items()

print(" " + "-" * 173)

input("Press Enter to continue...")
