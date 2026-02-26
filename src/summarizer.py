# src/summarizer.py
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)


def build_prompt(keyword: str, articles: list[dict]) -> str:
    articles_text = "\n".join([
        f"{i+1}. 제목: {a['title']}\n   내용: {a['summary']}\n   링크: {a['link']}"
        for i, a in enumerate(articles)
    ])
    return f"""다음은 '{keyword}' 관련 최신 뉴스 {len(articles)}건입니다.

{articles_text}

위 뉴스들을 한국어로 3-4문장으로 핵심만 요약해주세요.
주요 트렌드와 중요한 내용을 중심으로 작성하고, 각 뉴스의 링크는 포함하지 마세요."""


def summarize_articles(keyword: str, articles: list[dict], api_key: str) -> str:
    if not articles:
        return "수집된 뉴스가 없습니다."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = build_prompt(keyword, articles)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error("Gemini API 오류 (keyword=%s): %s", keyword, e)
        return f"요약 생성 실패: {e}"
