from app.chunk import split_page

def test_keep_url_and_title() -> None:
    """Test if every chunk has url and title from page"""
    page = {"url": "https://compileit.com/om-oss", "title": "Om oss", "text": "Vi bygger AI. " * 30}
    chunks = split_page(page, chunk_size=200, chunk_overlap=0)
    assert chunks
    for chunk in chunks:
        assert chunk["url"] == "https://compileit.com/om-oss"
        assert chunk["title"] == "Om oss"

def test_title_first() -> None:
    """Test if every chunk has title first"""
    page = {"url": "https://compileit.com/om-oss", "title": "Om oss", "text": "Vi bygger AI. " * 30}
    chunks = split_page(page, chunk_size=200, chunk_overlap=0)
    assert chunks
    for chunk in chunks:
        assert chunk["text"].startswith("Om oss\n\n")

def test_remove_short_text() -> None:
    """Test if texts under 100 chars are removed. Even with long title"""
    page = {"url": "https://compileit.com/kort", "title": "Lång titel " * 20, "text": "Kort text."}
    assert split_page(page, chunk_size=200, chunk_overlap=0) == []

def test_split_long_page() -> None:
    """Test if page length that exceeds chunk_size create more than one chunk"""
    page = {"url": "https://compileit.com/om-oss", "title": "Om oss", "text": "Vi bygger AI. " * 30}
    assert len(split_page(page, chunk_size=200, chunk_overlap=0)) > 1