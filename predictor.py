import joblib


# Load saved model
model = joblib.load("models/fake_job_model.pkl")

# Load saved TF-IDF vectorizer
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def predict_job(text):

    # Convert text into TF-IDF features
    text_tfidf = vectorizer.transform([text])

    # Make prediction
    prediction = model.predict(text_tfidf)[0]

    # Get probability
    probability = model.predict_proba(text_tfidf)[0]

    fake_probability = probability[1]
    real_probability = probability[0]

    if prediction == 1:
        result = "FAKE"
    else:
        result = "REAL"

    return {
        "result": result,
        "fake_probability": fake_probability,
        "real_probability": real_probability
    }


# ==========================================
# TEST
# ==========================================

test_job = """
Software Developer
ABC Technologies

We are looking for a software developer to join our team.
The candidate will work on Java and Python applications.

Requirements:
Java, Python, SQL, Data Structures and Algorithms.

Benefits:
Health insurance, paid leave and training.
"""


result = predict_job(test_job)


print("================================")
print("PREDICTION:", result["result"])
print("FAKE PROBABILITY:", result["fake_probability"])
print("REAL PROBABILITY:", result["real_probability"])