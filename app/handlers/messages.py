import json
import logging
import sys
from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.enums import ParseMode

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "***** %(asctime)s  [%(levelname)s] %(name)s: -> %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


async def handle_message(message: types.Message, collection):
    """
    Функция для приема сообщения от пользователя, форматирования даты,
    отправки/получения итоговых значений от зависимых функций,
    и отправки пользователю сгенерированной выборки из базы
    """
    try:
        data = json.loads(message.text)
        dt_from = datetime.fromisoformat(data["dt_from"])
        dt_upto = datetime.fromisoformat(data["dt_upto"])
        group_type = data["group_type"]

        result = await aggregate_data(collection, dt_from, dt_upto, group_type)

        dataset, labels = process_result(result, dt_from, dt_upto, group_type)

        response = {"dataset": dataset, "labels": labels}

        await message.answer(json.dumps(response), parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.answer(f"Error: {str(e)}")


def generate_time_labels(dt_from, dt_upto, group_type):
    """
    Эта функция генерирует метки времени для заданного диапазона дат,
    основываясь на типе группировки (час, день, месяц).
    """
    labels = []
    current = dt_from

    while current <= dt_upto:
        labels.append(current.isoformat())
        if group_type == "hour":
            current += timedelta(hours=1)
        elif group_type == "day":
            current += timedelta(days=1)
        elif group_type == "month":
            next_month = current.month % 12 + 1
            next_year = current.year + (current.month // 12)
            current = current.replace(month=next_month, year=next_year)

    return labels


def process_result(result, dt_from, dt_upto, group_type):
    """
    Эта функция обрабатывает результаты агрегации, чтобы заполнить
    отсутствующие временные метки нулевыми значениями и вернуть обновленные
    dataset и labels. Используем date_label, сгенерированный в pipeline,
     как ключ для сопоставления.
    """
    labels = generate_time_labels(dt_from, dt_upto, group_type)
    result_dict = {item["date_label"]: item["total"] for item in result}

    dataset = [result_dict.get(label, 0) for label in labels]

    return dataset, labels


async def aggregate_data(collection, dt_from, dt_upto, group_type):
    """
    Функция для выполнения агрегации MongoDB с заданным pipeline.
    Она использует рабочий pipeline для выборки данных. Очень большой получился запрос,
    сгенерирован chat-gpt, я его не до конца понимаю :))
    """
    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$dt"},
                    "month": {
                        "$cond": [
                            {"$in": [group_type, ["month", "day", "hour"]]},
                            {"$month": "$dt"},
                            None,
                        ]
                    },
                    "day": {
                        "$cond": [
                            {"$in": [group_type, ["day", "hour"]]},
                            {"$dayOfMonth": "$dt"},
                            None,
                        ]
                    },
                    "hour": {
                        "$cond": [{"$eq": [group_type, "hour"]}, {"$hour": "$dt"}, None]
                    },
                },
                "total": {"$sum": "$value"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}},
        {
            "$project": {
                "_id": 0,
                "total": 1,
                "date_label": {
                    "$dateToString": {
                        "format": "%Y-%m-%dT%H:%M:%S",
                        "date": {
                            "$dateFromParts": {
                                "year": "$_id.year",
                                "month": {"$ifNull": ["$_id.month", 1]},
                                "day": {"$ifNull": ["$_id.day", 1]},
                                "hour": {"$ifNull": ["$_id.hour", 0]},
                                "minute": 0,
                                "second": 0,
                            }
                        },
                    }
                },
            }
        },
    ]

    result = []
    async for doc in collection.aggregate(pipeline):
        result.append(doc)
    return result


def register_messages(router: Router, collection):
    async def handler(message: types.Message):
        await handle_message(message, collection)

    router.message.register(handler)
