import pandas as pd
from pathlib import Path

# ==========================================
# BIRD SPECIES OBSERVATION ANALYSIS
# STEP 1: LOAD EXCEL FILES
# ==========================================

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Excel file paths
forest_file = DATA_DIR / "Bird_Monitoring_Data_FOREST.XLSX"
grassland_file = DATA_DIR / "Bird_Monitoring_Data_GRASSLAND.XLSX"

# Check files exist
print("Checking input files...")

print("Forest file:", forest_file.exists())
print("Grassland file:", grassland_file.exists())

# Read all sheets from Forest
forest_sheets = pd.read_excel(
    forest_file,
    sheet_name=None
)

# Read all sheets from Grassland
grassland_sheets = pd.read_excel(
    grassland_file,
    sheet_name=None
)

# Display sheet names
print("\nFOREST SHEETS:")
print(list(forest_sheets.keys()))

print("\nGRASSLAND SHEETS:")
print(list(grassland_sheets.keys()))

print("\nExcel files loaded successfully!")
# ==========================================
# STEP 2: CHECK DATA STRUCTURE
# ==========================================

print("\n========== FOREST DATA ==========")

# First sheet ka naam
first_forest_sheet = list(forest_sheets.keys())[0]

print("Sheet:", first_forest_sheet)
print("Shape:", forest_sheets[first_forest_sheet].shape)

print("\nColumns:")
print(forest_sheets[first_forest_sheet].columns.tolist())

print("\nFirst 5 rows:")
print(forest_sheets[first_forest_sheet].head())


print("\n========== GRASSLAND DATA ==========")

# First sheet ka naam
first_grassland_sheet = list(grassland_sheets.keys())[0]

print("Sheet:", first_grassland_sheet)
print("Shape:", grassland_sheets[first_grassland_sheet].shape)

print("\nColumns:")
print(grassland_sheets[first_grassland_sheet].columns.tolist())

print("\nFirst 5 rows:")
print(grassland_sheets[first_grassland_sheet].head())
# ==========================================
# STEP 3: COMBINE FOREST AND GRASSLAND DATA
# ==========================================

# Add habitat information
forest_df = forest_sheets[first_forest_sheet].copy()
grassland_df = grassland_sheets[first_grassland_sheet].copy()

forest_df["Habitat"] = "Forest"
grassland_df["Habitat"] = "Grassland"

# Combine both datasets
combined_df = pd.concat(
    [forest_df, grassland_df],
    ignore_index=True
)

print("\n========== COMBINED DATA ==========")

print("Shape:", combined_df.shape)

print("\nColumns:")
print(combined_df.columns.tolist())

print("\nHabitat counts:")
print(combined_df["Habitat"].value_counts())

print("\nFirst 5 rows:")
print(combined_df.head())
# ==========================================
# STEP 4: DATA QUALITY CHECK
# ==========================================

print("\n========== DATA QUALITY CHECK ==========")

# Missing values
print("\nMissing values:")
print(combined_df.isnull().sum())

# Total missing values
print("\nTotal missing values:", combined_df.isnull().sum().sum())

# Duplicate rows
print("\nDuplicate rows:", combined_df.duplicated().sum())

# Dataset information
print("\nDataset information:")
print(combined_df.info())

# Statistical summary
print("\nStatistical summary:")
print(combined_df.describe(include="all"))
# ==========================================
# STEP 5: DATA CLEANING
# ==========================================

print("\n========== DATA CLEANING ==========")

# Create a copy of combined data
cleaned_df = combined_df.copy()

# ------------------------------------------
# 5.1 Remove duplicate rows
# ------------------------------------------

print("\nDuplicate rows before cleaning:")
print(cleaned_df.duplicated().sum())

cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)

print("Duplicate rows after cleaning:")
print(cleaned_df.duplicated().sum())


# ------------------------------------------
# 5.2 Identify completely empty columns
# ------------------------------------------

empty_columns = cleaned_df.columns[
    cleaned_df.isnull().all()
].tolist()

print("\nCompletely empty columns:")
print(empty_columns)


# ------------------------------------------
# 5.3 Remove completely empty columns
# ------------------------------------------

if empty_columns:
    cleaned_df = cleaned_df.drop(columns=empty_columns)

print("\nColumns after removing empty columns:")
print(cleaned_df.columns.tolist())


# ------------------------------------------
# 5.4 Check remaining missing values
# ------------------------------------------

print("\nMissing values after cleaning:")
print(
    cleaned_df.isnull()
    .sum()
    .sort_values(ascending=False)
)


# ------------------------------------------
# 5.5 Final dataset size
# ------------------------------------------

print("\n========== CLEANED DATASET ==========")

print("Rows:", cleaned_df.shape[0])
print("Columns:", cleaned_df.shape[1])

print("\nTotal missing values:")
print(cleaned_df.isnull().sum().sum())

print("\nDuplicate rows:")
print(cleaned_df.duplicated().sum())


# ------------------------------------------
# 5.6 Display first 5 rows
# ------------------------------------------

print("\nFirst 5 rows of cleaned data:")
print(cleaned_df.head())


print("\nData cleaning completed successfully!")
# ==========================================
# STEP 5.7: SAVE ORIGINAL COMBINED BACKUP
# ==========================================

backup_file = DATA_DIR / "combined_original.csv"

combined_df.to_csv(
    backup_file,
    index=False
)

print("\nOriginal combined dataset backup saved:")
print(backup_file)
# ==========================================
# STEP 6: DATE & TIME PROCESSING
# ==========================================

print("\n========== DATE & TIME PROCESSING ==========")

# ------------------------------------------
# 6.1 Convert Date column to datetime
# ------------------------------------------

cleaned_df["Date"] = pd.to_datetime(
    cleaned_df["Date"],
    errors="coerce"
)

print("\nDate column data type:")
print(cleaned_df["Date"].dtype)


# ------------------------------------------
# 6.2 Create Observation Year
# ------------------------------------------

cleaned_df["Observation_Year"] = (
    cleaned_df["Date"].dt.year
)


# ------------------------------------------
# 6.3 Create Observation Month
# ------------------------------------------

cleaned_df["Observation_Month"] = (
    cleaned_df["Date"].dt.month
)


# ------------------------------------------
# 6.4 Create Month Name
# ------------------------------------------

cleaned_df["Month_Name"] = (
    cleaned_df["Date"].dt.month_name()
)


# ------------------------------------------
# 6.5 Create Day
# ------------------------------------------

cleaned_df["Day"] = (
    cleaned_df["Date"].dt.day
)


# ------------------------------------------
# 6.6 Create Day Name
# ------------------------------------------

cleaned_df["Day_Name"] = (
    cleaned_df["Date"].dt.day_name()
)


# ------------------------------------------
# 6.7 Create Season
# ------------------------------------------

def get_season(month):

    if month in [12, 1, 2]:
        return "Winter"

    elif month in [3, 4, 5]:
        return "Spring"

    elif month in [6, 7, 8]:
        return "Summer"

    else:
        return "Autumn"


cleaned_df["Season"] = (
    cleaned_df["Observation_Month"]
    .apply(get_season)
)


# ------------------------------------------
# 6.8 Display date range
# ------------------------------------------

print("\nObservation date range:")

print("Start Date:",
      cleaned_df["Date"].min())

print("End Date:",
      cleaned_df["Date"].max())


# ------------------------------------------
# 6.9 Display year distribution
# ------------------------------------------

print("\nObservation Year distribution:")

print(
    cleaned_df["Observation_Year"]
    .value_counts()
    .sort_index()
)


# ------------------------------------------
# 6.10 Display month distribution
# ------------------------------------------

print("\nMonth distribution:")

print(
    cleaned_df["Month_Name"]
    .value_counts()
)


# ------------------------------------------
# 6.11 Display season distribution
# ------------------------------------------

print("\nSeason distribution:")

print(
    cleaned_df["Season"]
    .value_counts()
)


# ------------------------------------------
# 6.12 Check newly created columns
# ------------------------------------------

print("\nNew date/time columns:")

print([
    "Observation_Year",
    "Observation_Month",
    "Month_Name",
    "Day",
    "Day_Name",
    "Season"
])
print("\nDate & time processing completed successfully!")
# ==========================================
# STEP 6: SAVE FINAL CLEANED DATASET
# ==========================================

# Output file path
output_file = DATA_DIR / "bird_observation_cleaned.csv"

# Save cleaned dataset
combined_df.to_csv(
    output_file,
    index=False
)

print("\n========== FINAL DATASET SAVED ==========")
print("File:", output_file)
print("Rows:", combined_df.shape[0])
print("Columns:", combined_df.shape[1])

print("\nFinal dataset saved successfully!")
# ==========================================
# STEP 7: VERIFY FINAL CLEANED DATASET
# ==========================================

print("\n========== STEP 5: FINAL DATASET VERIFICATION ==========")

# Reload the saved cleaned dataset
final_df = pd.read_csv(output_file)

print("\nFinal dataset shape:")
print(final_df.shape)

print("\nFinal dataset columns:")
print(final_df.columns.tolist())

print("\nFirst 5 rows:")
print(final_df.head())

print("\nMissing values:")
print(final_df.isnull().sum())

print("\nDuplicate rows:")
print(final_df.duplicated().sum())

print("\nHabitat distribution:")
print(final_df["Habitat"].value_counts())

print("\nFinal dataset verification completed successfully!")