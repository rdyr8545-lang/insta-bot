import os, json, re, requests, io
from datetime import datetime
from flask import Flask
from threading import Thread
from PIL import Image, ImageOps, ImageEnhance
import telebot
from telebot.types import BotCommand

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, skip_pending=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot V8 Final Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

try:
    bot.set_my_commands([
        BotCommand("start", "❤️ تشغيل البوت"),
        BotCommand("baninfo", "📋 انواع الباند بالتفصيل"),
        BotCommand("ipbypass", "📱 فك حظر IP"),
        BotCommand("pending", "📝 كليشة فك الطعن"),
        BotCommand("verifytip", "✅ توثيق MAX"),
        BotCommand("list", "عرض اليوزرات"),
        BotCommand("add", "اضافة يوزر"),
        BotCommand("remove", "حذف يوزر"),
        BotCommand("check", "فحص يوزر"),
        BotCommand("addcase", "اضافة قضية"),
        BotCommand("checkcase", "فحص القضايا"),
        BotCommand("listcase", "عرض كل القضايا"),
        BotCommand("clear", "مسح الكل"),
    ])
except: pass

FILE = "watched_cases.json"
watched_users, cases = {}, {}
if os.path.exists(FILE):
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            j = json.load(f)
            watched_users = {int(k): v for k, v in j.get("users", {}).items()}
            cases = j.get("cases", {})
    except: pass

def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({"users": watched_users, "cases": cases}, f, ensure_ascii=False, indent=2)

def enhance_image(b):
    try:
        img = Image.open(io.BytesIO(b)).convert('RGB')
        w,h = img.size
        if w < 1000: img = img.resize((w*3, h*3), Image.LANCZOS)
        img = ImageEnhance.Contrast(img).enhance(1.8)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
        buf = io.BytesIO(); img.save(buf, format='JPEG', quality=95)
        return buf.getvalue()
    except: return b

def ocr_online(b):
    for data in [b, enhance_image(b)]:
        for lang in ['eng','ara+eng','ara']:
            try:
                r = requests.post("https://api.ocr.space/parse/image",
                    data={'apikey':'K87899142388957','language':lang,'OCREngine':2,'scale':True},
                    files={'file':('img.jpg', data, 'image/jpeg')}, timeout=30)
                j = r.json()
                if j.get('ParsedResults'):
                    t = j['ParsedResults'][0].get('ParsedText','')
                    if len(t.strip()) > 10: return t
            except: continue
    return ""

BANINFO_TEXT = """📋 انواع الباند بالتفصيل:

1️⃣ فيك اكاونت 3X - 80% ✅
2️⃣ نيو اكاونت 2X - 75% ⚠️ تجاوز قيود بحساب جديد
3️⃣ الاباحي 10X - 10% 💀
4️⃣ الفراود 3X - 80% 💰
5️⃣ اطفال 100X - 1% 😭
6️⃣ السبام 1X-4X - 80% ✅
"""

def extract_ban(text):
    u="o5.d9"; d="August 8, 2026"; k="integrity_fake"
    low = text.lower()
    mm=re.search(r'access to ([a-zA-Z0-9._]+)', text, re.I)
    if mm: u=mm.group(1)
    u=u.lower().replace("@","").strip()

    # 🔥 التركيز هنا - نيو قبل فيك
    if "new accounts" in low or "new account" in low or "creating another" in low or "avoiding" in low or "bypass" in low:
        k = "integrity_new"
    elif "impersonation" in low or "pretend to be" in low or "impersonating" in low or "fake" in low:
        k = "integrity_fake"
    elif "under 13" in low:
        k = "under13"
    elif "sexual" in low or "nudity" in low:
        k = "sexual"
    elif "fraud" in low:
        k = "fraud"
    elif "spam" in low:
        k = "spam"
    else:
        k = "integrity_fake"
    return u,d,k,text

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, f"❤️ هلا بالبوت الاسطوري V8\n\n{BANINFO_TEXT}\n\nدز صورة تعطيل هسه!")

@bot.message_handler(commands=['baninfo'])
def baninfo(m): bot.reply_to(m, BANINFO_TEXT)

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m): bot.reply_to(m, "📱 فك حظر IP: وضع طيران + مسح بيانات + WARP + VPN")

@bot.message_handler(commands=['pending'])
def pending(m): bot.reply_to(m, "Hello Instagram Support,\nMy account @[username] disabled by mistake. Please review.\nUsername: @[username]")

@bot.message_handler(commands=['verifytip'])
def verifytip(m): bot.reply_to(m, "✅ وثق حساب جديد بنفس ايميل المعطل MAX وتعال ارجعلك المعطل")

@bot.message_handler(commands=['list'])
def lst(m):
    users=watched_users.get(m.chat.id, [])
    bot.reply_to(m, "\n".join([f"@{u}" for u in users]) if users else "فارغة")

@bot.message_handler(commands=['add'])
def add_u(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        watched_users.setdefault(m.chat.id, [])
        if u not in watched_users[m.chat.id]: watched_users[m.chat.id].