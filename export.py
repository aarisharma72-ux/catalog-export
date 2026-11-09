import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

from catalog import fetch_products, product_rows
from settings import EXPORT_COLUMNS


def main():
    parser = argparse.ArgumentParser(description="Export the product catalog to CSV")
    parser.add_argument("--input", type=Path)
    parser.add_argument(
        "--output", type=Path, default=Path("exports") / f"catalog-{date.today()}.csv"
    )
    parser.add_argument("--active-only", action="store_true")
    args = parser.parse_args()

    try:
        if args.input:
            with args.input.open(encoding="utf-8-sig") as source:
                payload = json.load(source)
        else:
            payload = fetch_products()
        rows = list(product_rows(payload, active_only=args.active_only))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=EXPORT_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {len(rows)} products to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
