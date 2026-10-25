import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

def get_urls(sitemap_url: str, skip_paths: list[str]) -> list[str]:
    """Read sitemap. Return urls without skipped urls"""
    root = ET.fromstring(fetch_page(sitemap_url))
    urls = [loc.text.strip() for loc in root.findall("sm:url/sm:loc", SITEMAP_NS)]
    # Skip urls from skip_paths
    return [url for url in urls if not any(urlparse(url).path.startswith(p) for p in skip_paths)]

def fetch_page(url: str) -> str:
    """Fetch content. Return HTML"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def clean_page(html: str) -> dict:
    """Remove nav, footer, script and style tags. Return title and text"""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["nav", "footer", "script", "style"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    text = soup.get_text(separator="\n", strip=True)
    return {"title": title, "text": text}

def save_pages(pages: list[dict], path: Path) -> None:
    """Save pages as JSON. Every page with url, title, text"""
    path.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
