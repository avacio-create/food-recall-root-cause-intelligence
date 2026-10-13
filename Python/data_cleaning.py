"""
data_cleaning.py

Cleans the raw data, creates the derived features, validates the result and
exports the final dataset.
Code taken from Food_Recall_EDA.ipynb: Phase 4 (Data Cleaning and Preprocessing),
Phase 5 (Feature Engineering), Phase 8 (Data Quality Validation) and
Phase 9 (Export the Final Dataset).

Needs:     data_loading.py (provides the raw dataset `data`)
Provides:  raw_data, clean_data  (clean_data also contains the new columns
           classification_days, recall_year, root_cause, product_category,
           timely_classification)

Run:  python data_cleaning.py
"""

import os

import numpy as np
import pandas as pd

from data_loading import data

# Update this path if the cleaned file should be saved somewhere else
OUTPUT_PATH = r"F:\Anudip Proj\food\Food_Recalls_Cleaned.csv"

# ======================================================================
# Phase 4: Data Cleaning and Preprocessing
# ======================================================================
# --- 4.1 Create a working copy ---
# Create raw and clean dataset backups
raw_data = data.copy()
clean_data = data.copy()

print("Raw dataset shape:", raw_data.shape)
print("Clean dataset shape:", clean_data.shape)

# --- 4.2 Standardize column names ---
clean_data.columns = (
    clean_data.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print("Updated Column Names:\n")

for i, column in enumerate(clean_data.columns, start=1):
    print(f"{i} -> {column}")

# --- 4.3 Convert date columns to datetime ---
clean_data["recall_initiation_date"] = pd.to_datetime(
    clean_data["recall_initiation_date"],
    format="%Y%m%d",
    errors="coerce"
)

clean_data["center_classification_date"] = pd.to_datetime(
    clean_data["center_classification_date"],
    format="%Y%m%d",
    errors="coerce"
)

clean_data["termination_date"] = pd.to_datetime(
    clean_data["termination_date"],
    format="%Y%m%d",
    errors="coerce"
)

clean_data["report_date"] = pd.to_datetime(
    clean_data["report_date"],
    format="%Y%m%d",
    errors="coerce"
)

print(clean_data[
    ["recall_initiation_date", "center_classification_date", "termination_date", "report_date"]
].dtypes)

# --- 4.4 Remove leading and trailing spaces from text values ---
text_columns = [
    "status",
    "classification",
    "recalling_firm",
    "product_description",
    "product_quantity",
    "reason_for_recall",
    "voluntary_mandated",
    "initial_firm_notification",
    "distribution_pattern",
    "state"
]

for column in text_columns:
    clean_data[column] = (
        clean_data[column]
        .astype("string")
        .str.strip()
    )

print("Text columns cleaned successfully.")

# --- 4.5 Standardize state values ---
print("\nTop states after standardization")
# Convert state abbreviations into full state names

clean_data["state"] = (
    clean_data["state"]
    .str.upper()
    .str.strip()
)

# Dictionary mapping US state abbreviations to full names
state_mapping = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

clean_data["state"] = clean_data["state"].replace(state_mapping)

print(clean_data["state"].value_counts().head(10))

# --- 4.6 Handle missing values ---
print("\nMissing values after filling")
clean_data["state"] = clean_data["state"].fillna("Unknown")

clean_data["recalling_firm"] = clean_data["recalling_firm"].fillna("Unknown")

clean_data["product_description"] = clean_data["product_description"].fillna("Not Reported")

clean_data["reason_for_recall"] = clean_data["reason_for_recall"].fillna("Not Reported")

clean_data["product_quantity"] = clean_data["product_quantity"].fillna("Not Reported")

clean_data["voluntary_mandated"] = clean_data["voluntary_mandated"].fillna("Not Reported")

clean_data["initial_firm_notification"] = clean_data["initial_firm_notification"].fillna("Not Reported")

clean_data["distribution_pattern"] = clean_data["distribution_pattern"].fillna("Not Reported")

print(clean_data.isnull().sum())

# --- 4.7 Check duplicate records ---
duplicate_count = clean_data.duplicated().sum()

print("Number of duplicate rows:", duplicate_count)
print("Duplicate recall numbers (kept, not removed):", clean_data["recall_number"].duplicated().sum())

# remove duplicates only if they actually exist
if duplicate_count > 0:
    clean_data = clean_data.drop_duplicates()
    print("Duplicate rows removed.")
else:
    print("No duplicate rows found.")

# ======================================================================
# Phase 5: Feature Engineering
# ======================================================================
# --- 5.1 Classification days ---
print("\nClassification days (preview)")
# Days from recall initiation to FDA classification
clean_data["classification_days"] = (
    clean_data["center_classification_date"] - clean_data["recall_initiation_date"]
).dt.days

print(clean_data[["recall_initiation_date", "center_classification_date", "classification_days"]].head())

# Check missing dates and negative values
print("Missing initiation dates:", clean_data["recall_initiation_date"].isnull().sum())
print("Missing classification dates:", clean_data["center_classification_date"].isnull().sum())
print("Missing classification days:", clean_data["classification_days"].isnull().sum())

negative_days = (clean_data["classification_days"] < 0).sum()
print("Negative classification-day records:", negative_days)

# A negative duration is impossible, so it is set to missing
clean_data.loc[clean_data["classification_days"] < 0, "classification_days"] = np.nan

# --- 5.2 Recall year ---
print("\nRecalls per year")
clean_data["recall_year"] = clean_data["recall_initiation_date"].dt.year

print(clean_data["recall_year"].value_counts().sort_index())

# --- 5.3 Root cause and product category ---
print("\nRoot cause counts")
reason = clean_data["reason_for_recall"]

clean_data["root_cause"] = "Other / Unclassified"

clean_data.loc[reason.str.contains("label|mislabel|packag|coding|expiration|date code|misbrand|leak|seal", case=False, na=False), "root_cause"] = "Labeling / Packaging Error"
clean_data.loc[reason.str.contains("pasteuri|underprocess|under-process|temperature|cooling|refrigerat|acidified|sterility|inadequate process|process control|thermal", case=False, na=False), "root_cause"] = "Process / Temperature Control"
clean_data.loc[reason.str.contains("lead|pesticide|toxin|aflatoxin|melamine|chemical|heavy metal|arsenic|cadmium|mercury|sanitizer|cleaning", case=False, na=False), "root_cause"] = "Chemical Contamination"
clean_data.loc[reason.str.contains("metal|glass|plastic|foreign|fragment|wire|stone|rubber|bone|insect", case=False, na=False), "root_cause"] = "Foreign Material"
clean_data.loc[reason.str.contains("botulism|clostridium|cronobacter|staph|bacillus|norovirus|hepatitis|mold|mould|yeast|bacteria|microbial|pathogen|spoilage", case=False, na=False), "root_cause"] = "Other Microbial"
clean_data.loc[reason.str.contains("e. coli|escherichia|stec", case=False, na=False), "root_cause"] = "E. coli"
clean_data.loc[reason.str.contains("salmonella", case=False, na=False), "root_cause"] = "Salmonella"
clean_data.loc[reason.str.contains("listeria|monocytogenes", case=False, na=False), "root_cause"] = "Listeria"
clean_data.loc[reason.str.contains("undeclared|allergen|allergy|milk|wheat|soy|egg|peanut|tree nut|sesame|sulfite|shellfish|fish", case=False, na=False), "root_cause"] = "Undeclared Allergen"
clean_data.loc[reason == "Not Reported", "root_cause"] = "Reason Not Reported"

print(clean_data["root_cause"].value_counts())

print("\nProduct category counts")
description = clean_data["product_description"]

clean_data["product_category"] = "Other Food"

clean_data.loc[description.str.contains("sandwich|ready-to-eat|ready to eat|meal|soup|burrito|pizza|dinner|entree|frozen", case=False, na=False), "product_category"] = "Prepared / Ready-to-Eat"
clean_data.loc[description.str.contains("candy|chocolate|gummy|snack|chip|popcorn|nuts|peanut butter|bars", case=False, na=False), "product_category"] = "Confectionery & Snacks"
clean_data.loc[description.str.contains("juice|drink|beverage|coffee|water|soda|smoothie", case=False, na=False), "product_category"] = "Beverages"
clean_data.loc[description.str.contains("spinach|lettuce|salad|tomato|apple|berry|berries|melon|cantaloupe|sprout|produce|onion|vegetable|fruit", case=False, na=False), "product_category"] = "Fresh Produce"
clean_data.loc[description.str.contains("cookie|bread|cake|cracker|cereal|granola|muffin|bagel|pastry|bakery|flour|pasta|noodle", case=False, na=False), "product_category"] = "Bakery & Cereal"
clean_data.loc[description.str.contains("milk|cheese|yogurt|yoghurt|butter|cream|ice cream|egg|dairy", case=False, na=False), "product_category"] = "Dairy & Eggs"
clean_data.loc[description.str.contains("chicken|beef|pork|turkey|sausage|hot dog|bacon|meat|jerky|poultry", case=False, na=False), "product_category"] = "Meat & Poultry"
clean_data.loc[description.str.contains("salmon|tuna|shrimp|fish|seafood|crab|lobster|oyster|clam|cod|tilapia", case=False, na=False), "product_category"] = "Seafood"
clean_data.loc[description.str.contains("supplement|capsule|vitamin|tablet|protein powder|herbal", case=False, na=False), "product_category"] = "Dietary Supplements"
clean_data.loc[description.str.contains("infant|baby|toddler|formula", case=False, na=False), "product_category"] = "Infant & Baby Food"
clean_data.loc[description == "Not Reported", "product_category"] = "Description Not Reported"

print(clean_data["product_category"].value_counts())

# --- 5.4 Timely classification indicator ---
print("\nTimely classification counts")
# Change this number to use a different limit
timely_limit = 30

clean_data["timely_classification"] = np.where(
    clean_data["classification_days"] <= timely_limit, "Yes", "No"
)

clean_data.loc[clean_data["classification_days"].isnull(), "timely_classification"] = "Not Available"

print(clean_data["timely_classification"].value_counts())

# ======================================================================
# Phase 8: Data Quality Validation
# ======================================================================
print("=" * 70)
print("FINAL DATA QUALITY CHECK")
print("=" * 70)

print("\nRaw rows:", raw_data.shape[0])
print("Clean rows:", clean_data.shape[0])
print("Rows removed:", raw_data.shape[0] - clean_data.shape[0])
print("Columns:", clean_data.shape[1])

print("\nUnique recall numbers (raw):", raw_data["recall_number"].nunique())
print("Unique recall numbers (clean):", clean_data["recall_number"].nunique())

print("\nDuplicate Rows:")
print(clean_data.duplicated().sum())

print("\nNegative Classification Days:")
print((clean_data["classification_days"] < 0).sum())

# --- Missing values after cleaning ---
print("\nMissing values after cleaning")
print(clean_data.isnull().sum())

# --- Data types after cleaning ---
print("\nData types after cleaning")
print(clean_data.dtypes)

# --- Check the derived features ---
print("\nDerived features summary")
print(clean_data[["classification_days", "recall_year"]].describe())

# The number of removed rows should equal the number of duplicate rows found in Phase 3,
# and the number of unique recall numbers should be the same before and after cleaning.
# The columns that still have missing values (the dates, the classification and the
# classification days) were left empty on purpose.

# ======================================================================
# Phase 9: Export the Final Dataset
# ======================================================================
clean_data.to_csv(OUTPUT_PATH, index=False)

print("Cleaned dataset saved successfully.")

# check where the file is saved
print(os.path.exists(OUTPUT_PATH))
