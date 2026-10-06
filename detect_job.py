from scraper import scrape_webpage
from url_analyzer import analyze_url
from predictor import predict_job
from risk_analyzer import generate_reasons
from risk_score import calculate_risk_score


def detect_job(url):

    print("\n================================")
    print("       JOB FRAUD DETECTION")
    print("================================")

    print("\nURL:")
    print(url)

    # ==========================================
    # STEP 1: ANALYZE URL
    # ==========================================

    url_result = analyze_url(url)

    reasons = generate_reasons(url_result)

    print("\n================================")
    print("URL ANALYSIS")
    print("================================")

    print("HTTPS:", url_result["https"])
    print("URL Length:", url_result["url_length"])
    print("Domain Length:", url_result["domain_length"])
    print("Dot Count:", url_result["dot_count"])
    print("Hyphen Count:", url_result["hyphen_count"])
    print("Subdomain Count:", url_result["subdomain_count"])
    print("Suspicious Words:", url_result["suspicious_words"])
    print(
        "Special Character Count:",
        url_result["special_character_count"]
    )

    # ==========================================
    # STEP 2: SCRAPE WEBPAGE
    # ==========================================

    print("\n================================")
    print("WEBPAGE ANALYSIS")
    print("================================")

    print("Scraping webpage...")

    try:

        page = scrape_webpage(url)

        print("Page Title:", page["page_title"])

    except Exception as e:

        print("Unable to scrape webpage.")
        print("Error:", e)

        return

    # ==========================================
    # STEP 3: PREPARE JOB TEXT
    # ==========================================

    job_text = (
        page["page_title"]
        + " "
        + " ".join(page["headings"])
        + " "
        + page["text"]
    )

    # ==========================================
    # STEP 4: MACHINE LEARNING PREDICTION
    # ==========================================

    print("\n================================")
    print("       ML PREDICTION")
    print("================================")

    prediction = predict_job(job_text)

    print("RESULT:", prediction["result"])

    print(
        "FAKE PROBABILITY:",
        round(
            prediction["fake_probability"] * 100,
            2
        ),
        "%"
    )

    print(
        "REAL PROBABILITY:",
        round(
            prediction["real_probability"] * 100,
            2
        ),
        "%"
    )

    # ==========================================
    # STEP 5: RISK INDICATORS
    # ==========================================

    print("\n================================")
    print("       RISK INDICATORS")
    print("================================")

    if reasons:

        for reason in reasons:
            print("⚠️", reason)

    else:

        print(
            "No major suspicious URL indicators detected."
        )

    # ==========================================
    # STEP 6: CALCULATE RISK SCORE
    # ==========================================

    risk_score, risk_level = calculate_risk_score(
        prediction,
        url_result
    )

    # ==========================================
    # STEP 7: FINAL RESULT
    # ==========================================

    print("\n================================")
    print("       FINAL RESULT")
    print("================================")

    print(
        "Prediction:",
        prediction["result"]
    )

    print(
        "Fake Probability:",
        round(
            prediction["fake_probability"] * 100,
            2
        ),
        "%"
    )

    print(
        "Real Probability:",
        round(
            prediction["real_probability"] * 100,
            2
        ),
        "%"
    )

    print(
        "Risk Score:",
        risk_score,
        "/ 100"
    )

    print(
        "Risk Level:",
        risk_level
    )

    print("\nReasons:")

    if reasons:

        for reason in reasons:
            print("-", reason)

    else:

        print(
            "- No major suspicious URL indicators detected."
        )

    # ==========================================
    # FINAL WARNING
    # ==========================================

    if risk_level == "HIGH":

        print("\n🔴 WARNING: HIGH RISK JOB")

    elif risk_level == "MEDIUM":

        print("\n🟡 CAUTION: MEDIUM RISK JOB")

    else:

        print("\n🟢 LOW RISK JOB")

    print("================================")


# ==========================================
# TEST THE COMPLETE SYSTEM
# ==========================================

test_url = "file:///C:/FakeJobDetection/test_job.html"

detect_job(test_url)