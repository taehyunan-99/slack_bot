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
    titles = [
        "삼성전자 신제품 출시 발표", "LG 반도체 투자 계획", "네이버 AI 서비스 확대",
        "카카오 클라우드 전략 공개", "현대차 자율주행 기술 개발", "SK 에너지 전환 사업",
        "쿠팡 물류 시스템 혁신", "배달의민족 수수료 정책", "토스 금융 서비스 출시", "당근마켓 광고 매출 성장"
    ]
    entries = []
    for i, title in enumerate(titles):
        e = MagicMock()
        e.title = title
        e.link = f"https://example.com/{i}"
        e.published = "Mon, 26 Feb 2026 00:00:00 GMT"
        e.summary = f"뉴스 요약 {i}"
        entries.append(e)

    mock_feed = MagicMock()
    mock_feed.entries = entries

    with patch("feedparser.parse", return_value=mock_feed):
        result = fetch_news("AI", count=5)

    assert len(result) == 5
    assert result[0]["title"] == "삼성전자 신제품 출시 발표"
    assert result[0]["link"] == "https://example.com/0"

def test_fetch_news_empty_feed():
    mock_feed = MagicMock()
    mock_feed.entries = []

    with patch("feedparser.parse", return_value=mock_feed):
        result = fetch_news("존재하지않는키워드12345", count=5)

    assert result == []
