# tests/test_summarizer.py
import pytest
from unittest.mock import patch, MagicMock
from src.summarizer import summarize_articles, build_prompt

def test_build_prompt():
    articles = [
        {"title": "AI 발전", "link": "https://example.com/1", "summary": "내용1"},
        {"title": "LLM 출시", "link": "https://example.com/2", "summary": "내용2"},
    ]
    prompt = build_prompt("AI", articles)
    assert "AI" in prompt
    assert "AI 발전" in prompt
    assert "LLM 출시" in prompt

def test_summarize_articles_returns_string():
    mock_response = MagicMock()
    mock_response.text = "AI 분야에서 중요한 발전이 있었습니다."

    articles = [{"title": "AI 뉴스", "link": "https://example.com", "summary": "내용"}]

    with patch("google.generativeai.GenerativeModel") as mock_model_class:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = summarize_articles("AI", articles, api_key="test-key")

    assert isinstance(result, str)
    assert len(result) > 0

def test_summarize_articles_empty_list():
    result = summarize_articles("AI", [], api_key="test-key")
    assert result == "수집된 뉴스가 없습니다."
