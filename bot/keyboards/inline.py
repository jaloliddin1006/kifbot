"""
Inline klaviaturalar
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_reply_keyboard(chat_id: int, message_id: int) -> InlineKeyboardMarkup:
    """Javob berish inline klaviaturasi"""
    callback_data = f"reply_{chat_id}_{message_id}"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Javob berish", callback_data=callback_data)]
        ]
    )
    return keyboard


def get_start_menu() -> InlineKeyboardMarkup:
    """Start menyusi inline klaviaturasi"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Ariza yozish", callback_data="write_request")],
            [InlineKeyboardButton(text="ℹ️ Dekanat haqida", callback_data="about_faculty")],
            [InlineKeyboardButton(text="📚 Fakultet haqida", callback_data="about_department")]
        ]
    )
    return keyboard
