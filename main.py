import sys
from bootstrap.responses_loader import load_all_data, load_settings
from bootstrap.on_start import get_prefix, system_check
from bootstrap.engine import process_input

def run():
    vibe_data, legacy_data = load_all_data()
    settings = load_settings()
    prefix = get_prefix()

    # Get terminal settings from YAML
    term_conf = settings.get('terminal_settings', {})
    prompt = term_conf.get('prompt_symbol', '>>> ')

    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        print(f"{prefix}{process_input(user_query, vibe_data, legacy_data)}")
        return

    print(f"{prefix}Interactive session. Type 'exit' to quit.")

    while True:
        try:
            user_query = input(prompt).strip() # Uses YAML prompt
        except EOFError: break
        if user_query.lower() in ["exit", "quit"]: break
        if not user_query: continue

        print(f"{prefix}{process_input(user_query, vibe_data, legacy_data)}")

if __name__ == "__main__":
    run()
