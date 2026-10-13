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
    return "Bot is running 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,
        "🥊💥 مرحباً بك ببوت محمد صباح العظيم 💥🥊\n\n"
        "🟢 البوت شغال 24 ساعة\n\n"
        "📋 الاوامر:\n"
        "/baninfo - انواع الباند بالتفصيل\n"
        "/ipbypass - فك حظر IP\n"
        "/pending - كليشة فك الطعن الانكلش الاصلية\n"
        "/verifytip - طريقة التوثيق MAX\n"
        "/list - عرض اليوزرات\n"
        "/add - اضافة يوزر\n"
        "/remove - حذف يوزر\n"
        "/check - فحص يوزر\n"
        "/addcase - اضافة قضية\n"
        "/checkcase - فحص القضايا\n"
        "/listcase - عرض القضايا\n"
        "/clear - مسح الكل"
    )

@bot.message_handler(commands=['baninfo'])
def baninfo(m):
    bot.reply_to(m,
        "📋 انواع الباند في تيك توك بالتفصيل:\n\n"