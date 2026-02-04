import json
import os

def load_all_data():
    base_path = os.path.dirname(__file__)
    
    # Load Vibe Data (Keywords)
    vibe_path = os.path.join(base_path, '..', 'responses.json')
    vibe_data = []
    if os.path.exists(vibe_path):
        with open(vibe_path, 'r', encoding='utf-8') as f:
            vibe_data = json.load(f)

    # Load Legacy Data (Direct Lookup)
    legacy_path = os.path.join(base_path, '..', 'legacy_responses.json')
    legacy_data = {}
    if os.path.exists(legacy_path):
        with open(legacy_path, 'r', encoding='utf-8') as f:
            legacy_data = json.load(f)

    return vibe_data, legacy_data
