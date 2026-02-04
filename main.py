import sys
from bootstrap.responses_loader import load_all_data
from bootstrap.on_start import get_prefix, system_check
from bootstrap.engine import process_input

def run():
    # 1. Boot up
    vibe_data, legacy_data = load_all_data()
    prefix = get_prefix()

    if not system_check(vibe_data, legacy_data):
        print(f"{prefix}Error - Brain files not found.")
        return

    # 2. Check if the user gave arguments (Single-Shot Mode)
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        response = process_input(user_query, vibe_data, legacy_data)
        print(f"{prefix}{response}")
        return

    # 3. Interactive Mode (The Conversation Loop)
    print(f"{prefix}Interactive session started. Type 'exit' to quit.")
    print("-" * 30)
    
    while True:
        # Use a cool custom prompt
        try:
            user_query = input(">>> ").strip()
        except EOFError: # Handles Ctrl+D
            break

        # Exit conditions
        if user_query.lower() in ["exit", "quit", "bye"]:
            print(f"{prefix}Session ended. See ya.")
            break
            
        if not user_query:
            continue

        # Process and Output
        response = process_input(user_query, vibe_data, legacy_data)
        print(f"{prefix}{response}")

if __name__ == "__main__":
    run()
