# tests/test_slack_sender.py
import pytest
from unittest.mock import patch, MagicMock
from src.slack_sender import format_keyword_block, send_to_slack

def test_format_keyword_block():
    articles = [
        {"title": "AI 뉴스1", "link": "https://example.com/1"},
        {"title": "AI 뉴스2", "link": "https://example.com/2"},
    ]
    block = format_keyword_block(
        keyword="AI",
        emoji="🤖",
        summary="AI 분야 요약 내용",
        articles=articles
    )
    assert "AI" in block
    assert "🤖" in block
    assert "AI 분야 요약 내용" in block
    assert "https://example.com/1" in block

def test_send_to_slack_success():
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("requests.post", return_value=mock_response):
        result = send_to_slack("https://hooks.slack.com/test", "테스트 메시지")

    assert result is True

def test_send_to_slack_failure():
    mock_response = MagicMock()
    mock_response.status_code = 400

    with patch("requests.post", return_value=mock_response):
        result = send_to_slack("https://hooks.slack.com/test", "테스트 메시지")

    assert result is False
