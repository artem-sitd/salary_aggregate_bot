import json
import sys
from datetime import datetime
from aiogram import Router, types
from aiogram.enums import ParseMode
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "***** %(asctime)s  [%(levelname)s] %(name)s: -> %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# logger.info("API is starting up")


async def handle_message(message: types.Message, collection):
    try:
        data = json.loads(message.text)
        dt_from = datetime.fromisoformat(data["dt_from"])
        dt_upto = datetime.fromisoformat(data["dt_upto"])
        group_type = data["group_type"]

        result = await aggregate_data(collection, dt_from, dt_upto, group_type)

        # проверка что отдает
        # for i in result:
        #     logger.info(str(i))

        dataset = [item["total"] for item in result]
        labels = [item["date_label"] for item in result]

        response = {"dataset": dataset, "labels": labels}

        await message.reply(json.dumps(response), parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(e)
        await message.reply(f"Error: {str(e)}")


async def aggregate_data(collection, dt_from, dt_upto, group_type):
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
