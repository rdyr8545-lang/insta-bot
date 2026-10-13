import os, requests, re
from flask import Flask
from threading import Thread
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def extract_ban(text):
    low = text.lower()
    if "new accounts" in low or "creating another" in low or "avoiding" in low or "bypass" in low:
        return "integrity_new", "🔵 نيو اكاونت 2X - 75% ⚠️"
    else:
        return "integrity_fake", "🟣 فيك اكاونت 3X - 80% ✅"

@bot.message_handler(commands=['start','baninfo'])
def start(m):
    bot.reply_to(m, "1️⃣ فيك 3X - 80%\n2️⃣ نيو 2X - 75%\n3️⃣ اباحي 10%\n4️⃣ فراود 80%\n5️⃣ اطفال 1%\n6️⃣ سبام 80%")

@bot.message_handler(content_types=['photo'])
def photo(m):
    try:
        fid = m.photo[-1].file_id
        file_info = bot.get_file(fid)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
        data = requests.get(file_url).content
        r = requests.post("https://api.ocr.space/parse/image",
            data={'apikey':'K87899142388957','language':'eng','OCREngine':2},
            files={'file':('img.jpg', data, 'image/jpeg')}, timeout=30)
        text = r.json()['ParsedResults'][0]['ParsedText']
        k, detail = extract_ban(text)
        bot.reply_to(m, f"✅ قريت الصورة\n{detail}\n\nالنص: {text[:300]}")
    except Exception as e:
        bot.reply_to(m, f"❌ {e}")

def run_bot():
    while True:
        try: bot.infinity_polling()
        except: continue

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()