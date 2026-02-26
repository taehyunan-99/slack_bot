# src/main.py
import logging
import os
import yaml
from dotenv import load_dotenv
from src.crawler import fetch_news
from src.slack_sender import format_keyword_block, send_to_slack

load_dotenv()  # 로컬 .env 파일 로드 (GitHub Actions에서는 무시됨)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_pipeline(slack_webhook: str, config_path: str = "config/keywords.yaml") -> None:
    config = load_config(config_path)
    keywords = config["keywords"]
    count = config["settings"]["articles_per_keyword"]
    lang = config["settings"]["language"]
    country = config["settings"]["country"]

    blocks = []
    for kw in keywords:
        logger.info("크롤링 시작: %s", kw["name"])
        articles = fetch_news(kw["query"], count=count, lang=lang, country=country)
        logger.info("수집된 기사 수: %d (keyword=%s)", len(articles), kw["name"])
        blocks.extend(format_keyword_block(kw["name"], kw["emoji"], articles))
    logger.info("Slack 전송 중...")
    success = send_to_slack(slack_webhook, blocks)
    if not success:
        raise RuntimeError("Slack 전송 실패")
    logger.info("완료")


if __name__ == "__main__":
    run_pipeline(
        slack_webhook=os.environ["SLACK_WEBHOOK_URL"],
    )
