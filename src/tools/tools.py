import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, and Snippets."""
    results = tavily.search(query=query, max_results=5)

    out = []
    for r in results.get("results", []):
        out.append(
            f"Title: {r.get('title')}\nURL: {r.get('url')}\nSnippet: {r.get('content', '')[:300]}\n"
        )

    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract clean readable content from a URL.
    Uses multiple extraction strategies for better reliability.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # Fetch page
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        # Strategy 1: Trafilatura (highest precision)
        extracted = trafilatura.extract(
            html,
            include_links=False,
            include_images=False,
            output_format="txt"
        )
        if extracted and len(extracted.strip()) > 150:
            return extracted.strip()

        # Strategy 2: Readability-lxml fallback
        doc = Document(html)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        if text and len(text.strip()) > 150:
            return text.strip()

        # Strategy 3: Raw BeautifulSoup fallback
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        raw_text = soup.get_text(separator="\n", strip=True)
        return raw_text[:3000] if raw_text else "No extractable content found."

    except Exception as e:
        return f"Error scraping {url}: {e}"