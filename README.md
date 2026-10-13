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
| **Data state** | Raw: blanks, invalid dates, free text, inconsistent values |
| **Work done** | Quality audit, cleaning, feature creation, exploratory analysis, 11 charts, validated CSV export |
| **Tools** | Python, Pandas, NumPy, Matplotlib, Jupyter Notebook |
| **Status** | EDA complete |

---

## Why this project

When a food product may be unsafe, the company recalls it. A recall costs product, money and trust. The FDA publishes every recall, but the records are entered by hand:

- the **reason** for a recall and the **product description** are free text,
- dates are stored as text such as `20240115`, and some are invalid (for example `00000000`),
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

Main columns used: `recall_number`, `event_id`, `status`, `classification`, `recalling_firm`, `product_description`, `reason_for_recall`, `initial_firm_notification`, `state`, and the four date columns (`recall_initiation_date`, `center_classification_date`, `termination_date`, `report_date`).

Classification meaning: **Class I** means serious harm is possible, **Class II** means temporary or reversible harm, **Class III** means harm is unlikely.

---

## What was wrong with the raw data, and what was done

| Problem in the raw data | Treatment |
|---|---|
| Dates stored as text, some invalid (`00000000`) | Converted to real dates. Invalid values became missing |
| Extra leading and trailing spaces in text | Removed |
| States written as abbreviations | Mapped to full state names |
| Blank text fields | Filled with a clear label ("Unknown" or "Not Reported") |
| Blank dates and classification | Left empty on purpose, because a guessed value would give wrong results. An empty termination date means the recall is still ongoing |
| Exact duplicate rows | Removed |
| Repeated recall numbers | Kept, because one recall number can cover several products |
| Negative time differences | Set to missing, because a negative duration is impossible |

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

**Exploratory analysis** covers recalls by product category, root cause, firm, state and notification channel, plus recall status, classification and timely classification.

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

Add your saved chart images to the `visuals/` folder, using these file names (or edit the links).

| | |
|---|---|
| ![Product vs timely](visuals/product_vs_timely.png) | ![Product vs status](visuals/product_vs_status.png) |
| ![Cause vs status](visuals/cause_vs_status.png) | ![Product vs days](visuals/product_vs_days.png) |
| ![Year vs volume](visuals/year_vs_volume.png) | ![Channel vs timely](visuals/channel_vs_timely.png) |

---

## Key findings

*Fill this in from your notebook output, using only real numbers.*

- Rows and columns after cleaning: `___` rows, `___` columns
- Duplicate rows removed: `___`
- Columns with the most missing values: `___`
- Most common root cause: `___` (`___` recalls)
- Product category with the most recalls: `___`
- Firm with the most recalls: `___`
- State with the most recalls: `___`
- Share of recalls that are Class I: `___`
- Product category with the longest average classification time: `___` (`___` days)
- Year with the most recalls (full years only): `___`

---

## Recommendations

*Write 3 to 5 short points, each linked to one finding above.*

1. Because `[root cause]` is the most common cause of recalls, the quality team should `[action]`.
2. Because `[product category]` has the most recalls, supplier checks should focus on `[action]`.
3. Because `[product category or cause]` takes the longest to be classified, `[action]`.
4. Because `[x]%` of text fields were blank in the raw data, `[data reporting action]`.

---

## Limitations

- Root causes and product categories come from keyword searches on free text, so they are approximations.
- The 30-day timely classification limit is an assumption, not an FDA rule.
- Classification time covers only the time until the FDA classifies a recall, not the full life of the recall.
- The data covers only recalls reported to the FDA.
- The charts show patterns, not proof of cause.

---

## Repository layout

```text
food-recall-root-cause-intelligence/
|
|-- README.md
|
|-- data/
|   |-- food_enforcement_raw.csv        raw data (do not upload if over 100 MB; keep the download link instead)
|   `-- Food_Recalls_Cleaned.csv        cleaned dataset
|
|-- notebook/
|   `-- Food_Recall_EDA.ipynb
|
`-- visuals/
    |-- product_vs_timely.png
    |-- product_vs_status.png
    |-- cause_vs_status.png
    |-- product_vs_days.png
    |-- year_vs_volume.png
    `-- channel_vs_timely.png
```

---

## How to run it

1. Download the Food Enforcement data from the openFDA download page and convert the JSON files to one CSV file (`food_enforcement_raw.csv`).
2. Install the libraries: `pip install pandas numpy matplotlib jupyter`
3. Open `Food_Recall_EDA.ipynb` in Jupyter Notebook.
4. Change the folder path in the three places where it appears: loading the raw file, saving the cleaned file, and the check that the file exists.
5. Run all cells from top to bottom.

---

## Future scope

- Improve the grouping of reasons and products
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
