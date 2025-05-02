import asyncio
import logging
import sys
from bot import dp, bot, set_default_commands
from handlers import edit


async def main():
    await set_default_commands(bot)
    dp.include_router(edit.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
