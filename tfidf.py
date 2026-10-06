import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
df = pd.read_csv("dataset/fake_job_postings.csv")

# Convert target
df["fraudulent"] = df["fraudulent"].map({
    "f": 0,
    "t": 1
})

# Fill missing text values
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

for column in text_columns:
    df[column] = df[column].fillna("")

# Combine job text
df["combined_text"] = (
    df["title"] + " " +
    df["company_profile"] + " " +
    df["description"] + " " +
    df["requirements"] + " " +
    df["benefits"]
)

# Input and target
X = df["combined_text"]
y = df["fraudulent"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

# Learn vocabulary from training data
X_train_tfidf = vectorizer.fit_transform(X_train)

# Transform testing data using the same vocabulary
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF conversion completed!")

print("\nTraining data shape:", X_train_tfidf.shape)
print("Testing data shape:", X_test_tfidf.shape)

print("\nNumber of features:", len(vectorizer.get_feature_names_out()))

print("\nFirst 20 features:")
print(vectorizer.get_feature_names_out()[:20])