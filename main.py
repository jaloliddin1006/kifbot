"""
Telegram Bot asosiy fayli
Universitet fakulteti dekanati uchun bot
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN, LOG_LEVEL, LOG_FORMAT
from bot.handlers import routers
from bot.middlewares import ThrottlingMiddleware


async def main():
    """Asosiy funksiya"""
    # Logging sozlash
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler('bot.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    # Token tekshirish
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN o'rnatilmagan!")
        return
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Middleware qo'shish
    dp.message.middleware(ThrottlingMiddleware())
    
    # Routerlarni ro'yxatdan o'tkazish
    for router in routers:
        dp.include_router(router)
    
    logger.info("Bot ishga tushmoqda...")
    
    try:
        # Bot ma'lumotlarini olish
        bot_info = await bot.get_me()
        logger.info(f"Bot ishga tushdi: @{bot_info.username}")
        
        # Dispatcherni ishga tushirish
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot to'xtatildi")
    except Exception as e:
        logging.error(f"Umumiy xatolik: {e}")
