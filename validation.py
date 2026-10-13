from cleaners.name import clean_name
from cleaners.dates import parse_date
from cleaners.amounts import parse_amount
from cleaners.statuses import normalize_status
def build_rows(source_rows):
    rows = []
    for index, source in enumerate(source_rows, start=2):
        original_name, normalized_name = clean_name(source.get("customer_name", ""))
        date_value, date_issue = parse_date(source.get("transaction_date", ""))
        amount_value, amount_issue = parse_amount(source.get("amount", ""))
        status_value, status_issue = normalize_status(source.get("status", ""))
        issues = []
        if not (source.get("transaction_id") or "").strip():
            issues.append("missing_transaction_id")
        if not normalized_name:
            issues.append("missing_customer_name")
        if date_issue:
            issues.append(date_issue)
        if amount_issue:
            issues.append(amount_issue)
        if status_issue:
            issues.append(status_issue)
        rows.append({
            "source_row": index,
            "transaction_id": (source.get("transaction_id") or "").strip(),
            "customer_name_original": original_name,
            "customer_name": normalized_name,
            "amount_original": (source.get("amount") or "").strip(),
            "amount": amount_value,
            "transaction_date_original": (source.get("transaction_date") or "").strip(),
            "transaction_date": date_value,
            "status_original": (source.get("status") or "").strip(),
            "status": status_value,
            "order_id": (source.get("order_id") or "").strip(),
            "duplicate_transaction_id": False,
            "possible_duplicate": False,
            "duplicate_group": "",
            "issues": issues,
        })
    return rows

def finalize_rows(rows):
    for row in rows:
        row["issues"] = list(dict.fromkeys(row["issues"]))
        row["is_valid"] = not row["issues"]
        row["validity"] = "valid" if row["is_valid"] else "invalid"
        row["issue_explanation"] = "; ".join(row["issues"])
    return rows


