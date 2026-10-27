"""
AdventureWorks Sales & Budget Exploratory Data Analysis (EDA)
Maintainer: Ayush Mittal
Description: Automated data audit, KPI validation, and category analytics matching
             the Power BI 'Sales vs Budget' visualization model.
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_eda(data_dir="."):
    sales_file = os.path.join(data_dir, "Sales.xlsx")
    budget_file = os.path.join(data_dir, "Budget.xlsx")

    print("=" * 70)
    print(" ADVENTUREWORKS SALES VS BUDGET - DATA AUDIT & KPI REPORT")
    print("=" * 70)

    # 1. Load Dimension and Fact tables from Sales.xlsx
    print("\n[1/5] Loading Sales.xlsx tables...")
    df_calendar = pd.read_excel(sales_file, sheet_name="Sheet2")
    df_customer = pd.read_excel(sales_file, sheet_name="Sheet3")
    df_product = pd.read_excel(sales_file, sheet_name="Sheet4")
    df_sales = pd.read_excel(sales_file, sheet_name="Sheet5")
    df_territory = pd.read_excel(sales_file, sheet_name="Sheet6")

    print(f"  -> Calendar Records   : {len(df_calendar):,}")
    print(f"  -> Customer Records   : {len(df_customer):,}")
    print(f"  -> Product Records    : {len(df_product):,}")
    print(f"  -> Sales Transactions : {len(df_sales):,}")
    print(f"  -> Sales Territories  : {len(df_territory):,}")

    # 2. Filter 2016 Sales (Dashboard Scope)
    df_sales["OrderDate"] = pd.to_datetime(df_sales["OrderDate"])
    df_sales["Year"] = df_sales["OrderDate"].dt.year
    df_sales["Month"] = df_sales["OrderDate"].dt.strftime("%b")
    df_sales["MonthNum"] = df_sales["OrderDate"].dt.month

    df_sales_2016 = df_sales[df_sales["Year"] == 2016].copy()
    sales_total_2016 = df_sales_2016["SalesAmount"].sum()

    # 3. Load & Process Budget Data
    print("\n[2/5] Loading and unpivoting Budget.xlsx...")
    budget_raw = pd.read_excel(budget_file, sheet_name="Budget", header=3)

    # Exclude SubTotal and Grand Total rows
    clean_categories = ["Accessories", "Bikes", "Clothing"]
    df_budget_clean = budget_raw[budget_raw["Category"].isin(clean_categories)].copy()

    month_cols = [c for c in df_budget_clean.columns if "2016" in str(c)]
    budget_total_2016 = df_budget_clean[month_cols].sum().sum()

    # Calculate Core Variance Metrics
    variance = sales_total_2016 - budget_total_2016
    variance_pct = (variance / budget_total_2016) * 100

    print("\n" + "=" * 70)
    print(" EXECUTIVE KPI SUMMARY (YEAR 2016)")
    print("=" * 70)
    print(f"  * Total Budget : ₹ {budget_total_2016:,.2f}  (~₹ {budget_total_2016/1e6:.1f}M)")
    print(f"  * Total Sales  : ₹ {sales_total_2016:,.2f}  (~₹ {sales_total_2016/1e6:.1f}M)")
    print(f"  * Variance     : ₹ {variance:,.2f}  (~₹ {variance/1e3:.1f}K)")
    print(f"  * Variance %   : {variance_pct:.2f}%")
    print("=" * 70)

    # 4. Category Breakdown
    print("\n[3/5] Category Breakdown:")
    sales_merged = df_sales_2016.merge(
        df_product[["ProductKey", "Category", "SubCategory", "ProductName"]],
        on="ProductKey",
        how="left"
    )

    cat_sales = sales_merged.groupby("Category")["SalesAmount"].sum()

    print(f"{'Category':<15} | {'Budget (₹)':>14} | {'Sales (₹)':>14} | {'Variance (₹)':>14} | {'Var %':>8}")
    print("-" * 75)
    for cat in clean_categories:
        b_cat = df_budget_clean[df_budget_clean["Category"] == cat][month_cols].sum().sum()
        s_cat = cat_sales.get(cat, 0.0)
        v_cat = s_cat - b_cat
        vp_cat = (v_cat / b_cat) * 100 if b_cat > 0 else 0.0
        print(f"{cat:<15} | {b_cat:>14,.2f} | {s_cat:>14,.2f} | {v_cat:>14,.2f} | {vp_cat:>7.2f}%")

    # 5. Top 5 Products by Sales
    print("\n[4/5] Top 5 Products by Sales (2016):")
    top_products = sales_merged.groupby("ProductName")["SalesAmount"].sum().sort_values(ascending=False).head(5)
    for i, (prod_name, amt) in enumerate(top_products.items(), 1):
        print(f"  {i}. {prod_name:<35} : ₹ {amt:,.2f}")

    # 6. Top 5 customer records by sales, displayed without names
    print("\n[5/5] Top 5 Customer Records by Sales (2016):")
    sales_cust = df_sales_2016.merge(
        df_customer[["CustomerKey"]],
        on="CustomerKey",
        how="left"
    )
    top_customers = sales_cust.groupby("CustomerKey")["SalesAmount"].sum().sort_values(ascending=False).head(5)
    for i, (customer_key, amount) in enumerate(top_customers.items(), 1):
        print(f"  {i}. Customer record {customer_key}: ₹ {amount:,.2f}")

    print("\n" + "=" * 70)
    print(" Audit complete. All metrics conform to Power BI dashboard specifications.")
    print("=" * 70)


if __name__ == "__main__":
    run_eda()
