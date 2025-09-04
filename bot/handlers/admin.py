"""
Admin handlerlari
"""

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..config import GROUP_ID, MESSAGES
from ..states import AdminBroadcast, ReplyToUser
from ..keyboards import get_admin_menu, get_cancel_keyboard
from ..utils import is_admin, format_broadcast_message, format_reply_message

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "/send_message")
async def admin_broadcast_start(message: Message, state: FSMContext):
    """Admin umumiy xabar yuborish"""
    if not message.from_user or not is_admin(message.from_user.id):
        await message.answer(MESSAGES["no_permission"])
        return
    
    await state.set_state(AdminBroadcast.waiting_for_message)
    await message.answer(
        "📢 <b>Umumiy xabar yuborish</b>\n\n"
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(AdminBroadcast.waiting_for_message, F.text != "❌ Bekor qilish")
async def admin_broadcast_send(message: Message, state: FSMContext, bot: Bot):
    """Umumiy xabarni yuborish"""
    if not message.from_user or not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer("❌ Iltimos, matn kiriting!")
        return
    
    broadcast_text = format_broadcast_message(message.text)
    
    # Bu yerda barcha foydalanuvchilarga xabar yuborish logikasi bo'lishi kerak
    # Hozirda faqat guruhga yuboramiz
    try:
        await bot.send_message(GROUP_ID, broadcast_text)
        await message.answer(
            "✅ Xabar muvaffaqiyatli yuborildi!",
            reply_markup=get_admin_menu()
        )
    except Exception as e:
        logger.error(f"Umumiy xabar yuborishda xatolik: {e}")
        await message.answer(
            "❌ Xabar yuborishda xatolik yuz berdi!",
            reply_markup=get_admin_menu()
        )
    
    await state.clear()


@router.callback_query(F.data.startswith("reply_"))
async def handle_reply_callback(callback: CallbackQuery, state: FSMContext):
    """Javob berish callback"""
    try:
        # Callback ma'lumotlarini parsing qilish
        if not callback.data or not callback.message:
            await callback.answer("❌ Noto'g'ri ma'lumot!", show_alert=True)
            return
            
        parts = callback.data.split("_")
        if len(parts) >= 3:
            chat_id = int(parts[1])
            message_id = int(parts[2])
            
            await state.update_data(reply_chat_id=chat_id, reply_message_id=message_id)
            await state.set_state(ReplyToUser.waiting_for_reply)
            
            await callback.message.answer(
                "💬 <b>Javob yozish</b>\n\n"
                "Talabaga yubormoqchi bo'lgan javobingizni yozing:",
                reply_markup=get_cancel_keyboard()
            )
            
            await callback.answer()
        else:
            await callback.answer("❌ Noto'g'ri ma'lumot!", show_alert=True)
            
    except Exception as e:
        logger.error(f"Callback ishlov berishda xatolik: {e}")
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)


@router.message(ReplyToUser.waiting_for_reply, F.text != "❌ Bekor qilish")
async def send_reply_to_user(message: Message, state: FSMContext, bot: Bot):
    """Foydalanuvchiga javob yuborish"""
    if not message.from_user or not message.text:
        return
        
    data = await state.get_data()
    chat_id = data.get('reply_chat_id')
    
    if not chat_id:
        await message.answer("❌ Xatolik: Chat ID topilmadi!")
        await state.clear()
        return
    
    reply_text = format_reply_message(message.text)
    
    try:
        await bot.send_message(chat_id, reply_text)
        
        keyboard = get_admin_menu() if is_admin(message.from_user.id) else None
        await message.answer("✅ Javob muvaffaqiyatli yuborildi!", reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Javob yuborishda xatolik: {e}")
        
        keyboard = get_admin_menu() if is_admin(message.from_user.id) else None
        await message.answer("❌ Javob yuborishda xatolik yuz berdi!", reply_markup=keyboard)
    
    await state.clear()
