from collections import defaultdict
from decimal import Decimal, InvalidOperation

def flag_duplicates(rows):
    by_txid = defaultdict(list)
    for row in rows:
        if row["transaction_id"]:
            by_txid[row["transaction_id"]].append(row)
    repeated_ids = {key: group for key, group in by_txid.items() if len(group) > 1}
    for txid, group in repeated_ids.items():
        for row in group:
            row["duplicate_transaction_id"] = True
            row["issues"].append("repeated_transaction_id")
    by_signature = defaultdict(list)
    for row in rows:
        if row["customer_name"] and row["amount"] and row["transaction_date"] and row["order_id"]:
            try:
                positive = Decimal(row["amount"]) > 0
            except InvalidOperation:
                positive = False
            if positive:
                signature = (row["customer_name"].casefold(), row["amount"], row["transaction_date"], row["order_id"].casefold())
                by_signature[signature].append(row)
    possible_duplicate_groups = 0
    possible_duplicate_rows = 0
    for group in by_signature.values():
        if len(group) > 1:
            possible_duplicate_groups += 1
            group_id = f"LOOKALIKE-{possible_duplicate_groups:03d}"
            for row in group[1:]:
                row["possible_duplicate"] = True
                row["duplicate_group"] = group_id
                row["issues"].append("possible_duplicate_transaction")
                possible_duplicate_rows += 1
            group[0]["duplicate_group"] = group_id

    return repeated_ids, possible_duplicate_groups, possible_duplicate_rows
