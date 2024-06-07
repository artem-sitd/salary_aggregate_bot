from aiogram import Router, types
from aiogram.filters import Command


async def start_command(message: types.Message):
    await message.reply("Hello! I'm your bot.")


async def help_command(message: types.Message):
    await message.reply("Send me a JSON payload to aggregate salary data.")


def register_commands(router: Router):
    router.message.register(start_command, Command(commands=["start"]))
    router.message.register(help_command, Command(commands=["help"]))
