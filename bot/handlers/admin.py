"""
Admin handlerlari
"""

import logging
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..config import GROUP_ID, MESSAGES
from ..states import AdminBroadcast
from ..keyboards import get_admin_menu, get_cancel_keyboard
from ..utils import is_admin, format_broadcast_message, format_reply_message, format_group_reply_message, get_all_users

logger = logging.getLogger(__name__)
router = Router()


async def send_broadcast_to_users(bot: Bot, broadcast_text: str, admin_id: int):
    """Background da barcha foydalanuvchilarga xabar yuborish"""
    all_users = get_all_users()
    success_count = 0
    error_count = 0
    
    # Avval guruhga yuborish
    try:
        await bot.send_message(GROUP_ID, broadcast_text)
        logger.info("Umumiy xabar guruhga yuborildi")
    except Exception as e:
        logger.error(f"Guruhga xabar yuborishda xatolik: {e}")
    
    # Barcha foydalanuvchilarga yuborish
    for user_id in all_users:
        try:
            await bot.send_message(user_id, broadcast_text)
            success_count += 1
            # Har 10 ta xabardan keyin biroz kutish (rate limiting uchun)
            if success_count % 10 == 0:
                await asyncio.sleep(0.5)
        except Exception as e:
            error_count += 1
            logger.error(f"Foydalanuvchi {user_id} ga xabar yuborishda xatolik: {e}")
    
    # Adminga natijani yuborish
    result_message = f"""
✅ <b>Xabar yuborish tugallandi!</b>

📊 <b>Natijalar:</b>
✅ Muvaffaqiyatli: {success_count}
❌ Xatolik: {error_count}
👥 Jami: {len(all_users)}
"""
    
    try:
        await bot.send_message(admin_id, result_message)
        logger.info(f"Natija adminga ({admin_id}) yuborildi")
    except Exception as e:
        logger.error(f"Adminga natija yuborishda xatolik: {e}")


@router.message(F.text == "/send_message", F.chat.type == "private")
async def admin_broadcast_start(message: Message, state: FSMContext):
    """Admin umumiy xabar yuborish - faqat private chatda"""
    if not message.from_user or not is_admin(message.from_user.id):
        await message.answer(MESSAGES["no_permission"])
        return
    
    await state.set_state(AdminBroadcast.waiting_for_message)
    await message.answer(
        "📢 <b>Umumiy xabar yuborish</b>\n\n"
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(AdminBroadcast.waiting_for_message, F.text != "❌ Bekor qilish", F.chat.type == "private")
async def admin_broadcast_send(message: Message, state: FSMContext, bot: Bot):
    """Umumiy xabarni yuborish - backgroundda"""
    if not message.from_user or not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer("❌ Iltimos, matn kiriting!")
        return
    
    broadcast_text = format_broadcast_message(message.text)
    
    # Darhol adminga tasdiqlash xabari yuborish
    await message.answer(
        "⏳ <b>Xabar yuborish boshlandi!</b>\n\n"
        "Barcha foydalanuvchilarga xabar yuborilmoqda...\n"
        "Tugagach natijani yuboraman.",
        reply_markup=get_admin_menu()
    )
    
    # Background taskni yaratish va ishga tushirish
    task = asyncio.create_task(
        send_broadcast_to_users(bot, broadcast_text, message.from_user.id)
    )
    
    # Taskni background da ishlatish (kutmasdan)
    logger.info(f"Background broadcast task yaratildi: {task}")
    
    await state.clear()


@router.callback_query(F.data.startswith("reply_"))
async def handle_reply_callback(callback: CallbackQuery, state: FSMContext):
    """Javob berish callback - barcha foydalanuvchilar uchun alert"""
    try:
        # Callback ma'lumotlarini parsing qilish
        if not callback.data or not callback.message:
            await callback.answer("❌ Noto'g'ri ma'lumot!", show_alert=True)
            return
            
        # Barcha foydalanuvchilar uchun reply qilish ko'rsatmasi
        await callback.answer(
            "💬 Javob berish uchun xabarni reply qiling", 
            show_alert=True
        )
            
    except Exception as e:
        logger.error(f"Callback ishlov berishda xatolik: {e}")
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)


# Guruhda reply orqali javob berish
@router.message(F.chat.type.in_(["group", "supergroup"]), F.reply_to_message)
async def handle_group_reply(message: Message, bot: Bot):
    """Guruhda reply orqali javob berish - barcha guruh a'zolari uchun"""
    if not message.from_user or not message.text:
        return
    
    # Reply qilingan xabar bot tomonidan yuborilganligini va inline keyboard borligini tekshirish
    if (not message.reply_to_message or 
        not message.reply_to_message.from_user or
        not message.reply_to_message.reply_markup):
        return
    
    # Bot yuborgan xabar ekanligini tekshirish
    bot_info = await bot.get_me()
    if message.reply_to_message.from_user.id != bot_info.id:
        return
    
    try:
        # Inline keyboard'dan callback data olish
        inline_keyboard = message.reply_to_message.reply_markup.inline_keyboard
        
        # "reply_" bilan boshlanadigan callback_data ni topish
        target_user_id = None
        for row in inline_keyboard:
            for button in row:
                if button.callback_data and button.callback_data.startswith("reply_"):
                    # callback_data: "reply_{user_id}_{message_id}"
                    parts = button.callback_data.split("_")
                    if len(parts) >= 2:
                        target_user_id = int(parts[1])
                        break
            if target_user_id:
                break
        
        if not target_user_id:
            await message.reply("❌ Foydalanuvchi ID topilmadi!")
            return
        
        # Javob yuboruvchi nomini olish
        sender_name = message.from_user.full_name or f"@{message.from_user.username}" or "Guruh a'zosi"
        
        # Admin ekanligini tekshirib, mos xabar formatini tanlash
        if is_admin(message.from_user.id):
            reply_text = format_reply_message(message.text)
        else:
            reply_text = format_group_reply_message(message.text, sender_name)
        
        await bot.send_message(target_user_id, reply_text)
        
        # Tasdiqlash xabari
        await message.reply("✅ Javob muvaffaqiyatli yuborildi!")
        
    except (ValueError, IndexError, Exception) as e:
        logger.error(f"Guruhda reply orqali javob yuborishda xatolik: {e}")
        await message.reply("❌ Javob yuborishda xatolik yuz berdi!")
