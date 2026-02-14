import json
import os
import yaml

def load_settings():
    # Loads the YAML configuration from the root directory
    path = os.path.join(os.path.dirname(__file__), '..', 'settings.yml')
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                settings = yaml.safe_load(f)
                # The iconic warning
                print("--- SYSTEM NOTICE ---")
                print("WARNING: THIS AI IS NOT FOR COMMERCIAL USE AND ONLY FOR EDUCATIONAL/ENTERTAINMENT PURPUSES.")
                print("---------------------")
                return settings
        except yaml.YAMLError as e:
            print(f"Error parsing settings.yml: {e}")
    return {}

def load_token(settings):
    # v1.3.1: Loads the bot token from a separate file specified in settings.yml
    bot_settings = settings.get('bot_settings', {})
    token_filename = bot_settings.get('bot_token_file', 'token.txt')

    # If they put the actual token in the YAML by mistake, just use it
    if len(token_filename) > 40: 
        return token_filename

    path = os.path.join(os.path.dirname(__file__), '..', token_filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                # Strip whitespace and accidental quotes
                return f.read().strip().replace('"', '').replace("'", "")
        except Exception as e:
            print(f"Error reading token file: {e}")
    
    return None

def load_all_data():
    # Loads both modern vibe-coded and legacy knowledge JSON files
    base_path = os.path.dirname(__file__)

    # Modern responses
    vibe_path = os.path.join(base_path, '..', 'responses.json')
    vibe_data = []
    if os.path.exists(vibe_path):
        try:
            with open(vibe_path, 'r', encoding='utf-8') as f:
                vibe_data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Critical Error: responses.json is malformed!")

    # Legacy knowledge base
    legacy_path = os.path.join(base_path, '..', 'legacy_responses.json')
    legacy_data = {}
    if os.path.exists(legacy_path):
        try:
            with open(legacy_path, 'r', encoding='utf-8') as f:
                legacy_data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Critical Error: legacy_responses.json is malformed!")

    return vibe_data, legacy_data
