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
    return "Bot V8 OCR Running 24/7"

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

BANINFO_TEXT = """📋🔥 انواع الباند بالتفصيل ونسب الرجوع 😎

1️⃣ فيك اكاونت 3X - 80% يرجع اذا مابي انتهاك ✅
2️⃣ نيو اكاونت 2X - 75% يرجع ⚠️
3️⃣ الاباحي 10X - 10% فقط 💀
4️⃣ الفراود 3X - 80% يرجع 💰
5️⃣ اطفال 100X - 1% صعب جدا 😭
6️⃣ السبام 1X-4X - 80% اسهل باند ✅
"""

def extract_ban(text):
    u="o5.d9"; d="August 8, 2026"; k="integrity_fake"
    mm=re.search(r'access to ([a-zA-Z0-9._]+)', text, re.I)
    if mm: u=mm.group(1)
    u=u.lower().replace("@","").strip()
    low=text.lower()
    if "under 13" in low: k="under13"
    elif "avoiding" in low or "bypass" in low: k="integrity_new"
    elif "sexual" in low or "nudity" in low: k="sexual"
    elif "fraud" in low: k="fraud"
    elif "spam" in low: k="spam"
    else: k="integrity_fake"
    return u,d,k,text

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"❤️ هلا بالبوت الاسطوري V8\n\n{BANINFO_TEXT}\n\nدز صورة تعطيل هسه! 😎")

@bot.message_handler(commands=['baninfo'])
def baninfo(m): bot.reply_to(m, BANINFO_TEXT)

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m): bot.reply_to(m, "📱 فك حظر IP:\n1- وضع طيران 10ث\n2- مسح بيانات انستا\n3- شغل WARP 1.1.1.1\n4- VPN Proton\n5- اطعن من متصفح خفي")

@bot.message_handler(commands=['pending'])
def pending(m): bot.reply_to(m, "Hello Instagram Support Team,\nMy account @[يوزرك] was disabled by mistake. Please review manually.\nUsername: @[يوزرك]\nThank you")

@bot.message_handler(commands=['verifytip'])
def verifytip(m): bot.reply_to(m, "✅ وثق حساب جديد بنفس ايميل المعطل فئة MAX مجاني وتعال ارجعلك المعطل ❤️")

@bot.message_handler(commands=['list'])
def lst(m):
    users=watched_users.get(m.chat.id, [])
    txt=f"📋 عندك {len(users)} يوزر:\n" + "\n".join([f"@{u}" for u in users]) if users else "القائمة فارغة"
    bot.reply_to(m, txt)

@bot.message_handler(commands=['add'])
def add_u(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        watched_users.setdefault(m.chat.id, [])
        if u not in watched_users[m.chat.id]: watched_users[m.chat.id].append(u); save()
        bot.reply_to(m, f"✅ ضفت @{u}")
    except: bot.reply_to(m, "/add @يوزر")

@bot.message_handler(commands=['remove'])
def rem(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        if u in watched_users.get(m.chat.id, []): watched_users[m.chat.id].remove(u); save(); bot.reply_to(m, f"✅ حذفت @{u}")
    except: bot.reply_to(m, "/remove @يوزر")

@bot.message_handler(commands=['check'])
def chk(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        headers={"User-Agent":"Mozilla/5.0","X-IG-App-ID":"936619743392459"}
        r=requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={u}", headers=headers, timeout=10)
        bot.reply_to(m, f"🟢 @{u} رجع! 🎉" if r.status_code==200 and len(r.text)>500 else f"🔴 @{u} لسه معطل")
    except: bot.reply_to(m, "❓ ما كدرت افحص")

@bot.message_handler(commands=['addcase'])
def addcase(m):
    try: cases[m.text.split()[1]]={"added":datetime.now().strftime('%Y-%m-%d'),"chat_id":m.chat.id}; save(); bot.reply_to(m, "✅ ضفت القضية")
    except: bot.reply_to(m, "/addcase رقم")

@bot.message_handler(commands=['checkcase','listcase'])
def checkcase(m):
    user_cases={k:v for k,v in cases.items() if not k.startswith("info_") and v.get("chat_id")==m.chat.id}
    bot.reply_to(m, "\n".join(user_cases.keys()) if user_cases else "ما عندك قضايا")

@bot.message_handler(commands=['clear'])
def clr(m): watched_users[m.chat.id]=[]; save(); bot.reply_to(m, "✅ مسحت الكل")

@bot.message_handler(content_types=['photo','document'])
def media(m):
    bot.send_message(m.chat.id, "⏳ دا اقرا الصورة... 🔍")
    try:
        fid = m.photo[-1].file_id if m.content_type=='photo' else m.document.file_id
        data = bot.download_file(bot.get_file(fid).file_path)
        text = ocr_online(data)
        if not text.strip(): text="We disabled your account o5.d9"
        username,date,ban_key,full = extract_ban(text)
        perc = {"integrity_fake":"80% ✅","integrity_new":"75% ⚠️","sexual":"10% 💀","fraud":"80% 💰","under13":"1% 😭","spam":"80% ✅"}.get(ban_key,"70%")
        watched_users.setdefault(m.chat.id, [])
        watched_users[m.chat.id]=[u for u in watched_users[m.chat.id] if u!=username]
        watched_users[m.chat.id].append(username); save()
        bot.reply_to(m, f"✅ قريت الصورة\n👤 @{username}\n🔍 {ban_key}\n📈 {perc}\n\n{BANINFO_TEXT}")
    except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")

def run_bot():
    while True:
        try: bot.infinity_polling()
        except: continue

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()