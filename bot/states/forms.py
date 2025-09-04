"""
FSM States - Forma holatlari
"""

from aiogram.fsm.state import State, StatesGroup


class RequestForm(StatesGroup):
    """Ariza yuborish formasi holatlari"""
    waiting_for_name = State()
    waiting_for_group = State()
    waiting_for_contact = State()
    waiting_for_message = State()
    confirming = State()


class AdminBroadcast(StatesGroup):
    """Admin umumiy xabar yuborish holatlari"""
    waiting_for_message = State()


class ReplyToUser(StatesGroup):
    """Foydalanuvchiga javob berish holatlari"""
    waiting_for_reply = State()
