from .fixt import tests_input_data, tests_output_data
from app.handlers.messages import handle_message
from aiogram import types, Bot
import pytest
import json
from unittest.mock import AsyncMock
from app.config import API_TOKEN
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.mark.asyncio
async def test_intput_t2(mocker):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["salary_db"]
    collection = db["salaries"]

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    fake_message = AsyncMock(text=json.dumps(tests_input_data['intput_t2']))
    fake_response = tests_output_data['intput_t2']
    fake_message.reply = AsyncMock(return_value=None)
    await handle_message(fake_message, collection)
    fake_message.reply.assert_called_once_with(json.dumps(fake_response), parse_mode=ParseMode.HTML)


@pytest.mark.asyncio
async def test_intput_t3(mocker):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["salary_db"]
    collection = db["salaries"]

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    fake_message = AsyncMock(text=json.dumps(tests_input_data['intput_t3']))
    fake_response = tests_output_data['intput_t3']
    fake_message.reply = AsyncMock(return_value=None)
    await handle_message(fake_message, collection)
    fake_message.reply.assert_called_once_with(json.dumps(fake_response), parse_mode=ParseMode.HTML)


@pytest.mark.asyncio
async def test_intput_t4(mocker):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["salary_db"]
    collection = db["salaries"]

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    fake_message = AsyncMock(text=json.dumps(tests_input_data['intput_t4']))
    fake_response = tests_output_data['intput_t4']
    fake_message.reply = AsyncMock(return_value=None)
    await handle_message(fake_message, collection)
    fake_message.reply.assert_called_once_with(json.dumps(fake_response), parse_mode=ParseMode.HTML)
