# src/slack_sender.py
import requests
from datetime import datetime


def format_keyword_block(keyword: str, emoji: str, summary: str, articles: list[dict]) -> str:
    links = " | ".join([f"<{a['link']}|{a['title'][:20]}...>" for a in articles])
    return f"{emoji} *{keyword} 뉴스* ({len(articles)}건)\n>{summary}\n🔗 {links}"


def send_to_slack(webhook_url: str, message: str) -> bool:
    today = datetime.now().strftime("%Y년 %m월 %d일")
    full_message = f"*📰 오늘의 테크 뉴스 브리핑 - {today}*\n\n{message}"

    response = requests.post(
        webhook_url,
        json={"text": full_message},
        headers={"Content-Type": "application/json"},
    )
    return response.status_code == 200
