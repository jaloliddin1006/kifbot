"""
Yordamchi funksiyalar
"""

import json
import logging
from typing import Dict, Any
from datetime import datetime

from ..config import ADMIN_ID, DATA_FILE

logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Admin ekanligini tekshirish"""
    return user_id == ADMIN_ID


def save_user_data(user_id: int, data: Dict[str, Any]) -> None:
    """Foydalanuvchi ma'lumotlarini saqlash"""
    try:
        # Fayl mavjudligini tekshirish
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        except FileNotFoundError:
            all_data = {}
        
        # Ma'lumotlarni yangilash
        all_data[str(user_id)] = {
            **data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Faylga saqlash
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Foydalanuvchi {user_id} ma'lumotlari saqlandi")
        
    except Exception as e:
        logger.error(f"Ma'lumotlarni saqlashda xatolik: {e}")


def load_user_data(user_id: int) -> Dict[str, Any]:
    """Foydalanuvchi ma'lumotlarini yuklash"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            return all_data.get(str(user_id), {})
    except FileNotFoundError:
        return {}
    except Exception as e:
        logger.error(f"Ma'lumotlarni yuklashda xatolik: {e}")
        return {}


def format_request_message(data: Dict[str, Any], user_id: int) -> str:
    """Ariza xabarini formatlash"""
    message = f"""
🆕 <b>Yangi ariza/taklif</b>

👤 <b>Talaba:</b> {data.get('full_name', "Noma'lum")}
👥 <b>Guruh:</b> {data.get('group', "Noma'lum")}
📱 <b>Telefon:</b> {data.get('phone_number', "Noma'lum")}
🆔 <b>Telegram ID:</b> {user_id}

💬 <b>Xabar:</b>
{data.get('request_content', 'Rasm yoki fayl yuborilgan')}
"""
    return message


def format_user_preview(data: Dict[str, Any]) -> str:
    """Foydalanuvchi uchun ariza ko'rinishini formatlash"""
    preview = f"""
📋 <b>Ariza/Taklif ko'rinishi:</b>

👤 <b>To'liq ism:</b> {data.get('full_name', '')}
👥 <b>Guruh:</b> {data.get('group', '')}
📱 <b>Telefon:</b> {data.get('phone_number', '')}

💬 <b>Xabar:</b>
{data.get('request_content', 'Rasm yoki fayl yuborilgan')}

Barcha ma'lumotlar to'g'rimi?
"""
    return preview


def format_reply_message(text: str) -> str:
    """Javob xabarini formatlash"""
    return f"""
📩 <b>Dekanatdan javob</b>

{text}

---
<i>Fakultet dekanati</i>
"""


def format_group_reply_message(text: str, sender_name: str) -> str:
    """Guruh a'zosi javob xabarini formatlash"""
    return f"""
📩 <b>Javob</b>

{text}

---
<i>Fakultet dekanati</i>
"""
# <i>Javob beruvchi: {sender_name}</i>


def format_broadcast_message(text: str) -> str:
    """Umumiy xabar formatini yaratish"""
    return f"""
📢 <b>Dekanat xabari</b>

{text}

---
<i>Bu xabar fakultet dekanati tomonidan yuborilgan</i>
"""


def get_all_users() -> list:
    """Barcha foydalanuvchilar ID larini olish"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            return [int(user_id) for user_id in all_data.keys()]
    except FileNotFoundError:
        return []
    except Exception as e:
        logger.error(f"Foydalanuvchilar ma'lumotlarini yuklashda xatolik: {e}")
        return []
