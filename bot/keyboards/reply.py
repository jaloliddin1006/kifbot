"""
Reply klaviaturalar
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ariza/Taklif yuborish")],
            [KeyboardButton(text="ℹ️ Dekanat haqida"), KeyboardButton(text="🏛️ Fakultet haqida")],
            [KeyboardButton(text="📞 Bog'lanish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_admin_menu() -> ReplyKeyboardMarkup:
    """Admin menyu klaviaturasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ariza/Taklif yuborish")],
            [KeyboardButton(text="ℹ️ Dekanat haqida"), KeyboardButton(text="🏛️ Fakultet haqida")],
            [KeyboardButton(text="📞 Bog'lanish")],
            [KeyboardButton(text="/send_message")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """Kontakt so'rash klaviaturasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamini yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_confirmation_keyboard() -> ReplyKeyboardMarkup:
    """Tasdiqlash klaviaturasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Tasdiqlash"), KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Bekor qilish klaviaturasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
