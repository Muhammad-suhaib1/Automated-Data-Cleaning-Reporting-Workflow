# pipeline.py
import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime

def check_new_files():
    ledger_path = "input/General-Ledger.xlsx"
    budget_path = "input/Budget-Forecast.xlsx"
    
    if os.path.exists(ledger_path) and os.path.exists(budget_path):
        return ledger_path, budget_path
    
    print("⚠️ No new input files found in input/")
    return None, None

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(r"C:\Users\muham\Desktop\Finance Automation Project\pipeline.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

log("Pipeline started.")

ledger_path, budget_path = check_new_files()
log(f"Using ledger input file: {ledger_path}")
log(f"Using budget input file: {budget_path}")


# Data cleaning steps...
# After cleaned files are written:
log(f"Saved cleaned files to cleaned/ folder.")

# At the end
log("Pipeline completed successfully.")

# General Cleaning Functions

def remove_whitespace(df):
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()
    return df

def handle_missing(df, strategy="drop", fill_value=None):
    if strategy == "drop":
        df = df.dropna()
    elif strategy == "mean":
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].mean())
    elif strategy == "median":
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
    elif strategy == "mode":
        for col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])
    elif strategy == "constant" and fill_value is not None:
        df = df.fillna(fill_value)
    return df

def fix_dtypes(df):
    for col in df.columns:
        if "date" in col.lower():
            df.loc[:, col] = pd.to_datetime(df[col], errors="coerce")
        elif df[col].dtype == "object":
            try:
                df.loc[:, col] = pd.to_numeric(df[col])
            except Exception:
                pass
    return df

def remove_duplicates(df):
    return df.drop_duplicates()

# Custom Hardcoded Cleaning

def clean_ledger(df):
    df = remove_whitespace(df)
    df = handle_missing(df, strategy="drop")
    df = fix_dtypes(df)
    df = remove_duplicates(df)

    # Hardcoded rules
    if "Amount" in df.columns:
        df["Amount"] = df["Amount"].astype(float)
    if "Dept" in df.columns:
        df.loc[:, "Dept"] = df["Dept"].astype(str).str.upper()

    return df

def clean_budget(df):
    df = remove_whitespace(df)
    df = handle_missing(df, strategy="drop")
    df = fix_dtypes(df)
    df = remove_duplicates(df)

    if "Dept" in df.columns:
        df.loc[:, "Dept"] = df["Dept"].astype(str).str.upper()
    for col in ["BudgetUSD", "ForecastUSD", "ActualUSD", "VarianceUSD"]:
        if col in df.columns:
            df.loc[:, col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

# 3. Loading SQLite DB Starts here

def load_to_sqlite(ledger_df, budget_df, db_name="finance.db"):
    conn = sqlite3.connect(db_name)

    ledger_df.to_sql("ledger", conn, if_exists="replace", index=False)
    budget_df.to_sql("budget", conn, if_exists="replace", index=False)

    # sanity check
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print("✅ Tables in DB:", tables["name"].tolist())

    conn.close()

# Running Some Queries (For getting some insights directly in tabular form if we need to present numbers and not just visuals, more queries can we added here )

def save_query_results(db_name="finance.db"):
    conn = sqlite3.connect(db_name)

    queries = {
        "q_total_spend_by_dept": """
            SELECT Dept, SUM(Debit) AS Total_Spend
            FROM ledger
            GROUP BY Dept
            ORDER BY Total_Spend DESC;
        """,
        "q_total_spend_by_costcenter": """
            SELECT CostCenter, SUM(Debit) AS Total_Spend
            FROM ledger
            GROUP BY CostCenter
            ORDER BY Total_Spend DESC;
        """,
        "q_revenue_by_dept": """
            SELECT Dept, SUM(Credit) AS Total_Revenue
            FROM ledger
            GROUP BY Dept
            ORDER BY Total_Revenue DESC;
        """,
        "q_revenue_by_costcenter": """
            SELECT CostCenter, SUM(Credit) AS Total_Revenue
            FROM ledger
            GROUP BY CostCenter
            ORDER BY Total_Revenue DESC;
        """,
        "q_net_profit_by_dept": """
            SELECT Dept, SUM(Credit) - SUM(Debit) AS Net_Profit
            FROM ledger
            GROUP BY Dept
            ORDER BY Net_Profit DESC;
        """,
        "q_monthly_spend_trend": """
            SELECT strftime('%Y-%m', TxnDate) AS Month,
                   SUM(Debit) AS Total_Spend
            FROM ledger
            GROUP BY Month
            ORDER BY Month;
        """,
        "q_monthly_revenue_trend": """
            SELECT strftime('%Y-%m', TxnDate) AS Month,
                   SUM(Credit) AS Total_Revenue
            FROM ledger
            GROUP BY Month
            ORDER BY Month;
        """,
        "q_actual_vs_budget_by_dept": """
            SELECT b.FiscalYear, b.Dept,
                   SUM(l.Debit) AS Actual_Spend,
                   SUM(b.BudgetUSD) AS Budget,
                   SUM(b.BudgetUSD) - SUM(l.Debit) AS Variance
            FROM budget b
            LEFT JOIN ledger l ON b.Dept = l.Dept
            GROUP BY b.FiscalYear, b.Dept;
        """,
        "q_forecast_accuracy_by_dept": """
            SELECT Dept,
                   SUM(ForecastUSD) AS Total_Forecast,
                   SUM(ActualUSD) AS Total_Actual,
                   (SUM(ActualUSD) - SUM(ForecastUSD)) AS Forecast_Error
            FROM budget
            GROUP BY Dept;
        """,
        "q_top_expense_accounts": """
            SELECT AccountName, SUM(Debit) AS Total_Expense
            FROM ledger
            GROUP BY AccountName
            ORDER BY Total_Expense DESC
            LIMIT 10;
        """,
        "q_currency_mix": """
            SELECT Currency,
                   SUM(Debit) AS Total_Spend,
                   SUM(Credit) AS Total_Revenue
            FROM ledger
            GROUP BY Currency
            ORDER BY Total_Revenue DESC;
        """
    }

    for table_name, sql in queries.items():
        df = pd.read_sql(sql, conn)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✅ Saved {table_name} to DB")

    conn.close()


# 4. Run Pipeline

def main():
    ledger_path, budget_path = check_new_files()

    if not ledger_path or not budget_path:
        print("🚫 Exiting pipeline. No new files found.")
        return

    ledger = pd.read_excel(ledger_path)
    budget = pd.read_excel(budget_path)

    ledger_clean = clean_ledger(ledger)
    budget_clean = clean_budget(budget)

    print("Ledger Shape Before:", ledger.shape, "After:", ledger_clean.shape)
    print("Budget Shape Before:", budget.shape, "After:", budget_clean.shape)

    base_path = r"C:\Users\muham\Desktop\Finance Automation Project"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_ledger_file = os.path.join(base_path, "cleaned", f"General-Ledger-Cleaned_{timestamp}.xlsx")
    output_budget_file = os.path.join(base_path, "cleaned", f"Budget-Forecast-Cleaned_{timestamp}.xlsx")

    print(f"Saving cleaned ledger to: {output_ledger_file}")
    log(f"Saving cleaned ledger to: {output_ledger_file}")

    ledger_clean.to_excel(output_ledger_file, index=False)

    print(f"Saving cleaned budget to: {output_budget_file}")
    log(f"Saving cleaned budget to: {output_budget_file}")

    budget_clean.to_excel(output_budget_file, index=False)




    load_to_sqlite(ledger_clean, budget_clean)
    save_query_results("finance.db")

    print("🚀 Pipeline complete! Database refreshed: finance.db")


if __name__ == "__main__":
    main()