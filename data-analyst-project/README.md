# Data Analyst Project: Sales Performance Insights

This is a beginner-friendly data analyst project that demonstrates a complete mini workflow:

1. Load sales data from CSV.
2. Clean and transform fields.
3. Calculate business KPIs.
4. Export results as machine-readable and stakeholder-friendly reports.

## Project Structure

- `data/sales_data.csv` — sample raw sales dataset.
- `src/analyze_sales.py` — analysis script (standard library only).
- `outputs/` — generated summary files.

## KPIs Calculated

- Total orders
- Total units sold
- Total revenue
- Average order value
- Revenue by region
- Revenue by product
- Revenue by month
- Top region and top product by revenue

## How to Run

From the repository root:

```bash
python3 data-analyst-project/src/analyze_sales.py
```

After execution, these files are created/updated:

- `data-analyst-project/outputs/summary.json`
- `data-analyst-project/outputs/monthly_revenue.csv`
- `data-analyst-project/outputs/report.md`

## Ideas to Extend

- Add profit margin and discount analysis.
- Build charts in a Jupyter notebook.
- Connect to a SQL database and automate weekly reporting.
- Convert script into a scheduled ETL pipeline.
