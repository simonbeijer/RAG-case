import time

from app.config import BACKEND_DIR, load_config
from app.chunk import chunk_pages, save_chunks
from app.scrape import clean_page, fetch_page, get_urls, save_pages
from app.index import embed_chunks, save_embeddings
from app.llm import get_embedding_model

def scrape_site(config: dict) -> list[dict]:
    """Fetch and clean pages one at a time. Skip pages under 100 characters (3 retry). Return pages with url, title, text"""
    pages = []
    # One at a time: the server returns empty pages on concurrent requests
    for url in get_urls(config["sitemap_url"], config["skip_paths"]):
        page = clean_page(fetch_page(url))
        # Server sometimes returns only the title: try again, max 3 attempts in total
        for _ in range(2):
            if len(page["text"]) >= 100:
                break
            time.sleep(1)
            page = clean_page(fetch_page(url))
        if len(page["text"]) < 100:
            print(f"Skipped, under 100 characters: {url}")
            continue
        pages.append({"url": url, **page})
    return pages

def main() -> None:
    """Load config, scrape, chunk and embed. Save to data/pages.json, data/chunks.json and data/embeddings.npy"""
    config = load_config()
    pages = scrape_site(config)
    data_dir = BACKEND_DIR / "data"
    data_dir.mkdir(exist_ok=True)
    save_pages(pages, data_dir / "pages.json")
    chunks = chunk_pages(pages, config)
    save_chunks(chunks, data_dir / "chunks.json")
    embed_model = get_embedding_model(config)
    matrix = embed_chunks(chunks, embed_model)
    save_embeddings(matrix, data_dir / "embeddings.npy")


if __name__ == "__main__":
    main()
