import os
from flask import Flask
from threading import Thread
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot V8 Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

BANINFO = """📋 انواع الباند ونسب الرجوع:

1️⃣ فيك اكاونت 3X - 80% يرجع
2️⃣ نيو اكاونت 2X - 75% يرجع
3️⃣ الاباحي 10X - 10% فقط
4️⃣ الفراود 3X - 80% يرجع
5️⃣ اطفال 100X - 1% صعب
6️⃣ السبام 1X-4X - 80% اسهل باند
"""

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"❤️ هلا بالبوت الاسطوري V8\n\n{BANINFO}\n\n/ipbypass\n/pending\n/verifytip")

@bot.message_handler(commands=['baninfo'])
def baninfo(m):
    bot.reply_to(m, BANINFO)

@bot.message_handler(commands=['pending'])
def pending(m):
    bot.reply_to(m, "Hello Instagram Support Team,\nMy account @[username] disabled by mistake.\nPlease review manually.\nUsername: @[username]\nThank you")

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m):
    bot.reply_to(m, "فك حظر IP: وضع طيران + مسح بيانات انستا + WARP 1.1.1.1 + VPN")

@bot.message_handler(commands=['verifytip'])
def verifytip(m):
    bot.reply_to(m, "وثق حساب جديد بنفس ايميل المعطل فئة MAX مجاني وتعال ارجعلك المعطل")

@bot.message_handler(commands=['list','add','remove','check','clear'])
def other(m):
    bot.reply_to(m, "تم ✅")

def run_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            continue

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()