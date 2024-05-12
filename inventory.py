import items


class Inventory:
    def __init__(self):
        self.item_names = ["empty", "empty", "empty", "empty"]

    def add_item(self, item):
        if self.is_full():
            return
        for i in range(len(self.item_names)):
            if self.item_names[i] == "empty":
                self.item_names[i] = item
                return

    def use_item(self, item_count: int, game, player):
        if self.item_names[item_count] == "empty":
            return False
        item_name = self.item_names[item_count]
        self.item_names[item_count] = "empty"
        item = items.all_items[item_name]
        return item.use(game, player)

    def item_count(self):
        return len(list(filter(lambda x: x != "empty", self.item_names)))

    def is_full(self):
        return all(item != "empty" for item in self.item_names)

    def print_items(self):
        inventory_item_lines = []
        for item in self.item_names:
            if item == "empty":
                inventory_item_lines.append(items.empty_item_art)
            else:
                inventory_item_lines.append(items.all_items[item].art)

        for i in range(10):
            print(" | ", end="")
            for item_line in inventory_item_lines:
                print(item_line[i], end=" | ")
            print()
