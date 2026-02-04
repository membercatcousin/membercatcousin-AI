import json
import os
import yaml

def load_settings():
    path = os.path.join(os.path.dirname(__file__), '..', 'settings.yml')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def load_all_data():
    base_path = os.path.dirname(__file__)

    # Load Vibe Data
    vibe_path = os.path.join(base_path, '..', 'responses.json')
    vibe_data = []
    if os.path.exists(vibe_path):
        with open(vibe_path, 'r', encoding='utf-8') as f:
            vibe_data = json.load(f)

    # Load Legacy Data
    legacy_path = os.path.join(base_path, '..', 'legacy_responses.json')
    legacy_data = {}
    if os.path.exists(legacy_path):
        with open(legacy_path, 'r', encoding='utf-8') as f:
            legacy_data = json.load(f)

    return vibe_data, legacy_data
