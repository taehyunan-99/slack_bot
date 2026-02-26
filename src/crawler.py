# src/crawler.py
import logging
import re
import feedparser
from urllib.parse import quote

logger = logging.getLogger(__name__)


def build_rss_url(query: str, lang: str = "ko", country: str = "KR") -> str:
    encoded = quote(query)
    return f"https://news.google.com/rss/search?q={encoded}&hl={lang}&gl={country}&ceid={country}:{lang}"


def _tokenize(title: str) -> set:
    # 특수문자 제거 후 2글자 이상 단어만 추출
    cleaned = re.sub(r"[^\w\s]", " ", str(title))
    return {w for w in cleaned.split() if len(w) >= 2}


def _is_similar(title_a: str, title_b: str, threshold: float = 0.5) -> bool:
    words_a = _tokenize(title_a)
    words_b = _tokenize(title_b)
    if not words_a or not words_b:
        return False
    overlap = len(words_a & words_b) / min(len(words_a), len(words_b))
    return overlap >= threshold


def deduplicate(articles: list[dict]) -> list[dict]:
    unique = []
    for article in articles:
        if not any(_is_similar(article["title"], seen["title"]) for seen in unique):
            unique.append(article)
    return unique


def fetch_news(query: str, count: int = 5, lang: str = "ko", country: str = "KR") -> list[dict]:
    url = build_rss_url(query, lang, country)
    feed = feedparser.parse(url)

    if feed.bozo:
        logger.warning("RSS 피드 파싱 경고 (query=%s): %s", query, feed.bozo_exception)

    articles = []
    for entry in feed.entries[:count * 3]:  # 중복 제거 후 count개 확보를 위해 더 많이 수집
        articles.append({
            "title": getattr(entry, "title", "제목 없음"),
            "link": getattr(entry, "link", ""),
            "published": getattr(entry, "published", ""),
            "summary": getattr(entry, "summary", ""),
        })

    articles = deduplicate(articles)[:count]

    if not articles:
        logger.warning("수집된 기사 없음 (query=%s)", query)

    return articles
