"""Live fetcher for rsmt.ac.in — used as hybrid-mode fallback when local RAG cannot answer."""
from __future__ import annotations

import re
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.rsmt.ac.in"
HEADERS = {"User-Agent": "Mozilla/5.0 (RSMT-Chatbot)"}
TIMEOUT = 10

# Keyword -> page URL map (extend as needed)
URL_MAP: dict[str, str] = {
    "fee": "/cms/fee-structure/87",
    "fees": "/cms/fee-structure/87",
    "tuition": "/cms/fee-structure/87",
    "mca": "/cms/mca/19",
    "mba": "/cms/mba/20",
    "bca": "/cms/bca/21",
    "bba": "/cms/bba/22",
    "admission": "/cms/admission-procedure/24",
    "apply": "/cms/admission-procedure/24",
    "eligibility": "/cms/admission-procedure/24",
    "hostel": "/cms/hostel-transportation/26",
    "transport": "/cms/hostel-transportation/26",
    "scholarship": "/cms/scholarship-bank-finance/25",
    "library": "/cms/library/42",
    "lab": "/cms/computer-lab/41",
    "computer lab": "/cms/computer-lab/41",
    "sports": "/cms/sports/47",
    "cafeteria": "/cms/cafeteria/45",
    "health": "/cms/health-care/44",
    "guest house": "/cms/guest-house/48",
    "vision": "/cms/vision-mission/35",
    "mission": "/cms/vision-mission/35",
    "pedagogy": "/cms/pedagogy/36",
    "inspiration": "/cms/our-inspiration/34",
    "history": "/cms/our-inspiration/34",
    "founder": "/cms/our-inspiration/34",
    "placement": "/cms/training-placement-cell/54",
    "recruiter": "/cms/list-of-recruiters/59",
    "recruiters": "/cms/list-of-recruiters/59",
    "training": "/cms/training-placement-cell/54",
    "internship": "/cms/training-placement-cell/54",
    "contact": "/contactUs",
    "phone": "/contactUs",
    "email": "/contactUs",
    "address": "/contactUs",
    "news": "/Newsevent",
    "event": "/Newsevent",
    "events": "/Newsevent",
    "latest": "/Newsevent",
    "announcement": "/Newsevent",
    "nirf": "/cms/nirf/86",
    "milestone": "/cms/milestones-rsmt/63",
    "press": "/cms/press-notes/64",
    "alumni": "/cms/alumni/73",
    "faculty": "/members/computer",
    "iqac": "/Iqac",
    "grievance": "/cms/student-grievance-cell/68",
}


def _pick_url(question: str) -> str:
    q = question.lower()
    # Prefer the longest matching keyword
    matches = sorted(
        (kw for kw in URL_MAP if kw in q),
        key=len,
        reverse=True,
    )
    if matches:
        return urljoin(BASE, URL_MAP[matches[0]])
    return BASE  # homepage as default


def _clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Strip nav/footer/script/style noise
    for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    # Collapse whitespace
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def fetch_live(question: str, max_chars: int = 6000) -> Optional[dict]:
    """Fetch the most relevant rsmt.ac.in page for `question`. Returns dict or None on failure."""
    url = _pick_url(question)
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        return {"url": url, "text": "", "error": str(e)}
    text = _clean_text(r.text)[:max_chars]
    return {"url": url, "text": text, "error": None}


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "What is the MCA fee?"
    res = fetch_live(q)
    print(f"URL: {res['url']}")
    print(f"---\n{res['text'][:1500]}")
