"""
data_visualization.py

All charts of the project, merged into one file.
Code taken from Food_Recall_EDA.ipynb: the charts of Phase 6 (Exploratory Data
Analysis, 6.1 to 6.5) and all of Phase 7 (Comparative Data Visualization, 7.1 to 7.6).

Needs:     data_cleaning.py (clean_data) and exploratory_analysis.py (the count tables)

Run:  python data_visualization.py
"""

import pandas as pd
import matplotlib.pyplot as plt

from data_cleaning import clean_data
from exploratory_analysis import (
    product_counts,
    cause_counts,
    firm_counts,
    state_counts,
    channel_counts,
)

# ======================================================================
# Part 1: Exploratory charts (Phase 6)
# ======================================================================
# --- 6.1 Recalls by product category ---
plt.figure(figsize=(12, 6))

plt.bar(
    product_counts.index,
    product_counts.values
)

plt.xlabel("Product Category")
plt.ylabel("Number of Recalls")
plt.title("Recalls by Product Category")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# --- 6.2 Recalls by root cause ---
plt.figure(figsize=(12, 7))

plt.barh(
    cause_counts.index[::-1],
    cause_counts.values[::-1]
)

plt.xlabel("Number of Recalls")
plt.ylabel("Root Cause")
plt.title("Recalls by Root Cause")

plt.tight_layout()
plt.show()

# --- 6.3 Top firms by recall volume ---
top_firms = firm_counts.head(10)

plt.figure(figsize=(12, 6))

plt.bar(
    top_firms.index,
    top_firms.values
)

plt.xlabel("Recalling Firm")
plt.ylabel("Number of Recalls")
plt.title("Top Firms by Recall Volume")

plt.xticks(rotation=75, ha="right")
plt.tight_layout()
plt.show()

# --- 6.4 Top states by recall volume ---
top_states = state_counts.head(15)

plt.figure(figsize=(12, 6))

plt.bar(
    top_states.index,
    top_states.values
)

plt.xlabel("State")
plt.ylabel("Number of Recalls")
plt.title("Top States by Recall Volume")

plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.show()

# --- 6.5 Top notification channels ---
top_channels = channel_counts.head(8)

plt.figure(figsize=(12, 6))

plt.barh(
    top_channels.index[::-1],
    top_channels.values[::-1]
)

plt.xlabel("Number of Recalls")
plt.ylabel("How the Firm Notified Customers")
plt.title("Top Notification Channels")

plt.tight_layout()
plt.show()

# ======================================================================
# Part 2: Comparative charts (Phase 7)
# ======================================================================
# Recalls with no classification days ("Not Available") are left out of the
# timely-classification charts.

# --- 7.1 Product category vs timely classification ---
timely_data = clean_data[clean_data["timely_classification"] != "Not Available"]

product_timely = pd.crosstab(
    timely_data["product_category"],
    timely_data["timely_classification"],
    normalize="index"
) * 100

top_products = timely_data["product_category"].value_counts().head(8).index

product_timely = product_timely.loc[top_products]

product_timely.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 7)
)

plt.title("Timely Classification by Product Category", fontsize=15, fontweight="bold")
plt.xlabel("Product Category")
plt.ylabel("Percentage of Recalls (%)")

plt.xticks(rotation=45, ha="right")

plt.legend(title="Classified Within Limit", bbox_to_anchor=(1.02, 1), loc="upper left")

plt.tight_layout()
plt.show()

# --- 7.2 Product category vs recall status ---
product_status = pd.crosstab(
    clean_data["product_category"],
    clean_data["status"]
)

top_products = clean_data["product_category"].value_counts().head(8).index

product_status = product_status.loc[top_products]

product_status.plot(
    kind="bar",
    stacked=True,
    figsize=(13, 7)
)

plt.title("Recall Status Across Product Categories", fontsize=15, fontweight="bold")
plt.xlabel("Product Category")
plt.ylabel("Number of Recalls")

plt.xticks(rotation=45, ha="right")

plt.legend(title="Recall Status", bbox_to_anchor=(1.02, 1), loc="upper left")

plt.tight_layout()
plt.show()

# --- 7.3 Root cause vs recall status ---
cause_status = pd.crosstab(
    clean_data["root_cause"],
    clean_data["status"]
)

cause_status.plot(
    kind="bar",
    stacked=True,
    figsize=(13, 7)
)

plt.title("Recall Status Across Root Causes", fontsize=15, fontweight="bold")
plt.xlabel("Root Cause")
plt.ylabel("Number of Recalls")

plt.xticks(rotation=45, ha="right")

plt.legend(title="Recall Status", bbox_to_anchor=(1.02, 1), loc="upper left")

plt.tight_layout()
plt.show()

# --- 7.4 Product category vs classification duration ---
average_days = (
    clean_data
    .groupby("product_category")["classification_days"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 7))

plt.barh(
    average_days.index[::-1],
    average_days.values[::-1]
)

plt.title("Product Categories by Average Days to FDA Classification", fontsize=15, fontweight="bold")
plt.xlabel("Average Classification Time (Days)")
plt.ylabel("Product Category")

plt.tight_layout()
plt.show()

# --- 7.5 Recall year vs recall volume ---
year_counts = clean_data["recall_year"].value_counts().sort_index()

plt.figure(figsize=(12, 6))

plt.bar(
    year_counts.index.astype(int).astype(str),
    year_counts.values
)

plt.xlabel("Recall Year")
plt.ylabel("Number of Recalls")
plt.title("Recall Volume by Year (the latest year may be incomplete)")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- 7.6 Notification channel vs timely classification ---
channel_timely = pd.crosstab(
    timely_data["initial_firm_notification"],
    timely_data["timely_classification"],
    normalize="index"
) * 100

top_channels = timely_data["initial_firm_notification"].value_counts().head(5).index

channel_timely = channel_timely.loc[top_channels]

channel_timely.plot(
    kind="barh",
    stacked=True,
    figsize=(12, 6)
)

plt.title("Timely Classification by Notification Channel", fontsize=15, fontweight="bold")
plt.xlabel("Percentage of Recalls (%)")
plt.ylabel("Notification Channel")

plt.legend(title="Classified Within Limit", bbox_to_anchor=(1.02, 1), loc="upper left")

plt.tight_layout()
plt.show()
