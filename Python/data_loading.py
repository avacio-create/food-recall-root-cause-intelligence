"""
data_loading.py

Loads the raw FDA food enforcement dataset, inspects it and assesses its quality.
Code taken from Food_Recall_EDA.ipynb: Phase 1 (Data Acquisition),
Phase 2 (Initial Data Inspection) and Phase 3 (Data Quality Assessment).

Provides:  data  -> the raw dataset, every column read as text

Run:  python data_loading.py
"""

import pandas as pd

# Update this path if the file is stored somewhere else
DATA_PATH = r"F:\Anudip Proj\food\food_enforcement_raw.csv"

# ======================================================================
# Phase 1: Data Acquisition
# ======================================================================
# Load the food recall dataset
# dtype=str reads every column as text, so dates like 20240115 are not changed into numbers
data = pd.read_csv(DATA_PATH, dtype=str)

print("Dataset loaded successfully.")
print("Dataset Shape:", data.shape)

# ======================================================================
# Phase 2: Initial Data Inspection
# ======================================================================
# --- Preview the first rows ---
print("\nFirst rows")
print(data.head())

# --- Dataset dimensions and column names ---
print("Number of Rows:", data.shape[0])
print("Number of Columns:", data.shape[1])

print("\nColumn Names:")
print(list(data.columns))

# --- Data types and non-null counts ---
data.info()

# --- Descriptive statistics (count, unique values, most common value) ---
print("\nDescriptive statistics")
print(data.describe().T)

# ======================================================================
# Phase 3: Data Quality Assessment
# ======================================================================
# --- Missing values in every column ---
print("\nMissing values in every column")
missing_values = data.isnull().sum()

missing_percentage = (
    data.isnull().sum() / len(data) * 100
).round(2)

missing_summary = pd.DataFrame({
    "Missing Values": missing_values,
    "Missing Percentage": missing_percentage
})

print(missing_summary)

# --- Duplicate rows ---
print("Number of duplicate rows:", data.duplicated().sum())

# --- Duplicated recall identifiers ---
print("Total Recall Records:", len(data))
print("Unique Recall Numbers:", data["recall_number"].nunique())
print("Duplicate Recall Numbers:", data["recall_number"].duplicated().sum())

# --- Inconsistencies in categorical columns ---
print(data["classification"].value_counts(dropna=False))
print()
print(data["status"].value_counts(dropna=False))
print()
print(data["voluntary_mandated"].value_counts(dropna=False))
print()
print(data["state"].value_counts(dropna=False).head(10))

# --- Inconsistencies in date columns ---
# Dates are written as YYYYMMDD. A value that cannot be converted is invalid (for example 00000000)
date_columns = [
    "recall_initiation_date",
    "center_classification_date",
    "termination_date",
    "report_date"
]

for column in date_columns:
    converted = pd.to_datetime(data[column], format="%Y%m%d", errors="coerce")
    invalid_dates = (converted.isnull() & data[column].notnull()).sum()
    print(column, "-> invalid date values:", invalid_dates)
