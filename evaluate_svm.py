import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, fbeta_score, confusion_matrix

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

# Combine text
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

# SMOTE
smote = SMOTE(random_state=42)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_tfidf,
    y_train
)

# SVM
model = LinearSVC(
    random_state=42,
    max_iter=5000
)

model.fit(X_train_balanced, y_train_balanced)

# Predictions
y_pred = model.predict(X_test_tfidf)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f3 = fbeta_score(y_test, y_pred, beta=3)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\n========== SVM RESULTS ==========")

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F3 Score :", round(f3, 4))

print("\nConfusion Matrix:")
print(cm)