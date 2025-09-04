# Fakultet Dekanati Telegram Bot

Universitet fakulteti dekanati uchun Telegram bot. Talabalar ariza va takliflar yuborishi, admin esa javob berishi uchun mo'ljallangan.

## Xususiyatlar

### Talabalar uchun:
- 📝 Ariza va takliflar yuborish
- 👤 Shaxsiy ma'lumotlarni kiritish (ism, guruh, telefon)
- 📱 Kontakt yuborish (majburiy)
- 🖼️ Matn va rasm yuborish imkoniyati
- ✅ Xabarni tasdiqlash tizimi

### Adminlar uchun:
- 💬 Talabalar arizalariga javob berish
- 📢 Umumiy xabar yuborish
- 🔧 Barcha talaba funksiyalaridan foydalanish

### Xavfsizlik:
- 🚫 Rate limiting (spam himoyasi)
- 🔒 Admin huquqlarini tekshirish
- ⚡ Xatoliklarni boshqarish

## O'rnatish

1. Repository ni klonlash:
```bash
git clone <repository-url>
cd kifbot
```

2. Virtual muhit yaratish:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

4. `.env` faylini sozlash:
```env
BOT_TOKEN=your_bot_token_here
GROUP_ID=your_group_id_here  
ADMIN_ID=your_admin_id_here
RATE_LIMIT_REQUESTS=20
RATE_LIMIT_PERIOD=60
```

## Sozlash

### Bot Token olish:
1. Telegram'da @BotFather ga yozing
2. `/newbot` komandasi bering
3. Bot nomini kiriting
4. Username kiriting
5. Tokenni nusxalang

### Group ID topish:
1. Botni guruhga qo'shing
2. Guruhda biror xabar yozing
3. `https://api.telegram.org/bot<TOKEN>/getUpdates` ga kiring
4. `chat.id` ni topib oling

### Admin ID topish:
1. @userinfobot ga `/start` yozing
2. User ID ni oling

## Ishga tushirish

```bash
python main.py
```

## Fayl tuzilishi

```
kifbot/
├── main.py              # Asosiy bot fayli
├── .env                 # Konfiguratsiya (git ignored)
├── requirements.txt     # Python kutubxonalar
└── README.md           # Loyiha haqida ma'lumot
```

## Bot komandalar

- `/start` - Botni ishga tushirish
- `📝 Ariza/Taklif yuborish` - Yangi ariza yaratish
- `ℹ️ Dekanat haqida` - Dekanat ma'lumotlari
- `🏛️ Fakultet haqida` - Fakultet ma'lumotlari
- `📞 Bog'lanish` - Kontakt ma'lumotlari

## Admin funksiyalar

- `📢 Umumiy xabar yuborish` - Barcha foydalanuvchilarga xabar
- `💬 Javob berish` - Talaba arizasiga javob (inline button)

## Texnik ma'lumotlar

- **Framework:** aiogram 3.x
- **Python:** 3.8+
- **Databaza:** Hozircha faqat memory storage
- **Rate limiting:** 20 so'rov/daqiqa

## Kelajakdagi rivojlanish

- [ ] SQLite/PostgreSQL databaza qo'shish
- [ ] Foydalanuvchilar statistikasi
- [ ] Ariza statuslarini kuzatish
- [ ] Fayllar yuklash imkoniyati
- [ ] Kategoriyalar bo'yicha ajratish
- [ ] Xabarlar arxivi

## Yordam

Agar savollaringiz bo'lsa yoki xatolik topsangiz, GitHub Issues bo'limiga yozing.
