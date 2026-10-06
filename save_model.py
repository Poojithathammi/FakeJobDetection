import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("dataset/fake_job_postings.csv")

# Convert target
df["fraudulent"] = df["fraudulent"].map({
    "f": 0,
    "t": 1
})

# Fill missing values
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

# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)

# SMOTE
smote = SMOTE(random_state=42)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_tfidf,
    y_train
)

# Logistic Regression
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

# Train model
model.fit(X_train_balanced, y_train_balanced)

# Save model
joblib.dump(model, "models/fake_job_model.pkl")

# Save TF-IDF vectorizer
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model saved successfully!")
print("Saved: models/fake_job_model.pkl")
print("Saved: models/tfidf_vectorizer.pkl")