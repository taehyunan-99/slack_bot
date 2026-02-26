# slack_bot

## Project Overview
GitHub Actions 기반 뉴스 크롤링 봇. 구글 뉴스 RSS를 통해 키워드별 뉴스를 수집하고, Gemini API로 요약 후 Slack으로 전송.

## Tech Stack
- **Runtime**: Python 3.11+
- **Scheduler**: GitHub Actions (cron)
- **News Source**: Google News RSS
- **AI Summary**: Google Gemini API
- **Notification**: Slack Webhook

## Project Structure
```
slack_bot/
├── .github/workflows/    # GitHub Actions 워크플로우
├── src/
│   ├── crawler.py        # RSS 크롤링
│   ├── summarizer.py     # Gemini API 요약
│   └── slack_sender.py   # Slack 전송
├── config/
│   └── keywords.yaml     # 키워드 설정
├── tests/
├── requirements.txt
└── CLAUDE.md
```

## Key Conventions
- 환경변수: `GEMINI_API_KEY`, `SLACK_WEBHOOK_URL` (GitHub Secrets)
- 키워드 설정: `config/keywords.yaml`에서 관리
- 테스트: pytest 사용

## Commands
```bash
pip install -r requirements.txt
python src/crawler.py          # 크롤링 테스트
pytest tests/                  # 테스트 실행
```
