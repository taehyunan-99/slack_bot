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
    mock_entry = MagicMock()
    mock_entry.title = "AI 뉴스 제목"
    mock_entry.link = "https://example.com"
    mock_entry.published = "Mon, 26 Feb 2026 00:00:00 GMT"
    mock_entry.summary = "뉴스 요약 내용"

    mock_feed = MagicMock()
    mock_feed.entries = [mock_entry] * 10

    with patch("feedparser.parse", return_value=mock_feed):
        result = fetch_news("AI", count=5)

    assert len(result) == 5
    assert result[0]["title"] == "AI 뉴스 제목"
    assert result[0]["link"] == "https://example.com"

def test_fetch_news_empty_feed():
    mock_feed = MagicMock()
    mock_feed.entries = []

    with patch("feedparser.parse", return_value=mock_feed):
        result = fetch_news("존재하지않는키워드12345", count=5)

    assert result == []
