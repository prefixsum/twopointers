import json
import os


def save_config(guild_id, config):
    with open(f"server_configs/{guild_id}.json", "w") as f:
        json.dump(config, f)


def load_config(guild_id):
    try:
        with open(f"server_configs/{guild_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def ensure_config_directory():
    if not os.path.exists("server_configs"):
        os.makedirs("server_configs")
