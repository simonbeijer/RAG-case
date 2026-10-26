import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pages(pages: list[dict], config: dict) -> list[dict]:
    """Split all pages"""
    chunks = []
    for page in pages:
        chunks.extend(split_page(page, config["chunk_size"], config["chunk_overlap"]))
    return chunks

def split_page(page: dict, chunk_size: int, chunk_overlap: int) -> list[dict]:
    """Split page into chunks. Remove chunks under 100 characters. Page title first in every chunk. Return chunks with url, title, text"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # Title first so every chunk knows which page it is from
    return [
        {"url": page["url"], "title": page["title"], "text": f"{page['title']}\n\n{part}"}
        for part in splitter.split_text(page["text"])
        if len(part) >= 100
    ]

def save_chunks(chunks: list[dict], path: Path) -> None:
    """Save chunks into JSON"""
    path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")