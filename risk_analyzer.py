def generate_reasons(url_analysis):

    reasons = []

    # HTTPS
    if not url_analysis["https"]:
        reasons.append(
            "Website does not use HTTPS"
        )

    # Suspicious words
    suspicious_words = url_analysis["suspicious_words"]

    for word in suspicious_words:
        reasons.append(
            f"Suspicious word found in URL: {word}"
        )

    # Long URL
    if url_analysis["url_length"] > 100:
        reasons.append(
            "URL is unusually long"
        )

    # Many hyphens
    if url_analysis["hyphen_count"] >= 3:
        reasons.append(
            "Domain contains many hyphens"
        )

    # Many subdomains
    if url_analysis["subdomain_count"] >= 3:
        reasons.append(
            "URL contains many subdomains"
        )

    # Special characters
    if url_analysis["special_character_count"] >= 5:
        reasons.append(
            "URL contains many special characters"
        )

    return reasons