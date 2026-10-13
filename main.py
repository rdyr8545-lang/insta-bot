import os
from flask import Flask
from threading import Thread
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

users_list = []
cases_list = []

@app.route('/')
def home():
    return "Bot is running 24/7 ❤️"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,
        "مرحباً بك ببوت محمد صباح العظيم 💥🥊\n\n"
        "البوت شغال 24 ساعة 🟢\n\n"
        "📋 الاوامر:\n"
        "/baninfo - انواع الباند بالتفصيل 📋\n"
        "/ipbypass - فك حظر IP للاندرويد 📱\n"
        "/pending - كليشة فك الطعن المعلق 📝\n"
        "/verifytip - طريقة التوثيق المجاني MAX ✅\n"
        "/list - عرض اليوزرات\n"
        "/add - اضافة يوزر\n"
        "/remove - حذف يوزر\n"
        "/check - فحص يوزر\n"
        "/addcase - اضافة قضية\n"
        "/checkcase - فحص القضايا\n"
        "/listcase - عرض كل القضايا\n"
        "/clear - مسح الكل"
    )

@bot.message_handler(commands=['baninfo'])
def baninfo(m): bot.reply_to(m, "📋 انواع الباند: 24 ساعة، اسبوع، شهر، دائم")
@bot.message_handler(commands=['ipbypass'])
def ipbypass(m): bot.reply_to(m, "📱 فك حظر IP: وضع طيران + DNS 1.1.1.1 + VPN امريكي")
@bot.message_handler(commands=['pending'])
def pending(m): bot.reply_to(m, "📝 كليشة: مرحبا فريق تيك توك حسابي انحظر بالخطأ ارجو فك الحظر")
@bot.message_handler(commands=['verifytip'])
def verifytip(m): bot.reply_to(m, "✅ توثيق MAX: فوق 10K + نشر يومي + تحقق بخطوتين")
@bot.message_handler(commands=['list'])
def list_users(m):
    bot.reply_to(m, "📋 اليوزرات:\n" + "\n".join(users_list) if users_list else "القائمة فارغة")
@bot.message_handler(commands=['add'])
def add_user(m):
    try: users_list.append(m.text.split()[1]); bot.reply_to(m, f"تم اضافة {m.text.split()[1]} ✅")
    except: bot.reply_to(m, "استخدم: /add @username")
@bot.message_handler(commands=['remove'])
def remove_user(m):
    try: users_list.remove(m.text.split()[1]); bot.reply_to(m, "تم الحذف 🗑️")
    except: bot.reply_to(m, "اليوزر مو موجود")
@bot.message_handler(commands=['check'])
def check_user(m):
    try: bot.reply_to(m, "✅ موجود" if m.text.split()[1] in users_list else "❌ مو موجود")
    except: bot.reply_to(m, "استخدم: /check @username")
@bot.message_handler(commands=['addcase'])
def addcase(m):
    try: cases_list.append(m.text.split(maxsplit=1)[1]); bot.reply_to(m, "تم اضافة القضية ✅")
    except: bot.reply_to(m, "استخدم: /addcase اسم القضية")
@bot.message_handler(commands=['checkcase'])
def checkcase(m): bot.reply_to(m, f"عندك {len(cases_list)} قضية")
@bot.message_handler(commands=['listcase'])
def listcase(m): bot.reply_to(m, "📂 القضايا:\n" + "\n".join(cases_list) if cases_list else "ماكو قضايا")
@bot.message_handler(commands=['clear'])
def clear_all(m): users_list.clear(); cases_list.clear(); bot.reply_to(m, "تم مسح الكل ✅")

def run_bot():
    while True:
        try: bot.infinity_polling()
        except: continue

if __name__ == "__main__":
    Thread(target=run_flask).start()
    Thread(target=run_bot).start()