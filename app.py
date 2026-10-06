from flask import Flask, request, jsonify
from flask_cors import CORS

from scraper import (
    scrape_webpage,
    ScrapeError,
    extract_job_details
)

from url_analyzer import analyze_url
from predictor import predict_job
from risk_analyzer import generate_reasons
from risk_score import calculate_risk_score


app = Flask(__name__)

CORS(app)


# =========================================================
# MODEL PERFORMANCE
# =========================================================

MODEL_METRICS = {

    "accuracy": 97.65,

    "precision": 70.51,

    "recall": 88.44,

    "f3": 86.25

}


# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "success": True,

        "message":
            "Fake Job Detection API is running",

        "status":
            "online"

    })


# =========================================================
# DEMO REAL JOB
# =========================================================

@app.route(
    "/demo/real-job",
    methods=["GET"]
)
def demo_real_job():

    text = """

    Software Engineer

    Company:
    Demo Technology Company

    Location:
    Hyderabad

    Employment Type:
    Full Time

    Experience:
    0 to 2 years

    Education:
    B.Tech

    Industry:
    Information Technology

    Salary:
    ₹5-8 LPA

    We are looking for a talented Software Engineer
    to join our technology team.

    Responsibilities:

    Develop and maintain software applications.

    Write clean and efficient code.

    Work with development teams.

    Participate in software testing.

    Troubleshoot application issues.

    Requirements:

    Bachelor's degree in Computer Science
    or related field.

    Knowledge of Java, Python or JavaScript.

    Good problem-solving skills.

    Good communication skills.

    Benefits:

    Competitive salary.

    Health insurance.

    Paid leave.

    Professional development opportunities.

    Flexible working environment.

    Established technology company providing
    software solutions to customers worldwide.

    """


    prediction = predict_job(
        text
    )


    job_details = {

        "job_title":
            "Software Engineer",

        "company":
            "Demo Technology Company",

        "location":
            "Hyderabad",

        "salary":
            "₹5-8 LPA",

        "experience":
            "0 to 2 years",

        "employment_type":
            "Full Time",

        "education":
            "B.Tech",

        "industry":
            "Information Technology"

    }


    fake_probability = prediction[
        "fake_probability"
    ]


    risk_score = round(
        fake_probability * 100,
        2
    )


    if risk_score <= 30:

        risk_level = "LOW"

    elif risk_score <= 60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    return jsonify({

        "success":
            True,

        "analysis_status":
            "COMPLETED",

        "prediction":
            prediction["result"],

        "fake_probability":
            round(
                prediction[
                    "fake_probability"
                ] * 100,
                2
            ),

        "real_probability":
            round(
                prediction[
                    "real_probability"
                ] * 100,
                2
            ),

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "reasons":
            [],

        "job_details":
            job_details,

        "model_metrics":
            MODEL_METRICS

    })


# =========================================================
# DEMO FAKE JOB
# =========================================================

@app.route(
    "/demo/fake-job",
    methods=["GET"]
)
def demo_fake_job():

    text = """

    URGENT JOB OPPORTUNITY!!!

    Work from home and earn huge income quickly.

    No experience required.

    Guaranteed income of $5000 per week.

    Limited vacancies available.

    To start your job immediately,
    send your personal information
    and pay a registration fee.

    Pay a processing fee of $99 today.

    Easy money and immediate joining.

    Don't miss this amazing opportunity.

    """


    prediction = predict_job(
        text
    )


    fake_probability = prediction[
        "fake_probability"
    ]


    risk_score = min(

        round(
            fake_probability * 100 + 25
        ),

        100

    )


    if risk_score <= 30:

        risk_level = "LOW"

    elif risk_score <= 60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    reasons = [

        "Registration fee requested",

        "Processing fee requested",

        "Personal information requested",

        "Promises unusually high income",

        "Urgent hiring language detected",

        "No experience required",

        "Guaranteed income claim"

    ]


    job_details = {

        "job_title":
            "Work From Home Opportunity",

        "company":
            "Unknown Company",

        "location":
            "Not specified",

        "salary":
            "$5000 per week",

        "experience":
            "No experience required",

        "employment_type":
            "Not specified",

        "education":
            "Not specified",

        "industry":
            "Not specified"

    }


    return jsonify({

        "success":
            True,

        "analysis_status":
            "COMPLETED",

        "prediction":
            prediction["result"],

        "fake_probability":
            round(
                fake_probability * 100,
                2
            ),

        "real_probability":
            round(
                prediction[
                    "real_probability"
                ] * 100,
                2
            ),

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "reasons":
            reasons,

        "job_details":
            job_details,

        "model_metrics":
            MODEL_METRICS

    })


# =========================================================
# DETECT JOB
# =========================================================

@app.route(
    "/detect",
    methods=["POST"]
)
def detect_job():

    try:

        # =================================================
        # GET REQUEST JSON
        # =================================================

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "success":
                    False,

                "error":
                    "Request body must contain JSON."

            }), 400


        # =================================================
        # GET URL
        # =================================================

        url = data.get(
            "url",
            ""
        ).strip()


        if not url:

            return jsonify({

                "success":
                    False,

                "error":
                    "Job URL is required."

            }), 400


        # =================================================
        # VALIDATE URL
        # =================================================

        if not (

            url.startswith(
                "http://"
            )

            or

            url.startswith(
                "https://"
            )

            or

            url.startswith(
                "file:///"
            )

        ):

            return jsonify({

                "success":
                    False,

                "error":
                    "Please enter a valid HTTP, HTTPS or local HTML URL."

            }), 400


        # =================================================
        # URL ANALYSIS
        # =================================================

        url_analysis = analyze_url(
            url
        )


        # =================================================
        # SCRAPE WEBPAGE
        # =================================================

        try:

            page = scrape_webpage(
                url
            )

        except ScrapeError as e:

            return jsonify({

                "success":
                    False,

                "analysis_status":
                    "UNAVAILABLE",

                "prediction":
                    None,

                "fake_probability":
                    None,

                "real_probability":
                    None,

                "risk_score":
                    None,

                "risk_level":
                    "UNKNOWN",

                "reasons":
                    [],

                "url":
                    url,

                "url_analysis":
                    url_analysis,

                "model_metrics":
                    MODEL_METRICS,

                "error":
                    str(e),

                "message":
                    "The webpage could not be analyzed. "
                    "This does not mean that the job is fake. "
                    "The website may require login, block automated access, "
                    "use protected content, or provide insufficient readable "
                    "job information."

            }), 200


        # =================================================
        # PAGE INFORMATION
        # =================================================

        page_title = page.get(
            "page_title",
            ""
        )


        headings = page.get(
            "headings",
            []
        )


        page_text = page.get(
            "text",
            ""
        )


        # =================================================
        # CHECK PAGE CONTENT
        # =================================================

        if len(
            page_text.strip()
        ) < 100:

            return jsonify({

                "success":
                    False,

                "analysis_status":
                    "UNAVAILABLE",

                "prediction":
                    None,

                "fake_probability":
                    None,

                "real_probability":
                    None,

                "risk_score":
                    None,

                "risk_level":
                    "UNKNOWN",

                "reasons":
                    [],

                "url":
                    url,

                "page_title":
                    page_title,

                "headings":
                    headings,

                "url_analysis":
                    url_analysis,

                "model_metrics":
                    MODEL_METRICS,

                "error":
                    "The webpage does not contain enough readable information.",

                "message":
                    "The job could not be reliably analyzed. "
                    "This does not mean that the job is fake.",

                "extraction_method":
                    page.get(
                        "method",
                        "Unknown"
                    ),

                "final_url":
                    page.get(
                        "final_url",
                        url
                    )

            }), 200


        # =================================================
        # EXTRACT JOB DETAILS
        # =================================================

        job_details = extract_job_details(

            page_title,

            headings,

            page_text

        )


        # =================================================
        # MACHINE LEARNING PREDICTION
        # =================================================

        prediction = predict_job(
            page_text
        )


        # =================================================
        # DETECTION REASONS
        # =================================================

        reasons = generate_reasons(
            url_analysis
        )


        suspicious_phrases = [

            "registration fee",

            "application fee",

            "pay a fee",

            "pay registration",

            "send your personal information",

            "send personal information",

            "earn huge income",

            "earn money quickly",

            "urgent hiring",

            "immediate joining",

            "limited vacancies",

            "no experience required",

            "guaranteed income",

            "easy money",

            "work from home and earn",

            "pay money",

            "processing fee",

            "security deposit"

        ]


        text_lower = page_text.lower()


        for phrase in suspicious_phrases:

            if phrase in text_lower:

                reasons.append(

                    f"Suspicious phrase detected: {phrase}"

                )


        reasons = list(
            dict.fromkeys(
                reasons
            )
        )


        # =================================================
        # RISK SCORE
        # =================================================

        risk_score, risk_level = calculate_risk_score(

            prediction,

            url_analysis

        )


        # =================================================
        # FINAL RESPONSE
        # =================================================

        return jsonify({

            "success":
                True,

            "analysis_status":
                "COMPLETED",

            "prediction":
                prediction["result"],

            "url":
                url,

            "page_title":
                page_title,

            "headings":
                headings,

            "job_details":
                job_details,

            "fake_probability":
                round(
                    prediction[
                        "fake_probability"
                    ] * 100,
                    2
                ),

            "real_probability":
                round(
                    prediction[
                        "real_probability"
                    ] * 100,
                    2
                ),

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "reasons":
                reasons,

            "url_analysis":
                url_analysis,

            "model_metrics":
                MODEL_METRICS,

            "extraction_method":
                page.get(
                    "method",
                    "Unknown"
                ),

            "final_url":
                page.get(
                    "final_url",
                    url
                )

        })


    except Exception as e:

        return jsonify({

            "success":
                False,

            "analysis_status":
                "ERROR",

            "error":
                str(e),

            "message":
                "An unexpected error occurred while analyzing the job."

        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print()

    print("=" * 60)

    print(
        "        FAKE JOB DETECTION API"
    )

    print("=" * 60)

    print()

    print(
        "Server running at:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "Available endpoints:"
    )

    print(
        "GET  /"
    )

    print(
        "GET  /demo/real-job"
    )

    print(
        "GET  /demo/fake-job"
    )

    print(
        "POST /detect"
    )

    print()

    print("=" * 60)

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )