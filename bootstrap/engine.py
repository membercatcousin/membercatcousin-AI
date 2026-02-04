import difflib

def process_input(user_input, vibe_data, legacy_data):
    user_input = user_input.lower().strip()
    if not user_input: return "System online. Waiting for input..."

    # Layer 1: Algorithmic Vibe Match (Keywords)
    for entry in vibe_data:
        for keyword in entry["keywords"]:
            if keyword in user_input:
                return entry["response"]

    # Layer 2: Legacy Direct Match
    if user_input in legacy_data:
        return legacy_data[user_input]

    # Layer 3: Silent Typo Handler (60% Similarity - Legacy Only)
    best_match = None
    highest_ratio = 0.0
    for key in legacy_data.keys():
        ratio = difflib.SequenceMatcher(None, user_input, key).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = key

    if highest_ratio >= 0.6:
        return legacy_data[best_match] # Silent fix - no annoying text
                
    return "ResponseNotAvailableException"
