"""
Bot konfiguratsiya sozlamalari
"""

import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Rate limiting sozlamalari
RATE_LIMIT_REQUESTS = 30  # So'rovlar soni
RATE_LIMIT_PERIOD = 60   # Sekundlarda

# Logging sozlamalari
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Ma'lumotlar fayli
DATA_FILE = "user_data.json"

# Xabar matnlari
MESSAGES = {
    "welcome": """
🎓 <b>Fakultet Dekanati Botiga Xush Kelibsiz!</b>

Salom, {name}! 

Bu bot orqali siz:
• 📝 Ariza va takliflar yuborishingiz
• ℹ️ Dekanat va fakultet haqida ma'lumot olishingiz mumkin

Quyidagi tugmalardan foydalaning:
""",
    
    "rate_limit": "🚫 Juda ko'p so'rov yuborildi. Iltimos, bir oz kuting.",
    
    "no_permission": "❌ Sizda bu amalni bajarish uchun ruxsat yo'q!",
    
    "operation_cancelled": "❌ Operatsiya bekor qilindi.",
    
    "request_sent": """
✅ <b>Arizangiz muvaffaqiyatli yuborildi!</b>

Javob tez orada beriladi. Rahmat!
""",
    
    "error_occurred": "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
    
    "unknown_command": "❓ Tushunmadim. Iltimos, menyudan foydalaning."
}

# Fakultet ma'lumotlari
FACULTY_INFO = {
    "dekanat": """
🏛️ <b>Kompyuter injiniringi fakulteti dekanati</b>

📍 <b>Manzil:</b> TATU F binosi, 3-qavat

👨‍💼 <b>Dekan:</b> Kuchkorov Temurbek Ataxonovich
⏰ <b>Qabul vaqti:</b> Har kuni 14:00-16:00 (dushanba va shanbadan tashqari)
📞 <b>Telefon:</b> (+99871) 207-59-45
📧 <b>Email:</b> t.kuchkorov@tuit.uz

👨‍💼 <b>Yoshlar bilan ishlash bo'yicha dekan muovini:</b>
Karimov Abdulatif Botirovich
⏰ <b>Qabul vaqti:</b> Har kuni 14:00-17:00
📞 <b>Telefon:</b> (+99871) 207-59-46
📧 <b>Email:</b> abdulatifkarimoff@gmail.com

👨‍💼 <b>O'quv ishlari bo'yicha dekan muovinlari:</b>

📋 Husanov Sherzod Abdimanonovich
⏰ Qabul vaqti: Har kuni 14:00-17:00
📞 Telefon: (+99871) 207-59-46
📧 Email: sh.khusanov@tuit.uz

📋 G'ulomov Doniyor Zaynobidin o'g'li
⏰ Qabul vaqti: Har kuni 14:00-17:00
📞 Telefon: (+99871) 207-59-46
📧 Email: d.gulomov@tuit.uz

📋 Karimov Sardor Atxam o'g'li
⏰ Qabul vaqti: Har kuni 14:00-17:00
📞 Telefon: (+99871) 207-59-46
📧 Email: s.karimov@tuit.uz
""",

    "fakultet": """
🎓 <b>Kompyuter injiniringi fakulteti</b>

Fakultet 2013 yil 26 martdagi O'zbekiston Respublikasi Prezidentining №PQ-1942 "Axborot-kommunikatsiya texnologiyalari sohasida kadrlar tayyorlash tizimini yanada takomillashtirish chora-tadbirlari to'g'risida"gi Qarori asosida "Axborot texnologiyalari" fakulteti negizida tashkil topgan.

📋 <b>Kafedralar:</b>
• � Raqamli texnologiyalar konvergensiyasi
• 💻 Informatika asoslari
• 🤖 Sun'iy intellekt kafedrasi
• 🖥️ Kompyuter tizimlari
• 🎬 Multimedia texnologiyalari

🎓 <b>BAKALAVRIATURA YO'NALISHLARI:</b>

• 60610500 - Kompyuter injiniringi
  ▪️ Kompyuter injiniringi
  ▪️ AT-servisi
  ▪️ Multimedia texnologiyalari

• 60610700 - Sun'iy intellekt

• 60711500 - Mexatronika va robototexnika

• 60611400 - Pochta aloqasi texnologiyasi

🎓 <b>MAGISTRATURA YO'NALISHLARI:</b>

• 70610501 - Kompyuter injiniringi
  ▪️ Kompyuter tizimlarini loyihalash
  ▪️ Amaliy dasturiy vositalarini loyihalash
  ▪️ Axborot va multimedia texnologiyalari

• 70610502 - Elektron hukumat tizimini boshqarish
• 70610503 - Tibbiyotda kompyuter tizimlari
• 70610504 - Ma'lumotlar ilmi (Data Science)
• 70610505 - Internet ashyolari
• 70610205 - Geoaxborot tizimlari va texnologiyalari
• 70611401 - Pochta xizmatini tashkil etish va texnologiyasi
• 70610701 - Sun'iy intellekt
• 70611702 - Intellektual axborot-kommunikatsiya tizimlari

""",

    "contact": """
📞 <b>Bog'lanish ma'lumotlari</b>

🏛️ <b>Fakultet dekanati:</b>
📞 (+99871) 207-59-45
📧 t.kuchkorov@tuit.uz

👨‍💼 <b>Dekan qabulxonasi:</b>
📞 (+99871) 207-59-45
⏰ Har kuni 14:00-16:00 (dushanba va shanbadan tashqari)

📚 <b>O'quv ishlari bo'yicha muovinlar:</b>
📞 (+99871) 207-59-46
📧 sh.khusanov@tuit.uz
📧 d.gulomov@tuit.uz
📧 s.karimov@tuit.uz

🎓 <b>Yoshlar bilan ishlash bo'limi:</b>
📞 (+99871) 207-59-46
📧 abdulatifkarimoff@gmail.com
⏰ Har kuni 14:00-17:00

📍 <b>Manzil:</b>
TATU F binosi
Kompyuter injiniringi fakulteti
3-qavat

"""
}
