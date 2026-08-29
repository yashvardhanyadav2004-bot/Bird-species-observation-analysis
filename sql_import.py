import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# ============================================================
# 1. MYSQL CONNECTION DETAILS
# ============================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"

# Apna MySQL root password yahan enter karo
MYSQL_PASSWORD = "Yash1693051043"

DATABASE_NAME = "bird_species_analysis"

# ============================================================
# 2. CSV FILE PATH
# ============================================================

CSV_PATH = r"data\bird_observation_cleaned.csv"

# ============================================================
# 3. READ CSV
# ============================================================

print("Reading CSV file...")

df = pd.read_csv(CSV_PATH)

print(f"CSV loaded successfully!")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# ============================================================
# 4. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("/", "_")
)

print("\nColumns:")
print(df.columns.tolist())

# ============================================================
# 5. MYSQL DATABASE CONNECTION
# ============================================================

encoded_password = quote_plus(MYSQL_PASSWORD)

server_engine = create_engine(
    f"mysql+mysqlconnector://{MYSQL_USER}:{encoded_password}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}"
)

# ============================================================
# 6. CREATE DATABASE
# ============================================================

print("\nCreating database if it does not exist...")

with server_engine.connect() as connection:
    connection.execute(
        text(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`")
    )
    connection.commit()

print(f"Database ready: {DATABASE_NAME}")

# ============================================================
# 7. CONNECT TO PROJECT DATABASE
# ============================================================

db_engine = create_engine(
    f"mysql+mysqlconnector://{MYSQL_USER}:{encoded_password}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}"
)

# ============================================================
# 8. REMOVE OLD TABLE
# ============================================================

print("\nRemoving old table if it exists...")

with db_engine.connect() as connection:
    connection.execute(
        text("DROP TABLE IF EXISTS bird_observations")
    )
    connection.commit()

print("Old table removed.")

# ============================================================
# 9. IMPORT DATA INTO MYSQL
# ============================================================

print("\nImporting data into MySQL...")
print("Please wait...")

df.to_sql(
    name="bird_observations",
    con=db_engine,
    if_exists="replace",
    index=False,
    chunksize=500,
    method="multi"
)

print("\n========================================")
print("DATA IMPORT COMPLETED SUCCESSFULLY!")
print("========================================")

# ============================================================
# 10. VERIFY DATA
# ============================================================

with db_engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM bird_observations")
    )

    total_rows = result.scalar()

    result = connection.execute(
        text("SELECT COUNT(*) FROM bird_observations")
    )

print(f"\nTotal records imported: {total_rows}")

# ============================================================
# 11. SHOW SAMPLE DATA
# ============================================================

sample = pd.read_sql(
    "SELECT * FROM bird_observations LIMIT 5",
    db_engine
)

print("\nFirst 5 records:")
print(sample)

print("\nSQL import process finished.")