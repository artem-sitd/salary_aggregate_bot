#!/bin/bash
export TELEGRAM_API_TOKEN='your-telegram-api-token'
export WEBHOOK_URL='https://yourdomain.com/webhook'
uvicorn app.main:app --host 0.0.0.0 --port 8000
