def calculate_risk_score(prediction, url_analysis):

    # ML fake probability
    score = prediction["fake_probability"] * 100

    # Add risk for suspicious URL indicators
    if not url_analysis["https"]:
        score += 10

    score += len(url_analysis["suspicious_words"]) * 5

    if url_analysis["hyphen_count"] >= 3:
        score += 5

    if url_analysis["subdomain_count"] >= 3:
        score += 5

    if url_analysis["url_length"] > 100:
        score += 5

    if url_analysis["special_character_count"] >= 5:
        score += 5

    # Keep score between 0 and 100
    score = min(round(score), 100)

    # Determine risk level
    if score <= 30:
        risk_level = "LOW"

    elif score <= 60:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    return score, risk_level