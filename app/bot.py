import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import API_TOKEN
from app.handlers.commands import register_commands
from app.handlers.messages import register_messages

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["salary_db"]
collection = db["salaries"]

# Регистрация хендлеров
router = Router()
register_commands(router)
register_messages(router, collection)  # передаем коллекцию

dp.include_router(router)