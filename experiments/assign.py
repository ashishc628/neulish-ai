def assign_variant(user_id: str):
    return "A" if hash(user_id) % 2 == 0 else "B"
