
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "student-mat.csv"
OUTPUT_DIR = BASE_DIR / "dataset" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "cleaned_student_data.csv"

# 1. Load the raw dataset
data = pd.read_csv(DATA_PATH, sep=";")

print("Original dataset shape:", data.shape)

# 2. Remove duplicate rows
data = data.drop_duplicates()

# 3. Select important columns
required_columns = [
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3"
]

# 4. Check required columns
missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

# 5. Remove rows with missing required values
data = data.dropna(subset=required_columns)

# 6. Keep valid grade values
for column in ["G1", "G2", "G3"]:
    data = data[data[column].between(0, 20)]

# 7. Keep valid study time and nonnegative values
data = data[
    data["studytime"].between(1, 4)
    & data["failures"].ge(0)
    & data["absences"].ge(0)
]

# 8. Create output folder if needed
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 9. Save cleaned dataset
data.to_csv(OUTPUT_PATH, index=False)

# 10. Display results
print("Cleaned dataset shape:", data.shape)
print("Remaining missing values:")
print(data[required_columns].isnull().sum())

print("\nCleaned dataset saved successfully!")
print("Output file:", OUTPUT_PATH)
