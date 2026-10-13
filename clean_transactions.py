import csv
from decimal import Decimal
import sys
from pathlib import Path
from validation import build_rows, finalize_rows
from duplicates import flag_duplicates
from outputs import write_cleaned_csv, write_report

def main():
    input_path = Path(sys.argv[1] if len(sys.argv) > 1 else "input.csv")
    cleaned_path = Path(sys.argv[2] if len(sys.argv) > 2 else "cleaned.csv")
    report_path = Path(sys.argv[3] if len(sys.argv) > 3 else "report.json")

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"transaction_id", "customer_name", "amount", "transaction_date", "status", "order_id"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise SystemExit(f"Input CSV must contain columns: {', '.join(sorted(required))}")
        source_rows = list(reader)

    rows = build_rows(source_rows)
    repeated_ids, possible_duplicate_groups, possible_duplicate_rows = flag_duplicates(rows)
    finalize_rows(rows)
    write_cleaned_csv(rows, cleaned_path)
    valid_count, invalid_count, total_revenue = write_report(
        rows, input_path, cleaned_path, report_path,
        repeated_ids, possible_duplicate_groups, possible_duplicate_rows
    )

    print(f"Read {len(rows)} rows from {input_path}")
    print(f"Valid: {valid_count} | Invalid: {invalid_count}")
    print(f"Repeated transaction ID groups: {len(repeated_ids)}")
    print(f"Possible duplicate groups: {possible_duplicate_groups}")
    print(f"Total revenue (valid paid rows): {total_revenue.quantize(Decimal('0.01'))}")
    print(f"Created: {cleaned_path} and {report_path}")


if __name__ == "__main__":
    main()
