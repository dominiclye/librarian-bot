import json

def load_json_settings():
    with open("defaults.json", "r") as f:
        return json.load(f)