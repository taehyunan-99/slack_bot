# src/main.py
import os
import yaml
from src.crawler import fetch_news
from src.summarizer import summarize_articles
from src.slack_sender import format_keyword_block, send_to_slack


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_pipeline(gemini_key: str, slack_webhook: str, config_path: str = "config/keywords.yaml") -> None:
    config = load_config(config_path)
    keywords = config["keywords"]
    count = config["settings"]["articles_per_keyword"]
    lang = config["settings"]["language"]
    country = config["settings"]["country"]

    blocks = []
    for kw in keywords:
        articles = fetch_news(kw["query"], count=count, lang=lang, country=country)
        summary = summarize_articles(kw["name"], articles, api_key=gemini_key)
        block = format_keyword_block(kw["name"], kw["emoji"], summary, articles)
        blocks.append(block)

    message = "\n\n".join(blocks)
    success = send_to_slack(slack_webhook, message)
    if not success:
        raise RuntimeError("Slack 전송 실패")


if __name__ == "__main__":
    run_pipeline(
        gemini_key=os.environ["GEMINI_API_KEY"],
        slack_webhook=os.environ["SLACK_WEBHOOK_URL"],
    )
