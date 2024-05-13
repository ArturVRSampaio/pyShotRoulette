import server_config
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

    def serialize_items(self) -> str:
        inventory_item_lines = []
        for item in self.item_names:
            if item == "empty":
                inventory_item_lines.append(items.empty_item_art)
            else:
                inventory_item_lines.append(items.all_items[item].art)

        text = ""
        for i in range(server_config.CONFIG["itemArtHeight"]):
            text += " | "
            for item_line in inventory_item_lines:
                text += item_line[i] + " | "
            text += "\n"
        return text
