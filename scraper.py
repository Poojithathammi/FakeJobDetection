import requests
import re

from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse


class ScrapeError(Exception):
    pass


# =========================================================
# EXTRACT WEBPAGE CONTENT
# =========================================================

def extract_page_content(html):

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted elements
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe"
    ]):
        tag.decompose()

    # Page title
    page_title = ""

    if soup.title:
        page_title = soup.title.get_text(
            " ",
            strip=True
        )

    # Headings
    headings = []

    for heading in soup.find_all([
        "h1",
        "h2",
        "h3",
        "h4"
    ]):

        text = heading.get_text(
            " ",
            strip=True
        )

        if text:
            headings.append(text)

    headings = list(dict.fromkeys(headings))

    # Visible text
    visible_text = " ".join(
        soup.get_text(
            " ",
            strip=True
        ).split()
    )

    # =====================================================
    # DETECT ACCESS DENIED / BLOCKED PAGE
    # =====================================================

    blocked_phrases = [
        "access denied",
        "403 forbidden",
        "request blocked",
        "bot detected",
        "verify you are human",
        "captcha",
        "security check",
        "automated access",
        "unusual traffic",
        "request unsuccessful",
        "forbidden",
        "temporarily blocked",
        "access denied by",
        "you have been blocked"
    ]

    text_lower = visible_text.lower()
    title_lower = page_title.lower()

    for phrase in blocked_phrases:

        if (
            phrase in text_lower
            or phrase in title_lower
        ):

            raise ScrapeError(
                "Website blocked automated access. "
                "The job cannot be reliably analyzed."
            )

    return {
        "page_title": page_title,
        "headings": headings,
        "text": visible_text,
        "html": html
    }


# =========================================================
# EXTRACT JOB DETAILS
# =========================================================

def extract_job_details(
    page_title,
    headings,
    text
):

    full_text = " ".join(
        [page_title] +
        headings +
        [text]
    )

    search_text = full_text[:50000]

    details = {

        "job_title": "",

        "company": "",

        "location": "",

        "salary": "",

        "experience": "",

        "employment_type": "",

        "education": "",

        "industry": ""

    }

    # =====================================================
    # JOB TITLE
    # =====================================================

    if headings:

        blocked_headings = [

            "job description",
            "job details",
            "requirements",
            "responsibilities",
            "about us",
            "benefits",
            "apply now",
            "company overview",
            "description",
            "qualifications"

        ]

        for heading in headings:

            heading_clean = heading.strip()

            if (
                len(heading_clean) > 2
                and len(heading_clean) < 150
                and heading_clean.lower()
                not in blocked_headings
            ):

                details["job_title"] = heading_clean

                break

    # If no heading was found
    if not details["job_title"]:

        if page_title:

            title = page_title.strip()

            if len(title) > 2:

                details["job_title"] = title


    # =====================================================
    # COMPANY
    # =====================================================

    company_patterns = [

        r"(?:company|employer|organization)"
        r"\s*[:\-]\s*([^|,;\n]{2,100})",

        r"(?:posted by|recruiter)"
        r"\s*[:\-]\s*([^|,;\n]{2,100})",

        r"(?:company name)"
        r"\s*[:\-]\s*([^|,;\n]{2,100})"

    ]

    for pattern in company_patterns:

        match = re.search(
            pattern,
            search_text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 2:

                details["company"] = value

                break


    # =====================================================
    # LOCATION
    # =====================================================

    location_patterns = [

        r"(?:location|locations|job location)"
        r"\s*[:\-]\s*([^|;\n]{2,150})",

        r"(?:based in)"
        r"\s+([^|;\n]{2,100})",

        r"(?:work location)"
        r"\s*[:\-]\s*([^|;\n]{2,150})"

    ]

    for pattern in location_patterns:

        match = re.search(
            pattern,
            search_text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 2:

                details["location"] = value

                break


    # =====================================================
    # SALARY
    # =====================================================

    salary_patterns = [

        r"(?:salary|pay|compensation|ctc)"
        r"\s*[:\-]?\s*"
        r"(₹?\s?[\d,]+"
        r"(?:\s*-\s*₹?\s?[\d,]+)?"
        r"\s*(?:lpa|lakhs?|per annum|annually|"
        r"month|monthly|year|yr)?)",

        r"(₹\s?[\d,]+"
        r"(?:\s*-\s*₹?\s?[\d,]+)?"
        r"\s*(?:LPA|lakh|lakhs|per annum)?)",

        r"(\$\s?[\d,]+"
        r"(?:\s*-\s*\$?\s?[\d,]+)?"
        r"\s*(?:per year|per month|annually|monthly)?)"

    ]

    for pattern in salary_patterns:

        match = re.search(
            pattern,
            search_text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 1:

                details["salary"] = value

                break


    # =====================================================
    # EXPERIENCE
    # =====================================================

    experience_patterns = [

        r"(?:experience|work experience|required experience)"
        r"\s*[:\-]?\s*"
        r"(\d+\s*(?:to|-)\s*\d+\s*(?:years?|yrs?)?)",

        r"(\d+\s*(?:to|-)\s*\d+\s*"
        r"(?:years?|yrs?)\s*(?:of)?\s*experience)",

        r"(\d+\+?\s*(?:years?|yrs?)"
        r"\s*(?:of)?\s*experience)"

    ]

    for pattern in experience_patterns:

        match = re.search(
            pattern,
            search_text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 1:

                details["experience"] = value

                break


    # =====================================================
    # EMPLOYMENT TYPE
    # =====================================================

    employment_types = [

        "full time",
        "full-time",
        "part time",
        "part-time",
        "contract",
        "internship",
        "temporary",
        "freelance",
        "permanent"

    ]

    for employment_type in employment_types:

        if employment_type in search_text.lower():

            details["employment_type"] = (
                employment_type.title()
            )

            break


    # =====================================================
    # EDUCATION
    # =====================================================

    education_patterns = [

        r"(?:education|qualification|required education)"
        r"\s*[:\-]\s*([^|;\n]{2,150})",

        r"(B\.?Tech|B\.?E\.?|M\.?Tech|M\.?E\.?|"
        r"MBA|MCA|BCA|BSc|B\.?Sc|MSc|M\.?Sc|"
        r"Bachelor'?s degree|Master'?s degree|Ph\.?D)"

    ]

    for pattern in education_patterns:

        match = re.search(
            pattern,
            search_text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 1:

                details["education"] = value

                break


    # =====================================================
    # INDUSTRY
    # =====================================================

    industry_patterns = [

        r"(?:industry|sector)"
        r"\s*[:\-]\s*([^|;\n]{2,120})",

        r"(?:industry type)"
        r"\s*[:\-]\s*([^|;\n]{2,120})"

    ]

    for pattern in industry_patterns:

        match = re.search(
            pattern,
            search_text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 2:

                details["industry"] = value

                break


    return details


# =========================================================
# REQUESTS + BEAUTIFULSOUP
# =========================================================

def scrape_with_requests(url):

    headers = {

        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36",

        "Accept":
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,"
            "*/*;q=0.8",

        "Accept-Language":
            "en-US,en;q=0.9",

        "Connection":
            "keep-alive"

    }

    try:

        response = requests.get(

            url,

            headers=headers,

            timeout=15,

            allow_redirects=True

        )

    except requests.exceptions.Timeout:

        raise ScrapeError(
            "Website request timed out."
        )

    except requests.exceptions.ConnectionError:

        raise ScrapeError(
            "Could not connect to the website."
        )

    except requests.exceptions.RequestException as e:

        raise ScrapeError(
            f"Website request failed: {str(e)}"
        )

    if response.status_code == 401:

        raise ScrapeError(
            "Website requires authentication."
        )

    if response.status_code == 403:

        raise ScrapeError(
            "Website restricts automated access."
        )

    if response.status_code == 404:

        raise ScrapeError(
            "Job page was not found."
        )

    if response.status_code >= 400:

        raise ScrapeError(
            f"Website returned HTTP {response.status_code}."
        )

    result = extract_page_content(
        response.text
    )

    if len(result["text"]) < 200:

        raise ScrapeError(
            "The webpage returned insufficient job information."
        )

    result["method"] = (
        "Requests + BeautifulSoup"
    )

    result["final_url"] = response.url

    return result


# =========================================================
# PLAYWRIGHT + CHROMIUM
# =========================================================

def scrape_with_playwright(url):

    try:

        from playwright.sync_api import (
            sync_playwright,
            TimeoutError as PlaywrightTimeoutError
        )

    except ImportError:

        raise ScrapeError(
            "Playwright is not installed."
        )

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page(

                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/139.0.0.0 Safari/537.36"
                ),

                viewport={
                    "width": 1366,
                    "height": 768
                }

            )

            page.goto(

                url,

                wait_until="domcontentloaded",

                timeout=30000

            )

            page.wait_for_timeout(
                3000
            )

            html = page.content()

            final_url = page.url

            browser.close()


        result = extract_page_content(
            html
        )


        if len(result["text"]) < 200:

            raise ScrapeError(
                "Browser rendering did not provide enough readable job information."
            )


        result["method"] = (
            "Playwright + Chromium"
        )

        result["final_url"] = final_url

        return result


    except PlaywrightTimeoutError:

        raise ScrapeError(
            "Browser timed out while loading the webpage."
        )

    except ScrapeError:

        raise

    except Exception as e:

        raise ScrapeError(
            f"Browser extraction failed: {str(e)}"
        )


# =========================================================
# LOCAL HTML FILE
# =========================================================

def scrape_local_file(url):

    try:

        file_path = url.replace(
            "file:///",
            ""
        )

        html = Path(
            file_path
        ).read_text(
            encoding="utf-8"
        )

        result = extract_page_content(
            html
        )

        if len(result["text"]) < 80:

            raise ScrapeError(
                "Local webpage contains insufficient text."
            )

        result["method"] = "Local HTML"

        result["final_url"] = url

        return result


    except Exception as e:

        if isinstance(e, ScrapeError):

            raise

        raise ScrapeError(
            f"Could not read local webpage: {str(e)}"
        )


# =========================================================
# MAIN WEBPAGE SCRAPER
# =========================================================

def scrape_webpage(url):

    # Local HTML
    if url.startswith("file:///"):

        return scrape_local_file(url)


    # URL validation
    parsed = urlparse(url)

    if parsed.scheme not in [
        "http",
        "https"
    ]:

        raise ScrapeError(
            "Only HTTP, HTTPS and local HTML URLs are supported."
        )


    errors = []


    # =====================================================
    # METHOD 1 - REQUESTS
    # =====================================================

    try:

        return scrape_with_requests(
            url
        )

    except ScrapeError as e:

        errors.append(
            f"Requests: {str(e)}"
        )


    # =====================================================
    # METHOD 2 - PLAYWRIGHT
    # =====================================================

    try:

        return scrape_with_playwright(
            url
        )

    except ScrapeError as e:

        errors.append(
            f"Playwright: {str(e)}"
        )


    # =====================================================
    # BOTH FAILED
    # =====================================================

    raise ScrapeError(

        "Automatic webpage analysis failed. "
        "The website may require login, block automated access, "
        "use protected content, or provide insufficient readable "
        "job information."

    )