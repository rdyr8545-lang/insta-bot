import os
from flask import Flask
from threading import Thread
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

users = []
cases = []

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "مرحبا بك ببوت محمد صباح العظيم\nالبوت شغال 24 ساعة\n\n/baninfo\n/pending\n/ipbypass")

@bot.message_handler(commands=['baninfo'])
def baninfo(m):
    txt = (
        "انواع الباند بالتفصيل:\n\n"
        "1- 24h Ban : حظر 24 ساعة\n"
        "2- 7 Days Ban : حظر اسبوع سبام\n"
        "3- 30 Days Ban : حظر شهر\n"
        "4- Shadow Ban : نزول مشاهدات 80%\n"
        "5- IP Ban : حظر الايبي ما تكدر تسوي حساب جديد\n"
        "6- Permanent Ban : باند دائم\n"
        "7- Age Ban : حظر عمر\n"
        "8- Pending Appeal : الطعن معلق\n"
    )
    bot.reply_to(m, txt)

@bot.message_handler(commands=['pending'])
def pending(m):
    txt = (
        "الكليشة الانكلش الاصلية:\n\n"
        "Hello TikTok Support Team,\n"
        "My account @[username] has been incorrectly banned. I have not violated any community guidelines. I am a real person and my content is original.\n"
        "Please review my account again manually.\n"
        "Account: @[username]\n"
        "Thank you"
    )
    bot.reply_to(m, txt)

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m):
    bot.reply_to(m, "فك حظر IP: وضع طيران 10 ثواني + DNS 1.1.1.1 + VPN امريكي + مسح بيانات تيك توك")

@bot.message_handler(commands=['list'])
def list_u(m):
    bot.reply_to(m, "\n".join(users) if users else "فارغة")

@bot.message_handler(commands=['add'])
def add_u(m):
    try:
        users.append(m.text.split()[1])
        bot.reply_to(m, "تم")
    except:
        bot.reply_to(m, "استخدم /add @username")

@bot.message_handler(commands=['remove'])
def rem_u(m):
    try:
        users.remove(m.text.split()[1])
        bot.reply_to(m, "تم الحذف")
    except:
        bot.reply_to(m, "مو موجود")

@bot.message_handler(commands=['clear'])
def clear_u(m):
    users.clear()
    cases.clear()
    bot.reply_to(m, "تم مسح الكل")

def run_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            continue

if __name__ == "__main__":
    Thread(target=run_flask).start()
    Thread(target=run_bot).start()