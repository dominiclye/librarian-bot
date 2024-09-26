import json

def load_json_settings():
    with open("server_defaults.json", "r") as f:
        return json.load(f)
    
def load_user_json_settings():
    with open("user_defaults.json", "r") as f:
        return json.load(f)