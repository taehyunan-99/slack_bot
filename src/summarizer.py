# src/summarizer.py
import logging
import time
import google.generativeai as genai

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 15  # seconds


def build_prompt(keyword: str, articles: list[dict]) -> str:
    articles_text = "\n".join([
        f"{i+1}. 제목: {a['title']}\n   내용: {a['summary']}\n   링크: {a['link']}"
        for i, a in enumerate(articles)
    ])
    return f"""다음은 '{keyword}' 관련 최신 뉴스 {len(articles)}건입니다.

{articles_text}

위 뉴스들을 한국어로 3-4문장으로 핵심만 요약해주세요.
주요 트렌드와 중요한 내용을 중심으로 작성하고, 각 뉴스의 링크는 포함하지 마세요."""


def _fallback_summary(articles: list[dict]) -> str:
    lines = "\n".join([f"• {a['title']}" for a in articles])
    return f"(요약 불가 - 원본 제목)\n{lines}"


def summarize_articles(keyword: str, articles: list[dict], api_key: str) -> str:
    if not articles:
        return "수집된 뉴스가 없습니다."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    prompt = build_prompt(keyword, articles)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = model.generate_content(prompt)
            usage = response.usage_metadata
            logger.info(
                "Gemini 토큰 사용량 (keyword=%s): input=%d, output=%d, total=%d",
                keyword,
                usage.prompt_token_count,
                usage.candidates_token_count,
                usage.total_token_count,
            )
            return response.text
        except Exception as e:
            logger.warning("Gemini API 오류 (keyword=%s, attempt=%d/%d): %s", keyword, attempt, MAX_RETRIES, e)
            if attempt < MAX_RETRIES:
                logger.info("%d초 후 재시도...", RETRY_DELAY)
                time.sleep(RETRY_DELAY)

    logger.error("Gemini API 최대 재시도 초과 (keyword=%s) - 원본 출력", keyword)
    return _fallback_summary(articles)
