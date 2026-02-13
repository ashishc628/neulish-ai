def clamp(value, min_v, max_v):
    try:
        return max(min_v, min(float(value), max_v))
    except:
        return min_v

def normalize_10_to_5(value):
    try:
        value = clamp(value, 0, 10)
        return int(round((value / 10) * 4 + 1))
    except:
        return 3
