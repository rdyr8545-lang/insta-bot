import os, threading
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7 ❤️"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "❤️ هلا حبيبي البوت شغال 24 ساعة 🔥\n\n📋 انواع الباند:\nفيك 80%\nنيو 75%\nاباحي 10%\nفراود 80%\nاطفال 1%\nسبام 80%")

@bot.message_handler(content_types=['photo'])
def photo(m):
    bot.reply_to(m, "✅ قريت الصورة")

def run_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            continue

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
