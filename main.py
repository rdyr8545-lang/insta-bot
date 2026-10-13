import sys, subprocess, os, json, re, requests, io
from datetime import datetime
from flask import Flask
from threading import Thread

try:
    from PIL import Image, ImageOps, ImageEnhance
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageOps, ImageEnhance
try:
    import telebot
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])
    import telebot
from telebot.types import BotCommand

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "حط توكنك هنا"

bot = telebot.TeleBot(BOT_TOKEN, skip_pending=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot V8 is Running 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

try:
    bot.set_my_commands([
        BotCommand("start", "❤️ تشغيل البوت"),
        BotCommand("baninfo", "📋 انواع الباند بالتفصيل"),
        BotCommand("ipbypass", "📱 فك حظر IP للاندرويد"),
        BotCommand("pending", "📝 كليشة فك الطعن المعلق"),
        BotCommand("verifytip", "✅ طريقة التوثيق المجاني MAX"),
        BotCommand("list", "عرض اليوزرات"),
        BotCommand("add", "اضافة يوزر"),
        BotCommand("remove", "حذف يوزر"),
        BotCommand("check", "فحص يوزر"),
        BotCommand("addcase", "اضافة قضية"),
        BotCommand("checkcase", "فحص القضايا"),
        BotCommand("listcase", "عرض كل القضايا"),
        BotCommand("clear", "مسح الكل"),
    ])
except:
    pass

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
        img = Image.open(io.BytesIO(b)).convert('L')
        w,h = img.size
        if w < 1200: img = img.resize((w*4, h*4), Image.LANCZOS)
        img = ImageOps.autocontrast(img, cutoff=1)
        img = ImageEnhance.Sharpness(img).enhance(3.0)
        img = ImageEnhance.Contrast(img).enhance(2.5)
        buf = io.BytesIO(); img.save(buf, format='JPEG', quality=100)
        return buf.getvalue()
    except: return b

def ocr_online(b):
    enh = enhance_image(b)
    for data in [enh, b]:
        for lang in ['eng','ara+eng','ara']:
            try:
                r = requests.post("https://api.ocr.space/parse/image",
                    data={'apikey':'K87899142388957','language':lang,'OCREngine':2,'scale':True},
                    files={'file':('img.jpg', data, 'image/jpeg')}, timeout=50)
                j = r.json()
                if j.get('ParsedResults'):
                    t = j['ParsedResults'][0].get('ParsedText','')
                    if len(t.strip())>3: return t
            except: continue
    return ""

BANINFO_TEXT = """📋🔥 انواع الباند بالتفصيل ونسب الرجوع حبيبي 😎👇

━━━━━━━━━━━━━━━
1️⃣ فيك اكاونت - نزاهة الحساب 🎭 3X
💪 القوة: 3X
📈 نسبة الرجوع: 80% اذا مابي انتهاك ✅
━━━━━━━━━━━━━━━
2️⃣ نيو اكاونت - نزاهة الحساب 2X 🆕 2X
💪 القوة: 2X
📈 نسبة الرجوع: 75% يرجع اذا مابي اي انتهاك ⚠️
━━━━━━━━━━━━━━━
3️⃣ الاباحي 🔞
💪 القوة: 10X 💀
📈 نسبة الرجوع: 10% فقط 😭
━━━━━━━━━━━━━━━
4️⃣ الفراود - غسيل اموال 💸 3X
💪 القوة: 3X
📈 نسبة الرجوع: 80% يرجع اذا مابي انتهاك ✅💰
━━━━━━━━━━━━━━━
5️⃣ اطفال - اقل من 13 سنة 👶
💪 القوة: 100X 💀💀
📈 نسبة الرجوع: 1% - صعب فكه حاليااا
━━━━━━━━━━━━━━━
6️⃣ السبام وكم اكس 📵
💪 القوة: 1X-4X
📈 نسبة الرجوع: 80% اسهل باند ✅
━━━━━━━━━━━━━━━
💡 دز صورة تعطيل هسه وراح اكلك نوع باندك ونسبة رجوعك 😎
"""

def extract_ban(text):
    u="غير معروف"; d="August 8, 2026"; k="integrity_fake"
    mm=re.search(r'access to ([a-zA-Z0-9._]+)', text, re.I)
    if mm: u=mm.group(1)
    else:
        mm=re.search(r'o5\.d9|[a-z0-9][a-z0-9._]{2,29}', text.lower())
        if mm: u=mm.group(0)
    u=u.lower().replace("@","").strip()
    low=text.lower()
    if "under 13" in low: k="under13"
    elif "avoiding" in low or "bypass" in low or "creating another" in low: k="integrity_new"
    elif "sexual" in low or "nudity" in low: k="sexual"
    elif "fraud" in low: k="fraud"
    elif "spam" in low: k="spam"
    else: k="integrity_fake"
    return u,d,k