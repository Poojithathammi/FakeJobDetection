import pandas as pd

# Load dataset
file_path = "dataset/fake_job_postings.csv"
df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# Convert target column
df["fraudulent"] = df["fraudulent"].map({
    "f": 0,
    "t": 1
})

# Text columns
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

# Fill missing text values
for column in text_columns:
    df[column] = df[column].fillna("")

# Categorical columns
categorical_columns = [
    "location",
    "department",
    "salary_range",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

# Fill missing categorical values
for column in categorical_columns:
    df[column] = df[column].fillna("Unknown")

# Create combined text
df["combined_text"] = (
    df["title"] + " " +
    df["company_profile"] + " " +
    df["description"] + " " +
    df["requirements"] + " " +
    df["benefits"]
)

print("\nCleaning completed!")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nTarget distribution:")
print(df["fraudulent"].value_counts())

print("\nFirst 5 combined texts:")
print(df["combined_text"].head())