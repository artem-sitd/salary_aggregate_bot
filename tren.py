from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["salary_db"]
collection = db["salaries"]


async def get_aggregate(dt_from, dt_upto):
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)

    # pipeline = [{"$find": {"dt": {"$gte": dt_from, "$lte": dt_upto}}}]
    pipeline = [{"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}}]
    result = []
    async for doc in collection.aggregate(pipeline):
        result.append(doc)
    return result


print(asyncio.run(get_aggregate("2022-02-01T00:00:00", "2022-02-02T00:00:00")))
