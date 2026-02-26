# src/crawler.py
import logging
import feedparser
from urllib.parse import quote

logger = logging.getLogger(__name__)


def build_rss_url(query: str, lang: str = "ko", country: str = "KR") -> str:
    encoded = quote(query)
    return f"https://news.google.com/rss/search?q={encoded}&hl={lang}&gl={country}&ceid={country}:{lang}"


def fetch_news(query: str, count: int = 5, lang: str = "ko", country: str = "KR") -> list[dict]:
    url = build_rss_url(query, lang, country)
    feed = feedparser.parse(url)

    if feed.bozo:
        logger.warning("RSS 피드 파싱 경고 (query=%s): %s", query, feed.bozo_exception)

    articles = []
    for entry in feed.entries[:count]:
        articles.append({
            "title": getattr(entry, "title", "제목 없음"),
            "link": getattr(entry, "link", ""),
            "published": getattr(entry, "published", ""),
            "summary": getattr(entry, "summary", ""),
        })

    if not articles:
        logger.warning("수집된 기사 없음 (query=%s)", query)

    return articles
