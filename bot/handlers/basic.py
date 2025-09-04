"""
Asosiy handlerlar
"""

import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..config import MESSAGES, FACULTY_INFO
from ..keyboards import get_main_menu, get_admin_menu
from ..utils import is_admin

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def cmd_start(message: Message, state: FSMContext):
    """Start komandasi - faqat private chatda"""
    await state.clear()
    
    if not message.from_user:
        return
    
    user_name = message.from_user.full_name or "Foydalanuvchi"
    welcome_text = MESSAGES["welcome"].format(name=user_name)
    
    if is_admin(message.from_user.id):
        await message.answer(welcome_text, reply_markup=get_admin_menu())
    else:
        await message.answer(welcome_text, reply_markup=get_main_menu())


@router.message(F.text == "ℹ️ Dekanat haqida", F.chat.type == "private")
async def about_dean_office(message: Message):
    """Dekanat haqida ma'lumot - faqat private chatda"""
    await message.answer(FACULTY_INFO["dekanat"])


@router.message(F.text == "🏛️ Fakultet haqida", F.chat.type == "private")
async def about_faculty(message: Message):
    """Fakultet haqida ma'lumot - faqat private chatda"""
    await message.answer(FACULTY_INFO["fakultet"])


@router.message(F.text == "📞 Bog'lanish", F.chat.type == "private")
async def contact_info(message: Message):
    """Bog'lanish ma'lumotlari - faqat private chatda"""
    await message.answer(FACULTY_INFO["contact"])


@router.message(F.text == "❌ Bekor qilish", F.chat.type == "private")
async def cancel_operation(message: Message, state: FSMContext):
    """Operatsiyani bekor qilish - faqat private chatda"""
    await state.clear()
    
    if not message.from_user:
        return
    
    if is_admin(message.from_user.id):
        keyboard = get_admin_menu()
    else:
        keyboard = get_main_menu()
    
    await message.answer(MESSAGES["operation_cancelled"], reply_markup=keyboard)


@router.message(F.chat.type == "private")
async def handle_unknown_message(message: Message):
    """Noma'lum xabarlarni qayta ishlash - faqat private chatda"""
    if not message.from_user:
        return
        
    if is_admin(message.from_user.id):
        keyboard = get_admin_menu()
    else:
        keyboard = get_main_menu()
    
    await message.answer(MESSAGES["unknown_command"], reply_markup=keyboard)
