"""
exploratory_analysis.py

Summary tables for the exploratory analysis of the cleaned food recall data.
Code taken from Food_Recall_EDA.ipynb: Phase 6 (Exploratory Data Analysis),
sections 6.1 to 6.6. The charts for these tables are in data_visualization.py.

Needs:     data_cleaning.py (provides the cleaned dataset `clean_data`)
Provides:  product_counts, cause_counts, firm_counts, state_counts, channel_counts

Run:  python exploratory_analysis.py
"""

from data_cleaning import clean_data

# ======================================================================
# Phase 6: Exploratory Data Analysis
# ======================================================================
# --- 6.1 Product category analysis ---
print("\nRecalls by product category")
product_counts = clean_data["product_category"].value_counts()

print(product_counts)

# --- 6.2 Root cause analysis ---
print("\nRecalls by root cause")
cause_counts = clean_data["root_cause"].value_counts()

print(cause_counts)

# --- 6.3 Firm analysis ---
print("\nTop 15 recalling firms")
firm_counts = clean_data["recalling_firm"].value_counts()

print(firm_counts.head(15))

# --- 6.4 State analysis ---
print("\nTop 15 states")
state_counts = clean_data["state"].value_counts()

print(state_counts.head(15))

# --- 6.5 Notification channel analysis ---
print("\nTop notification channels")
channel_counts = clean_data["initial_firm_notification"].value_counts()

print(channel_counts.head(10))

# --- 6.6 Recall status, classification and timely classification ---
print("Recall Status")
print(clean_data["status"].value_counts())

print("\nClassification")
print(clean_data["classification"].value_counts())

print("\nTimely Classification")
print(clean_data["timely_classification"].value_counts())
