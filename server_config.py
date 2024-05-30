import json

from helpers import read_config

config_file = "server_config.json"
default_config = {"itemArtSize": "small", "AIPlayers": 0, "port": 5000}
CONFIG = read_config(config_file, default_config)

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
