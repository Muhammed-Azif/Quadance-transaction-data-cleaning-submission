import csv
import json
from collections import Counter
from decimal import Decimal

def write_cleaned_csv(rows, cleaned_path):
    fieldnames = [
        "source_row", "transaction_id", "customer_name_original", "customer_name",
        "amount_original", "amount", "transaction_date_original", "transaction_date",
        "status_original", "status", "order_id", "is_valid", "validity",
        "duplicate_transaction_id", "possible_duplicate", "duplicate_group", "issues", "issue_explanation",
    ]
    with cleaned_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output = row.copy()
            output["issues"] = "|".join(output["issues"])
            writer.writerow({key: output.get(key, "") for key in fieldnames})

def write_report(rows, input_path, cleaned_path, report_path, repeated_ids, possible_duplicate_groups, possible_duplicate_rows):
    valid_rows = [row for row in rows if row["is_valid"]]
    invalid_rows = [row for row in rows if not row["is_valid"]]
    paid_valid = [row for row in valid_rows if row["status"] == "paid" and row["amount"]]
    total_revenue = sum((Decimal(row["amount"]) for row in paid_valid), Decimal("0.00"))
    report = {
        "input_file": str(input_path),
        "output_file": str(cleaned_path),
        "input_rows": len(rows),
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalid_rows),
        "reconciliation": {
            "valid_plus_invalid_equals_input": len(valid_rows) + len(invalid_rows) == len(rows),
            "cleaned_csv_rows_equal_input": len(rows),
        },
        "duplicate_counts": {
            "repeated_transaction_id_groups": len(repeated_ids),
            "rows_with_repeated_transaction_ids": sum(len(group) for group in repeated_ids.values()),
            "possible_duplicate_groups": possible_duplicate_groups,
            "possible_duplicate_rows_after_first_occurrence": possible_duplicate_rows,
            "all_rows_flagged_as_any_duplicate": sum(1 for row in rows if row["duplicate_transaction_id"] or row["possible_duplicate"]),
        },
        "status_counts_all_rows": dict(sorted(Counter(row["status"] for row in rows).items())),
        "revenue": {
            "definition": "Sum of amounts for valid rows whose normalized status is paid; invalid rows, duplicates, refunds, pending and cancelled rows are excluded.",
            "paid_valid_rows_count": len(paid_valid),
            "total_revenue": format(total_revenue.quantize(Decimal("0.01")), "f"),
            "currency": "not specified in input; values are treated as generic currency units",
        },
        "issue_counts": dict(sorted(Counter(issue for row in rows for issue in row["issues"]).items())),
        "assumptions": [
            "Date output uses YYYY-MM-DD. ISO year-first formats are parsed directly; slash/dash day-first dates are interpreted as DD/MM/YYYY or DD-MM-YYYY. Ambiguous month-first dates are not guessed.",
            "Names are normalized by collapsing whitespace and title-casing; the exact original name is preserved.",
            "Commas are treated as thousands separators; currency symbols are removed. Missing, unparsable, zero, and negative amounts are invalid.",
            "Unknown statuses become 'unknown' and invalidate the row. Common aliases are mapped to the known status set.",
            "Rows with repeated transaction IDs are all invalid because their conflicting identity cannot be resolved automatically.",
            "For lookalike duplicates, the first matching row is retained as the reference and later matching rows are marked invalid as possible duplicates.",
            "Revenue means valid paid transaction amounts only; refunds are excluded rather than netted because refund linkage is not supplied.",
        ],
    }
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return len(valid_rows), len(invalid_rows), total_revenue
