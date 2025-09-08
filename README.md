# Automated Data Cleaning & Reporting Workflow

## Overview
This project is a full-fledged automation pipeline that takes messy raw data files, cleans them intelligently, extracts actionable insights through SQL, and serves professional visuals via Power BI — all without manual effort after setup.
It’s designed to help anyone dealing with recurring raw data cleaning and reporting tasks, so they can focus on decision-making, not data wrangling.

## Why This Project?

Manually cleaning data, running SQL queries, and updating dashboards every week is time-consuming, error-prone, and repetitive.
This project solves that by automating the entire flow end-to-end — making data handling effortless and insights instant.

## 🛠️ Tech Stack

1. Python → Data cleaning, file detection, logging
2. SQLite → Central database storing cleaned data + query results
3. SQL → Prebuilt queries to extract meaningful insights
4. ODBC → Connecting SQLite DB to Power BI
5. Power BI → Interactive, multi-page dashboards with automatic refresh
6. Logging System → Tracks each pipeline run for full transparency 📋

## ⚡ Project Structure

Finance Automation Project/
-├── input/               ← Drop raw Excel files here (General-Ledger.xlsx, Budget-Forecast.xlsx)
-├── cleaned/             ← Cleaned Excel reports with timestamps are saved here
-├── pipeline.py          ← Main automation script
-├── finance.db           ← SQLite database (auto-generated and updated)
-├── pipeline_logs/       ← Logs for every run (success, errors, timestamps)
-├── visuals/             ← Add dashboard screenshots here
-├── README.md            ← Project overview & guide (this file)

## How It Works
 
1️⃣ Auto Data Pull & Clean:

- Every week, the pipeline detects new raw Excel files in the input/ folder.
- Python cleans messy data intelligently (fixes types, removes duplicates, handles missing values, etc.).
- Saves cleaned reports in cleaned/ folder (with timestamp).

2️⃣ Database Update:

- Cleaned data is loaded into a centralized SQLite database (finance.db).
- Prebuilt SQL queries run automatically to calculate key insights:
- Spend trends by department
- Profit vs cost comparisons
- Monthly patterns
- Forecast vs actual comparisons

3️⃣ Visualization in Power BI:

- Database connects to Power BI via ODBC.
- Power BI refreshes visuals automatically as the DB updates.
- Interactive dashboards show clean, actionable insights.

4️⃣ Pipeline Logs:

- Every time the pipeline runs, a log is generated:
- Timestamp: 2025-09-08 02:00:01  
- Status: SUCCESS  
- New files detected: General-Ledger.xlsx, Budget-Forecast.xlsx  
- Cleaned files saved → finance.db updated ✅
  
Logs are saved in pipeline_logs/ for easy monitoring 🔧

## Visual Preview

### 📊 Page 1 – High-Level Financial Overview

<img width="1067" height="800" alt="image" src="https://github.com/user-attachments/assets/b68c0d16-9804-4e42-a3c2-bb16d1c7ae52" />

### 📊 Page 2 – Department Spend vs Budget Comparison

<img width="1075" height="808" alt="image" src="https://github.com/user-attachments/assets/377ae4d6-bf96-4604-a9f4-fff07c48caa4" />

### 📊 Page 3 – Monthly Trends

<img width="959" height="723" alt="image" src="https://github.com/user-attachments/assets/b9b8bca0-0fe3-4ccf-a829-ed78c45adb97" />

### 📊 Page 4 – Forecast vs Actual Insights

<img width="955" height="714" alt="image" src="https://github.com/user-attachments/assets/076a3eaa-a6bb-4a44-bed8-7eaf5eaae367" />


## How to Run the Pipeline Locally

1. Place raw Excel files in input/:
- General-Ledger.xlsx
- Budget-Forecast.xlsx

2. Run the automation pipeline:

- python pipeline.py
- Cleaned reports will appear in cleaned/.
- SQLite DB will be updated with new data and queries.
- Logs will appear in pipeline_logs/.
- Power BI will automatically pick up the latest DB state (via ODBC) and refresh visuals.

## Final Thoughts

This project is built to make data processing easier, smarter, and fully automated.
Just drop your raw files → and get clean visuals + insights automatically.

Feel free to explore, try it yourself, and drop a star if you like ⭐
