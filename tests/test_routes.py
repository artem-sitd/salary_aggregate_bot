"""
Модуль с самими тестами для трех случаев из fixt.py. Используется реальная база (не тестовая).
Операции с базой только чтение. Имитация объекта Message телеграмма для функции handle_message.
Бот также настоящий (не моковый)
"""

import json
from unittest.mock import AsyncMock

import pytest
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import API_TOKEN
from app.handlers.messages import handle_message

from .fixt import tests_input_data, tests_output_data


@pytest.mark.asyncio
async def test_intput_t2(mocker):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["salary_db"]
    collection = db["salaries"]

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    fake_message = AsyncMock(text=json.dumps(tests_input_data["intput_t2"]))
    fake_response = tests_output_data["intput_t2"]
    fake_message.answer = AsyncMock(return_value=None)
    await handle_message(fake_message, collection)
    fake_message.answer.assert_called_once_with(
        json.dumps(fake_response), parse_mode=ParseMode.HTML
    )


@pytest.mark.asyncio
async def test_intput_t3(mocker):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["salary_db"]
    collection = db["salaries"]

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    fake_message = AsyncMock(text=json.dumps(tests_input_data["intput_t3"]))
    fake_response = tests_output_data["intput_t3"]
    fake_message.answer = AsyncMock(return_value=None)
    await handle_message(fake_message, collection)
    fake_message.answer.assert_called_once_with(
        json.dumps(fake_response), parse_mode=ParseMode.HTML
    )


@pytest.mark.asyncio
async def test_intput_t4(mocker):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["salary_db"]
    collection = db["salaries"]

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    fake_message = AsyncMock(text=json.dumps(tests_input_data["intput_t4"]))
    fake_response = tests_output_data["intput_t4"]
    fake_message.answer = AsyncMock(return_value=None)
    await handle_message(fake_message, collection)
    fake_message.answer.assert_called_once_with(
        json.dumps(fake_response), parse_mode=ParseMode.HTML
    )
