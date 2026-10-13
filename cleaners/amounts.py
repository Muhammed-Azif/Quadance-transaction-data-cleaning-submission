import re
from decimal import Decimal, InvalidOperation
MISSING = {"", "n/a", "na", "null", "none", "-"}

def parse_amount(value):
    raw = (value or "").strip()
    if raw.lower() in MISSING:
        return "", "missing_amount"
    cleaned = raw.replace(",", "").replace("₹", "").replace("$", "").replace("€", "")
    cleaned = re.sub(r"\s+", "", cleaned)
    try:
        amount = Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return "", "invalid_amount_format"
    if not amount.is_finite():
        return "", "invalid_amount_format"
    if amount <= 0:
        return format(amount, "f"), "amount_not_positive"
    return format(amount.quantize(Decimal("0.01")), "f"), ""


