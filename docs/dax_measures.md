# DAX Measures Reference - Sales & Budget Analysis

This document details all explicit Data Analysis Expressions (DAX) created in the **Sales & Budget** Power BI model.

---

## 1. Core Measures

### Total Sales
Computes total realized revenue across all filtered sales transactions.
```dax
Sales = SUM(Sales[SalesAmount])
```
* **Format**: Currency (`₹ #,##0.00`)
* **Usage**: KPI card, bar charts, trend lines, top products/customers tables.

---

### Total Budget
Computes the aggregated revenue quota across all active product categories and time periods.
```dax
Budget = SUM(Budget[Budget])
```
* **Format**: Currency (`₹ #,##0.00`)
* **Usage**: KPI card, category comparisons, monthly target tracking.

---

### Budget Variance (Absolute)
Measures the absolute monetary deviation between realized sales revenue and budgeted target.
```dax
Variance = [Sales] - [Budget]
```
* **Format**: Currency (`₹ #,##0.00`)
* **Interpretation**:
  * `> 0`: Outperformed target (Budget surplus).
  * `< 0`: Underperformed target (Budget deficit).
* **Usage**: Variance KPI card, Variance by Category bar chart, Variance by Month column chart.

---

### Budget Variance Percentage
Computes the normalized percentage variance relative to the budget benchmark.
```dax
Variance % = DIVIDE([Variance], [Budget], 0)
```
* **Format**: Percentage (`0.00%`)
* **Interpretation**: Relative performance metric independent of absolute sales scale.
* **Usage**: Variance % KPI card.

---

## 2. Best Practices Implemented

1. **Explicit vs Implicit Measures**: All visual containers utilize explicit DAX measures rather than default column aggregations, ensuring predictable filter context propagation.
2. **Safe Division**: Utilized `DIVIDE()` with a fallback value `0` to prevent division-by-zero errors when evaluating subcategories with zero budget allocations.
3. **Star Schema Alignment**: Measures seamlessly slice across the `Calendar`, `Product`, `Customer`, and `Territories` dimension tables without requiring bi-directional cross-filtering.
