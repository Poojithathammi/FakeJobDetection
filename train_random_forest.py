import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

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

# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# SMOTE on training data only
smote = SMOTE(random_state=42)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_tfidf,
    y_train
)

# Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train
model.fit(X_train_balanced, y_train_balanced)

print("Random Forest training completed!")
print("Training samples:", X_train_balanced.shape[0])
print("Testing samples:", X_test_tfidf.shape[0])