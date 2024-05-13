import json

config_file = "server_config.json"
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

    if CONFIG.get("AIPlayers") is None:
        CONFIG["AIPlayers"] = 0
    
    if CONFIG.get("port") is None:
        CONFIG["port"] = 5000
