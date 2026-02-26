from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "sales_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def load_rows(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["date"] = datetime.strptime(row["date"], "%Y-%m-%d").date()
            row["units_sold"] = int(row["units_sold"])
            row["unit_price"] = float(row["unit_price"])
            row["revenue"] = row["units_sold"] * row["unit_price"]
            rows.append(row)
    return rows


def compute_summary(rows: list[dict]) -> dict:
    total_revenue = sum(r["revenue"] for r in rows)
    total_units = sum(r["units_sold"] for r in rows)
    avg_order_value = total_revenue / len(rows)

    by_region = defaultdict(float)
    by_product = defaultdict(float)
    by_month = defaultdict(float)

    for r in rows:
        by_region[r["region"]] += r["revenue"]
        by_product[r["product"]] += r["revenue"]
        by_month[r["date"].strftime("%Y-%m")] += r["revenue"]

    best_region = max(by_region.items(), key=lambda item: item[1])
    best_product = max(by_product.items(), key=lambda item: item[1])

    return {
        "total_orders": len(rows),
        "total_units_sold": total_units,
        "total_revenue": round(total_revenue, 2),
        "average_order_value": round(avg_order_value, 2),
        "top_region": {"name": best_region[0], "revenue": round(best_region[1], 2)},
        "top_product": {"name": best_product[0], "revenue": round(best_product[1], 2)},
        "revenue_by_region": {k: round(v, 2) for k, v in sorted(by_region.items())},
        "revenue_by_product": {k: round(v, 2) for k, v in sorted(by_product.items())},
        "revenue_by_month": {k: round(v, 2) for k, v in sorted(by_month.items())},
    }


def write_outputs(summary: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_file = OUTPUT_DIR / "summary.json"
    summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    monthly_file = OUTPUT_DIR / "monthly_revenue.csv"
    with monthly_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "revenue"])
        for month, revenue in summary["revenue_by_month"].items():
            writer.writerow([month, revenue])

    report_file = OUTPUT_DIR / "report.md"
    report = f"""# Sales Performance Snapshot

## Core Metrics
- Total orders: **{summary['total_orders']}**
- Total units sold: **{summary['total_units_sold']}**
- Total revenue: **${summary['total_revenue']:,}**
- Average order value: **${summary['average_order_value']:,}**

## Highlights
- Highest-performing region: **{summary['top_region']['name']}** (${summary['top_region']['revenue']:,})
- Highest-performing product: **{summary['top_product']['name']}** (${summary['top_product']['revenue']:,})

## Monthly Revenue
"""
    for month, revenue in summary["revenue_by_month"].items():
        report += f"- {month}: ${revenue:,}\n"

    report_file.write_text(report, encoding="utf-8")


def main() -> None:
    rows = load_rows(DATA_FILE)
    summary = compute_summary(rows)
    write_outputs(summary)
    print("Analysis complete. Files written to:")
    print(f"- {OUTPUT_DIR / 'summary.json'}")
    print(f"- {OUTPUT_DIR / 'monthly_revenue.csv'}")
    print(f"- {OUTPUT_DIR / 'report.md'}")


if __name__ == "__main__":
    main()
