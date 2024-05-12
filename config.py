import json

config_file = "config.json"
CONFIG = {}

with open(config_file, "r") as f:
    CONFIG = json.load(f)
    if CONFIG["itemArtSize"] == "large":
        CONFIG["itemArtWidth"] = 40
        CONFIG["itemArtHeight"] = 20
        CONFIG["itemArtFolder"] = "assets/art/items/HR"
    else:
        CONFIG["itemArtWidth"] = 20
        CONFIG["itemArtHeight"] = 10
        CONFIG["itemArtFolder"] = "assets/art/items/LR"
