# tests/test_crawler.py
import pytest
from unittest.mock import patch, MagicMock
from src.crawler import fetch_news, build_rss_url

def test_build_rss_url():
    url = build_rss_url("AI", "ko", "KR")
    assert "news.google.com/rss/search" in url
    assert "AI" in url
    assert "hl=ko" in url
    assert "gl=KR" in url

def test_fetch_news_returns_list():
    entries = []
    for i in range(10):
        e = MagicMock()
        e.title = f"AI 뉴스 제목 {i}"
        e.link = f"https://example.com/{i}"
        e.published = "Mon, 26 Feb 2026 00:00:00 GMT"
        e.summary = f"뉴스 요약 {i}"
        entries.append(e)

    mock_feed = MagicMock()
    mock_feed.entries = entries

    with patch("feedparser.parse", return_value=mock_feed):
        result = fetch_news("AI", count=5)

    assert len(result) == 5
    assert result[0]["title"] == "AI 뉴스 제목 0"
    assert result[0]["link"] == "https://example.com/0"

def test_fetch_news_empty_feed():
    mock_feed = MagicMock()
    mock_feed.entries = []

    with patch("feedparser.parse", return_value=mock_feed):
        result = fetch_news("존재하지않는키워드12345", count=5)

    assert result == []
