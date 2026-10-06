from urllib.parse import urlparse
import re


def analyze_url(url):

    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path

    features = {}

    # 1. HTTPS check
    features["https"] = parsed.scheme == "https"

    # 2. URL length
    features["url_length"] = len(url)

    # 3. Domain length
    features["domain_length"] = len(domain)

    # 4. Number of dots in domain
    features["dot_count"] = domain.count(".")

    # 5. Number of hyphens in domain
    features["hyphen_count"] = domain.count("-")

    # 6. Number of subdomains
    parts = domain.split(".")

    if len(parts) > 2:
        features["subdomain_count"] = len(parts) - 2
    else:
        features["subdomain_count"] = 0

    # 7. Suspicious words
    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "bonus",
        "free",
        "winner",
        "urgent"
    ]

    found_words = []

    for word in suspicious_words:
        if word in url.lower():
            found_words.append(word)

    features["suspicious_words"] = found_words

    # 8. Special characters
    special_characters = len(re.findall(r"[@?=&%]", url))

    features["special_character_count"] = special_characters

    return features


# ==========================================
# TEST MULTIPLE URLs
# ==========================================

test_urls = [
    "https://example.com/jobs/software-developer",
    "http://free-job-bonus.com/login/verify",
    "https://secure-account-update.com/job",
    "https://jobs.google.com/software-engineer"
]


for url in test_urls:

    result = analyze_url(url)

    print("\n================================")
    print("URL:", url)

    for key, value in result.items():
        print(key, ":", value)