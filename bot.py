from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from aiogram.types import BotCommand

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni boshlash"),
        BotCommand(command="edit", description="AI yordamida rasm o'zgartirish"),
        BotCommand(command="help", description="Yordam / Kontakt"),
        BotCommand(command="stats", description="📊 Statistika (faqat admin)"),
    ]
    await bot.set_my_commands(commands)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
