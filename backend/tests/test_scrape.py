from app.scrape import clean_page

def test_remove_tags() -> None:
    """Test if nav, footer, script and style is removed from text"""
    html = (
        "<html><body>"
        "<nav>Menu</nav>"
        "<script>var x = 1;</script>"
        "<style>p { color: red; }</style>"
        "<footer>Contact</footer>"
        "</body></html>"
    )
    text = clean_page(html)["text"]
    assert "Menu" not in text
    assert "var x" not in text
    assert "color" not in text
    assert "Contact" not in text

def test_keeps_main_text() -> None:
    """ Test if main text outside of tags are kept"""
    html = "<html><body><nav>Menu</nav><p>Vi bygger AI.</p><footer>Contact</footer></body></html>"
    assert clean_page(html)["text"] == "Vi bygger AI."

def test_return_title() -> None:
    """Test if title is returned"""
    html = "<html><head><title>Compileit</title></head><body><p>Text</p></body></html>"
    assert clean_page(html)["title"] == "Compileit"


def test_missing_title_is_empty() -> None:
    """Test if page without title tag returns empty title"""
    html = "<html><body><p>Text</p></body></html>"
    assert clean_page(html)["title"] == ""
