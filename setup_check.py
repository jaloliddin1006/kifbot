# Bot test uchun ishga tushirish
# Avval .env faylini to'ldiring:

# 1. Telegram Bot Token olish:
#    - @BotFather ga yozing
#    - /newbot komandasi bering  
#    - Bot nomini va username kiriting
#    - Tokenni .env fayliga qo'ying

# 2. Group ID topish:
#    - Botni guruhga admin qilib qo'shing
#    - Guruhda /start yozing
#    - https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates ga kiring
#    - chat.id ni topib .env ga qo'ying

# 3. Admin ID topish:
#    - @userinfobot ga /start yozing
#    - User ID ni .env ga qo'ying

# Keyin botni ishga tushiring:
# python main.py

print("Bot sozlash yo'riqnomasi:")
print("1. .env faylini to'ldiring")
print("2. python main.py bilan ishga tushiring")
print("3. Telegram'da /start yozing")

import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
group_id = os.getenv('GROUP_ID')  
admin_id = os.getenv('ADMIN_ID')

print(f"\nHozirgi sozlamalar:")
print(f"BOT_TOKEN: {'✅ O\'rnatilgan' if bot_token and bot_token != 'your_bot_token_here' else '❌ O\'rnatilmagan'}")
print(f"GROUP_ID: {'✅ O\'rnatilgan' if group_id and group_id != 'your_group_id_here' else '❌ O\'rnatilmagan'}")
print(f"ADMIN_ID: {'✅ O\'rnatilgan' if admin_id and admin_id != 'your_admin_id_here' else '❌ O\'rnatilmagan'}")

if not bot_token or bot_token == 'your_bot_token_here':
    print("\n⚠️ .env faylida BOT_TOKEN ni o'rnating!")
else:
    print("\n✅ Bot ishga tushirish uchun tayyor!")
    print("Ishga tushirish: python main.py")
