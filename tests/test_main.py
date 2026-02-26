# tests/test_main.py
import pytest
from unittest.mock import patch
from src.main import load_config, run_pipeline

def test_load_config():
    config = load_config("config/keywords.yaml")
    assert "keywords" in config
    assert len(config["keywords"]) == 8
    assert config["settings"]["articles_per_keyword"] == 3

def test_run_pipeline_calls_all_components():
    with patch("src.main.fetch_news", return_value=[{"title": "t", "link": "l", "summary": "s"}]) as mock_fetch, \
         patch("src.main.send_to_slack", return_value=True) as mock_send:

        run_pipeline(
            slack_webhook="https://hooks.slack.com/test",
            config_path="config/keywords.yaml"
        )

    assert mock_fetch.call_count == 8
    assert mock_send.call_count == 1
