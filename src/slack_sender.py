# src/slack_sender.py
import logging
import requests
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
KST = timezone(timedelta(hours=9))


def format_keyword_block(keyword: str, articles: list[dict]) -> list:
    items = "\n".join([f"• <{a['link']}|{a['title']}>" for a in articles])
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{keyword} 뉴스* ({len(articles)}건)\n{items}"},
        },
        {"type": "divider"},
    ]


def send_to_slack(webhook_url: str, blocks: list) -> bool:
    if not blocks:
        logger.warning("전송할 기사 없음, Slack 전송 생략")
        return True
    today = datetime.now(tz=KST).strftime("%Y년 %m월 %d일")
    header = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📰 오늘의 테크 뉴스 브리핑 - {today}"},
        }
    ]
    response = requests.post(
        webhook_url,
        json={"blocks": header + blocks},
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    if response.status_code != 200:
        logger.error("Slack 전송 실패: status=%d body=%s", response.status_code, response.text)
        return False
    return True
