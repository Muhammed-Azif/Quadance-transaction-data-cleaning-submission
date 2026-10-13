KNOWN_STATUSES = {"paid", "pending", "cancelled", "refund"}
def normalize_status(value):
    raw = " ".join((value or "").split()).lower()
    aliases = {
        "complete": "paid", "completed": "paid", "success": "paid", "successful": "paid",
        "waiting": "pending", "in progress": "pending", "canceled": "cancelled",
        "refunded": "refund", "refunded payment": "refund",
    }
    normalized = aliases.get(raw, raw)
    if not normalized:
        return "unknown", "missing_status"
    if normalized not in KNOWN_STATUSES:
        return "unknown", "unknown_status"
    return normalized, ""



