import sys
from bootstrap.responses_loader import load_all_data
from bootstrap.on_start import get_prefix, system_check
from bootstrap.engine import process_input

def run():
    # 1. Boot up
    vibe_data, legacy_data = load_all_data()
    prefix = get_prefix()

    if not system_check(vibe_data, legacy_data):
        print(f"{prefix}Error - Brain files not found. Check your JSONs.")
        return

    # 2. Capture User Input from Terminal
    user_query = " ".join(sys.argv[1:])
    
    # 3. Get response from Engine
    response = process_input(user_query, vibe_data, legacy_data)
    
    # 4. Final Output
    print(f"{prefix}{response}")

if __name__ == "__main__":
    run()
