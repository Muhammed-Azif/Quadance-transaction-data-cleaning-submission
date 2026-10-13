def clean_name(value):
    original = value if value is not None else ""
    normalized = " ".join(original.split()).title()
    return original, normalized
