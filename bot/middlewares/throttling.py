"""
Rate limiting middleware
"""

import asyncio
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime, timedelta

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from ..config import RATE_LIMIT_REQUESTS, RATE_LIMIT_PERIOD, MESSAGES


class ThrottlingMiddleware(BaseMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self):
        self.user_requests: Dict[int, list] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat Message turini tekshirish
        if not isinstance(event, Message):
            return await handler(event, data)
        
        # from_user mavjudligini tekshirish
        if not event.from_user:
            return await handler(event, data)
            
        user_id = event.from_user.id
        current_time = datetime.now()
        
        # Foydalanuvchi so'rovlarini kuzatish
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []
        
        # Eski so'rovlarni tozalash
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if current_time - req_time < timedelta(seconds=RATE_LIMIT_PERIOD)
        ]
        
        # Rate limit tekshirish
        if len(self.user_requests[user_id]) >= RATE_LIMIT_REQUESTS:
            await event.answer(MESSAGES["rate_limit"])
            return
        
        # So'rovni ro'yxatga qo'shish
        self.user_requests[user_id].append(current_time)
        
        # Handlerni davom ettirish
        return await handler(event, data)
