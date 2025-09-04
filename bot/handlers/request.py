"""
Ariza yuborish handlerlari
"""

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..config import GROUP_ID, MESSAGES
from ..states import RequestForm
from ..keyboards import (
    get_cancel_keyboard, get_contact_keyboard,
    get_confirmation_keyboard, get_main_menu, get_admin_menu,
    get_reply_keyboard
)
from ..utils import (
    is_admin, save_user_data,
    format_request_message, format_user_preview
)

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "📝 Ariza/Taklif yuborish", F.chat.type == "private")
async def start_request(message: Message, state: FSMContext):
    """Ariza yozishni boshlash - faqat private chatda"""
    if not message.from_user:
        return
        
    await state.set_state(RequestForm.waiting_for_name)
    await message.answer(
        "📝 <b>Ariza/Taklif yuborish</b>\n\n"
        "Iltimos, to'liq ismingizni kiriting:\n"
        "<i>Masalan: Abdullayev Dilshod Azamat o'g'li</i>",
        reply_markup=get_cancel_keyboard()
    )


@router.message(RequestForm.waiting_for_name, F.text != "❌ Bekor qilish", F.chat.type == "private")
async def process_name(message: Message, state: FSMContext):
    """Ism qabul qilish"""
    if not message.text:
        await message.answer("❌ Iltimos, matn kiriting!")
        return
    
    full_name = message.text.strip()
    
    if len(full_name) < 3:
        await message.answer("❌ Iltimos, to'liq ismingizni kiriting!")
        return
    
    await state.update_data(full_name=full_name)
    await state.set_state(RequestForm.waiting_for_group)
    
    await message.answer(
        "👥 <b>Guruh nomini kiriting:</b>\n"
        "<i>Masalan: 21-guruh, IT-22, Matematika-23</i>",
        reply_markup=get_cancel_keyboard()
    )


@router.message(RequestForm.waiting_for_group, F.text != "❌ Bekor qilish", F.chat.type == "private")
async def process_group(message: Message, state: FSMContext):
    """Guruh qabul qilish"""
    if not message.text:
        await message.answer("❌ Iltimos, matn kiriting!")
        return
    
    group = message.text.strip()
    
    if len(group) < 2:
        await message.answer("❌ Iltimos, guruh nomini to'g'ri kiriting!")
        return
    
    await state.update_data(group=group)
    await state.set_state(RequestForm.waiting_for_contact)
    
    await message.answer(
        "📱 <b>Telefon raqamingizni ulashing:</b>\n"
        "Quyidagi tugma orqali telefon raqamingizni yuboring:",
        reply_markup=get_contact_keyboard()
    )


@router.message(RequestForm.waiting_for_contact, F.contact, F.chat.type == "private")
async def process_contact(message: Message, state: FSMContext):
    """Kontakt qabul qilish"""
    if not message.contact or not message.from_user:
        await message.answer("❌ Kontakt ma'lumotlarida xatolik!")
        return
    
    contact = message.contact
    
    if contact.user_id != message.from_user.id:
        await message.answer("❌ Iltimos, o'zingizning telefon raqamingizni yuboring!")
        return
    
    await state.update_data(
        phone_number=contact.phone_number,
        contact_user_id=contact.user_id
    )
    await state.set_state(RequestForm.waiting_for_message)
    
    await message.answer(
        "✍️ <b>Ariza/Taklif matnini yozing:</b>\n\n"
        "Siz matn, rasm yoki fayllar yuborishingiz mumkin.\n"
        "Tugatgach, \"Tasdiqlash\" tugmasini bosing:",
        reply_markup=get_confirmation_keyboard()
    )


@router.message(RequestForm.waiting_for_message, F.text == "✅ Tasdiqlash", F.chat.type == "private")
async def confirm_request(message: Message, state: FSMContext):
    """Arizani tasdiqlash"""
    data = await state.get_data()
    
    if 'request_content' not in data and 'photos' not in data and 'documents' not in data:
        await message.answer("❌ Iltimos, avval ariza matnini yozing yoki fayl yuboring!")
        return
    
    await state.set_state(RequestForm.confirming)
    
    # Ma'lumotlarni ko'rsatish
    preview_text = format_user_preview(data)
    await message.answer(preview_text, reply_markup=get_confirmation_keyboard())


@router.message(RequestForm.waiting_for_message, ~F.text.in_(["✅ Tasdiqlash", "❌ Bekor qilish"]), F.chat.type == "private")
async def process_request_content(message: Message, state: FSMContext):
    """Ariza matnini qabul qilish"""
    data = await state.get_data()
    
    if message.text:
        content = data.get('request_content', '') + message.text + '\n'
        await state.update_data(request_content=content)
        await message.answer("✅ Matn qabul qilindi. Davom eting yoki \"Tasdiqlash\" tugmasini bosing.")
    
    elif message.photo:
        # Rasmlarni saqlash
        photos = data.get('photos', [])
        photos.append(message.photo[-1].file_id)
        await state.update_data(photos=photos)
        await message.answer("📸 Rasm qabul qilindi. Davom eting yoki \"Tasdiqlash\" tugmasini bosing.")
    
    elif message.document:
        # Fayllarni saqlash
        documents = data.get('documents', [])
        documents.append({
            'file_id': message.document.file_id,
            'file_name': message.document.file_name
        })
        await state.update_data(documents=documents)
        await message.answer("📎 Fayl qabul qilindi. Davom eting yoki \"Tasdiqlash\" tugmasini bosing.")


@router.message(RequestForm.confirming, F.text == "✅ Tasdiqlash", F.chat.type == "private")
async def send_request_to_group(message: Message, state: FSMContext, bot: Bot):
    """Arizani guruhga yuborish"""
    if not message.from_user:
        return
        
    data = await state.get_data()
    user_id = message.from_user.id
    
    # Guruhga yuborish uchun xabar tayyorlash
    group_message = format_request_message(data, user_id)
    
    try:
        # Asosiy xabarni yuborish
        sent_message = await bot.send_message(
            GROUP_ID,
            group_message,
            reply_markup=get_reply_keyboard(user_id, message.message_id)
        )
        
        # Rasmlarni yuborish
        if 'photos' in data:
            for photo_id in data['photos']:
                await bot.send_photo(GROUP_ID, photo_id)
        
        # Fayllarni yuborish
        if 'documents' in data:
            for doc in data['documents']:
                await bot.send_document(GROUP_ID, doc['file_id'])
        
        # Foydalanuvchi ma'lumotlarini saqlash
        save_user_data(user_id, data)
        
        # Muvaffaqiyat xabari
        keyboard = get_main_menu() if not is_admin(user_id) else get_admin_menu()
        await message.answer(MESSAGES["request_sent"], reply_markup=keyboard)
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Guruhga xabar yuborishda xatolik: {e}")
        keyboard = get_main_menu() if not is_admin(user_id) else get_admin_menu()
        await message.answer(MESSAGES["error_occurred"], reply_markup=keyboard)

