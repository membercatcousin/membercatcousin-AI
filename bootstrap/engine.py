import difflib
# Import your new real exceptions
from bootstrap.exceptions import TopicBlockedException, ResponseNotAvailableException

def process_input(user_input, vibe_data, legacy_data, settings):
    user_input = user_input.lower().strip()
    if not user_input: return "System online. Waiting for input..."

    # --- Layer 0: Security ---
    sec_conf = settings.get('security_settings', {})
    forbidden = sec_conf.get('forbidden_keywords', [])
    for word in forbidden:
        if word in user_input:
            # IT'S REAL NOW! We are raising an actual error.
            raise TopicBlockedException(word)

    # --- Layer 1: Algorithmic Vibe Match (Longest Wins) ---
    best_response = None
    longest_match_len = 0
    for entry in vibe_data:
        for keyword in entry["keywords"]:
            if keyword in user_input:
                if len(keyword) > longest_match_len:
                    longest_match_len = len(keyword)
                    best_response = entry["response"]

    if best_response:
        return best_response

    # --- Layer 2 & 3: Legacy + Typo ---
    if user_input in legacy_data:
        return legacy_data[user_input]

    best_match = None
    highest_ratio = 0.0
    for key in legacy_data.keys():
        ratio = difflib.SequenceMatcher(None, user_input, key).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = key

    if highest_ratio >= 0.6:
        return legacy_data[best_match]

    # If nothing is found, RAISE the other exception
    raise ResponseNotAvailableException()
