"""
Данный модуль был для тестирования тестов :)) в части использования фикстур,
но от этой затеи отказался, модуль будет удален позже
"""
# import pytest
# from fastapi.testclient import TestClient
# from motor.motor_asyncio import AsyncIOMotorClient
# from app.main import app
#
# client = TestClient(app)
#
#
# @pytest.fixture(scope="module")
# async def collection():
#     test_client = AsyncIOMotorClient("mongodb://localhost:27017")
#     test_db = test_client["salary_db"]
#     test_collection = test_db["salaries"]
#     return test_collection
