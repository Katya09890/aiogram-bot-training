import os
import ssl
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from config import TOKEN

# ОТКЛЮЧАЕМ ПРОВЕРКУ SSL
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

session = AiohttpSession(connector=aiohttp.TCPConnector(ssl=ssl_context))

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session
)

dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    await message.answer("Бот работает!")

async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
