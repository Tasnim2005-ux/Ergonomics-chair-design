import pandas as pd
import numpy as np


# ==============================
# 1. LOAD DATA
# ==============================

male_file = "data/male.xlsx"
female_file = "data/female.xlsx"

male_df = pd.read_excel(male_file)
female_df = pd.read_excel(female_file)


# ==============================
# 2. CLEAN COLUMN NAMES
# ==============================

def clean_columns(df):

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace("(CM)", "CM", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


male_df = clean_columns(male_df)
female_df = clean_columns(female_df)


# ==============================
# 3. REQUIRED MEASUREMENTS
# ==============================

measurement_columns = [

    "POPLITEAL_HEIGHTCM",

    "BUTTOCK_POPLITEAL_HIGHTCM",

    "HIP_BREADTHCM",

    "SITTING_SHOULDER_HEIGHTCM",

    "SITTING_KNEE_HEIGHTCM",

    "TIGH_CLEARENCECM",

    "BUTTOCK_KNEE_LENGTHCM",

    "FOOT_LENGTHCM",

    "SITTING_ELBOW_HEIGHTCM"
]


# ==============================
# 4. CONVERT MEASUREMENTS
#    TO NUMERIC
# ==============================

for column in measurement_columns:

    male_df[column] = pd.to_numeric(
        male_df[column],
        errors="coerce"
    )

    female_df[column] = pd.to_numeric(
        female_df[column],
        errors="coerce"
    )


# ==============================
# 5. REMOVE INVALID ROWS
# ==============================

male_df = male_df.dropna(
    subset=measurement_columns
).copy()

female_df = female_df.dropna(
    subset=measurement_columns
).copy()


# ==============================
# 6. STATISTICAL ANALYSIS
# ==============================

def calculate_statistics(df):

    results = []

    for column in measurement_columns:

        data = df[column].dropna()

        results.append({

            "Measurement": column,

            "Minimum":
                data.min(),

            "Maximum":
                data.max(),

            "Mean":
                data.mean(),

            "Median":
                data.median(),

            "Standard Deviation":
                data.std(),

            "Variance":
                data.var(),

            "P5":
                np.percentile(data, 5),

            "P25":
                np.percentile(data, 25),

            "P50":
                np.percentile(data, 50),

            "P75":
                np.percentile(data, 75),

            "P95":
                np.percentile(data, 95)
        })

    return pd.DataFrame(results)


male_statistics = calculate_statistics(
    male_df
)

female_statistics = calculate_statistics(
    female_df
)


# ==============================
# 7. DISPLAY RESULTS
# ==============================

print("\n================================")
print("MALE DATASET")
print("================================")

print(
    "Valid observations:",
    len(male_df)
)

print(
    male_statistics.round(2).to_string(
        index=False
    )
)


print("\n================================")
print("FEMALE DATASET")
print("================================")

print(
    "Valid observations:",
    len(female_df)
)

print(
    female_statistics.round(2).to_string(
        index=False
    )
)