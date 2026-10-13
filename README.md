# Food Recall Root-Cause Intelligence

**What goes wrong in food recalls, which products are hit, and how fast does the FDA respond?**
An exploratory data analysis of raw FDA Food Enforcement Reports, framed for the Food Safety and Quality Assurance team of a global food manufacturer (Nestlé).

> The data is public FDA data and was not provided by Nestlé. Nestlé is used only as the business framing of the project.

---

## At a glance

| | |
|---|---|
| **Industry** | Food manufacturing and food safety |
| **Business framing** | Nestlé, Global Food Safety and Quality Assurance |
| **Data** | FDA Food Enforcement Reports (openFDA), one row per recalled product |
| **Size** | 29,471 recall records, 24 raw columns (29 after cleaning) |
| **Data state** | Raw: blanks, free text, inconsistent values, an impossible date |
| **Work done** | Quality audit, cleaning, feature creation, exploratory analysis, 11 charts, validated CSV export |
| **Tools** | Python, Pandas, NumPy, Matplotlib, Jupyter Notebook |
| **Status** | EDA complete |

---

## Why this project

When a food product may be unsafe, the company recalls it. A recall costs product, money and trust. The FDA publishes every recall, but the records are entered by hand:

- the **reason** for a recall and the **product description** are free text,
- dates are stored as text such as `20240115`, and one is impossible (year `0212`),
- many fields are blank or marked "Unknown",
- states are abbreviations, and spaces and formats are inconsistent.

Because of this, the raw table cannot answer simple business questions. This project cleans the data and answers them.

**The question:** Which root causes and product categories lead to the most recalls, and how do recall status and classification time differ across them?

---

## How the project works

The notebook follows nine phases, in this order:

```
Load  ->  Inspect  ->  Assess quality  ->  Clean  ->  Create features
      ->  Explore  ->  Compare with charts  ->  Validate  ->  Export
```

| Phase | What happens |
|---|---|
| 1. Data acquisition | Load the raw CSV and confirm it read correctly |
| 2. Initial inspection | First rows, size, column names, data types, descriptive statistics |
| 3. Quality assessment | Missing values, duplicate rows, repeated recall numbers, inconsistent categories and dates |
| 4. Cleaning | Working copy, column names, dates, spaces, state names, missing values, duplicates |
| 5. Feature engineering | New columns built from existing ones (see below) |
| 6. Exploratory analysis | Counts by product, cause, firm, state and notification channel; status and classification |
| 7. Comparative visualization | Six comparison charts |
| 8. Validation | Rows, missing values, duplicates, data types and new columns re-checked |
| 9. Export | Cleaned dataset saved as CSV |

---

## The data

| Item | Detail |
|---|---|
| Name | FDA Food Enforcement Reports (food recalls) |
| Publisher | U.S. Food and Drug Administration, through openFDA |
| Download page | <https://open.fda.gov/apis/downloads> (Food, Enforcement) |
| API endpoint | `https://api.fda.gov/food/enforcement.json` |
| Original format | JSON (zipped) |
| Format used here | CSV, converted with `pandas.json_normalize`. Only the format changed, not the values |
| Period | Recalls initiated from 2008 to 2026 (2026 is a partial year; most records are from 2012 onward) |

Main columns used: `recall_number`, `event_id`, `status`, `classification`, `recalling_firm`, `product_description`, `reason_for_recall`, `initial_firm_notification`, `state`, and the four date columns (`recall_initiation_date`, `center_classification_date`, `termination_date`, `report_date`).

Classification meaning: **Class I** means serious harm is possible, **Class II** means temporary or reversible harm, **Class III** means harm is unlikely.

---

## What was wrong with the raw data, and what was done

| Problem in the raw data | Treatment |
|---|---|
| Dates stored as text | Converted to real dates |
| One impossible initiation date (year `0212`, recall F-0880-2013) | Treated as invalid and set to missing |
| Extra leading and trailing spaces in text | Removed |
| States written as abbreviations | Mapped to full state names |
| Blank text fields | Filled with a clear label ("Unknown" or "Not Reported") |
| Blank dates and classification | Left empty on purpose, because a guessed value would give wrong results. An empty termination date means the recall is still ongoing |
| Exact duplicate rows | None found (0 removed) |
| Repeated recall numbers | None are repeated. Two records have no recall number yet (both are ongoing recalls that are not yet classified). Kept, because they are real recalls |
| Negative time differences | Set to missing, because a negative duration is impossible (none found) |

Columns that are almost empty in the raw data: `more_code_info` (100% blank), `address_2` (94.0%), `product_quantity` (6.0%) and `termination_date` (5.1%).

---

## Features created

| New column | How it is built |
|---|---|
| `classification_days` | Days from recall start to FDA classification |
| `recall_year` | Year taken from the recall start date |
| `root_cause` | Free-text reason grouped by keyword searches (for example allergen, Listeria, Salmonella, foreign material, labeling error) |
| `product_category` | Product description grouped by keyword searches (for example dairy, meat and poultry, bakery, produce, seafood) |
| `timely_classification` | "Yes" if classified within 30 days, "No" if not, "Not Available" if dates are missing |

The 30-day limit is an assumption made for this project, because the FDA data has no such column. It is one variable in the notebook and can be changed.

---

## Analysis and charts

**Five exploratory charts** show recalls by product category, root cause, recalling firm, state and notification channel.

**Six comparison charts** show how related variables differ:

| # | Chart | What it shows |
|---|---|---|
| 1 | Product category vs timely classification | Which products are classified within 30 days more often |
| 2 | Product category vs recall status | How recalls of each product category stand (ongoing, completed, terminated) |
| 3 | Root cause vs recall status | Whether some causes stay ongoing longer |
| 4 | Product category vs classification time | Average days to FDA classification by product |
| 5 | Recall year vs recall volume | How recall counts change over the years |
| 6 | Notification channel vs timely classification | Whether the way customers were notified relates to classification speed |

### Chart gallery

<!-- The image links below must match the file names inside the Visualization folder (GitHub is case-sensitive). Edit the names if yours differ. -->

### 1. Category Analysis

<img width="1184" height="674" alt="Category Analysis.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Category%20Analysis.png" />

### 2. Firm Analysis

<img width="1184" height="674" alt="Firm Analysis.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Firm%20Analysis.png" />

### 3. Notification Channel Analysis

<img width="1184" height="674" alt="Notification Channel Analysis.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Notification%20Channel%20Analysis.png" />

### 4. Notification Channel vs Timely Classification

<img width="1184" height="674" alt="Notification Channel vs Timely Classification.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Notification%20Channel%20vs%20Timely%20Classification.png" />

### 5. Product Category vs Classification Duration

<img width="1184" height="674" alt="Product Category vs Classification Duration.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Product%20Category%20vs%20Classification%20Duration.png" />

### 6. Product Category vs Recall Status

<img width="1184" height="674" alt="Product Category vs Recall Status.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Product%20Category%20vs%20Recall%20Status.png" />

### 7. Product Category vs Timely Classification

<img width="1184" height="674" alt="Product Category vs Timely Classification.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Product%20Category%20vs%20Timely%20Classification.png" />

### 8. Recall Year vs Recall Volume

<img width="1184" height="674" alt="Recall Year vs Recall Volume.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Recall%20Year%20vs%20Recall%20Volume.png" />

### 9. Root Cause Analysis

<img width="1184" height="674" alt="Root Cause Analysis.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Root%20Cause%20Analysis.png" />

### 10. Root Cause vs Recall Status

<img width="1184" height="674" alt="Root Cause vs Recall Status.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/Root%20Cause%20vs%20Recall%20Status.png" />

### 11. State Analysis.png

<img width="1184" height="674" alt="State Analysis.png" src="https://github.com/avacio-create/food-recall-root-cause-intelligence/blob/main/Visualization/State%20Analysis.png" />

---

## Key findings

| Measure | Result |
|---|---|
| Rows and columns after cleaning | 29,471 rows, 29 columns (24 original plus 5 new) |
| Duplicate rows Present | 0 |
| Most common root cause | Undeclared Allergen, 9,531 recalls (32.3%) |
| Second most common root cause | Listeria, 7,397 recalls (25.1%) |
| Product category with the most recalls | Dairy & Eggs, 6,005 recalls (20.4%), among the named categories. "Other Food" (7,155) is a catch-all for descriptions the keywords did not match |
| Firm with the most recalls | Garden-Fresh Foods, Inc., 633 recalls |
| State with the most recalls | California, 4,045 recalls (13.7%) |
| Recalls by class | Class II 50.0%, Class I 44.0%, Class III 6.0% |
| Recall status | Terminated 94.9%, Ongoing 3.6%, Completed 1.5% |
| Classified within 30 days | 33.7% (median 38 days from recall start to classification) |
| Longest average classification time | Dietary Supplements, 119.1 days on average (median 54 days) |
| Year with the most recalls (full years only) | 2016, with 3,066 recalls |

Other points from the comparison charts:

- Only 21.9% of Dietary Supplements recalls and 28.9% of Infant & Baby Food recalls were classified within 30 days, the lowest shares. Prepared / Ready-to-Eat was highest at 40.3%.
- Salmonella has the highest share of ongoing recalls (6.3%), and Process / Temperature Control has the highest share of completed-but-not-terminated recalls (14.3%).
- Recall volume rose from 2012 to a peak in 2016, dropped to 1,117 in 2020, and has moved between about 1,400 and 2,200 since.

---

## Recommendations

1. **Strengthen allergen and Listeria controls.** Undeclared allergens and Listeria together account for 57.4% of recalls. Label-to-formula checks, allergen changeover cleaning and environmental monitoring of ready-to-eat lines are the most direct controls for these causes.
2. **Focus supplier checks on the largest product categories.** Dairy & Eggs (20.4%), Seafood (14.1%) and Fresh Produce (12.2%) are the three largest named categories, so supplier audits and incoming-material checks should start there.
3. **Do not wait for FDA classification.** Only 33.7% of recalls are classified within 30 days, and 44.0% end up Class I. A company should run its own risk assessment from the day a recall starts, especially for Dietary Supplements and Infant & Baby Food, which are classified most slowly.
4. **Improve how recall data is recorded.** 6.0% of product quantities are blank, firm names appear in several spellings, and one date was entered as year 0212. Standard formats for quantity, firm name and date would make recall data much easier to analyse.

---

## Limitations

- Root causes and product categories come from keyword searches on free text, so they are approximations.
- The keyword rules are applied in order and the allergen rule runs last. A recall that mentions both a pathogen and an allergen-type word (for example eggs contaminated with Listeria) is therefore labelled Undeclared Allergen. About 700 recalls whose reason mentions Listeria, Salmonella or E. coli carry the allergen label, so the allergen count is probably overstated.
- "Other Food" and "Other / Unclassified" are catch-all groups, so the largest category and cause groups are partly unclassified.
- The 30-day timely classification limit is an assumption, not an FDA rule.
- Classification time covers only the time until the FDA classifies a recall, not the full life of the recall.
- Each row is one product, and one recall event can cover many products, so counts by firm and cause reflect product records, not separate events.
- The data covers only recalls reported to the FDA.
- The charts show patterns, not proof of cause.

---

## Repository layout

```text
food-recall-root-cause-intelligence/
|
|-- README.md
|
|-- Dataset/
|   |-- food_enforcement_raw.csv        raw data from openFDA (CSV)
|   |-- food-enforcement-0001-of-0001.json
|   `-- Food_Recalls_Cleaned.csv        cleaned dataset
|
|-- Documentation/                      project documents
|
|-- Notebook/
|   `-- Food_Recall_EDA.ipynb           full analysis, phases 1 to 9
|
|-- Python/                             
|   |-- data_loading.py                 load, inspect, quality assessment
|   |-- data_cleaning.py                cleaning, features, validation, export
|   |-- exploratory_analysis.py         summary tables
|   `-- data_visualization.py           all 11 charts
|
|-- Visualization/                      saved chart images
|   |-- Category Analysis.png
|   |-- Firm Analysis.png
|   |-- Notification Channel Analysis.png
|   |-- Notification Channel vs Timely Classification.png
|   |-- Product Category vs Classification Duration.png
|   |-- Product Category vs Recall Status.png
|   |-- Product Category vs Timely Classification.png
|   |-- Recall Year vs Recall Volume.png
|   |-- Root Cause Analysis.png
|   |-- Root Cause vs Recall Status.png
|   `-- State Analysis.png
`
```

---

## How to run it

1. The raw data is in the `Dataset` folder. To download it yourself, use the openFDA download page above and convert the JSON files to one CSV file (`food_enforcement_raw.csv`).
2. Install the libraries: `pip install pandas numpy matplotlib jupyter`
3. **Notebook:** open `Notebook/Food_Recall_EDA.ipynb` in Jupyter Notebook, change the folder path in the three places where it appears (loading the raw file, saving the cleaned file, and the check that the file exists), and run all cells from top to bottom.
4. **Python scripts:** change `DATA_PATH` in `data_loading.py` and `OUTPUT_PATH` in `data_cleaning.py` to your folders. Then, from inside the `Python` folder, run `python data_visualization.py` to run everything in order, or run a single script on its own. Each script imports the one before it.

---

## Future scope

- Improve the grouping of reasons and products, and apply the pathogen rules before the allergen rule
- Standardize firm names, which appear in several spellings
- Analyze recall size from the quantity text
- Add statistical tests and a dashboard once covered in class

---

## Author

| | |
|---|---|
| **Name** | A Varun Sanketh |
| **Student ID** | AF05309750 |
| **Organization** | Anudip Foundation |
| **Course** | AIML |
| **Batch Code** | ANP-D7444 |
