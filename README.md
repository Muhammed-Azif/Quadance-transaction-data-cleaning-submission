A Python program to clean and validate transaction records from 'input.csv'.

It generates:
 'cleaned.csv' – processed transactions with validity and issue details.
'report.json' – summary of valid/invalid rows, duplicates, and revenue.
# How to run

Requires Python 3.10 or above. No external packages are needed.

bash
python clean_transactions.py Input/input.csv Output/cleaned.csv Output/report.json

Keep `input.csv' in the project folder before running.

# Project Files

 'clean_transactions.py' – Main program
 'validation.py' – Row validation
 'duplicates.py' – Duplicate detection
 'outputs.py' – CSV and JSON generation
 'cleaners/' – Name, date, amount, and status cleaning functions

# Cleaning Rules and Assumptions

* Names are normalized by removing extra spaces while preserving the original.
* Dates are converted to 'YYYY-MM-DD'. Ambiguous slash/dash dates follow the day-first convention.
* Amounts are cleaned using 'Decimal'. Missing, invalid, zero, and negative amounts are flagged.
* Statuses are normalized to paid, pending, cancelled, or refund.
* Repeated transaction IDs are marked invalid.
* Possible duplicates are identified using customer name, amount, date, and order ID.
* All input rows are retained, including invalid transactions.
* Revenue includes only valid paid transactions. Refunds are excluded.

## Edge Case

Names such as `Meera Nair` and `Meera   Nair` are normalized before checking for possible duplicates.
