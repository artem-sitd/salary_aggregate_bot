"""
Модуль для инициирования бота, создания подключения к Mongodb и коллекции в нем,
регистрации комманд и handlers бота из других модулей
"""

import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import API_TOKEN, MONGO_URL
from app.handlers.commands import register_commands
from app.handlers.messages import register_messages

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()


client = AsyncIOMotorClient(MONGO_URL)
db = client["salary_db"]
collection = db["salaries"]

# Регистрация хендлеров
router = Router()
register_commands(router)
register_messages(router, collection)  # передаем коллекцию

dp.include_router(router)
