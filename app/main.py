"""
Модуль для инициирования Fastapi приложения, также роута "/" для редиректа вебхук от телеграмма - нашему боту
"""

import logging

from aiogram.types import Update
from fastapi import FastAPI, Request

from app.bot import bot, dp
from app.config import WEBHOOK_URL

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with aiogram bot!"}


# Обработчик для webhook
@app.post("/")
async def webhook(request: Request):
    try:
        update = Update(**await request.json())
        await dp._process_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Failed to process update: {e}")
        return {"status": "error", "message": str(e)}
