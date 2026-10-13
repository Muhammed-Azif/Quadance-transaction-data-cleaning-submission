from datetime import datetime
MISSING = {"", "n/a", "na", "null", "none", "-"}
def parse_date(value):
    raw = (value or "").strip()
    if raw.lower() in MISSING:
        return "", "missing_date"
    preferred = ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y")
    for fmt in preferred:
        try:
            return datetime.strptime(raw, fmt).date().isoformat(), ""
        except ValueError:
            pass
    for fmt in ("%m/%d/%Y", "%m-%d-%Y"):
        try:
            parsed = datetime.strptime(raw, fmt).date()
            day_first_possible = False
            for dmy_fmt in ("%d/%m/%Y", "%d-%m-%Y"):
                try:
                    datetime.strptime(raw, dmy_fmt)
                    day_first_possible = True
                    break
                except ValueError:
                    continue
            if not day_first_possible:
                return parsed.isoformat(), ""
        except ValueError:
            pass
    return "", "uninterpretable_date"
