import os, json, requests, re
from flask import Flask
from threading import Thread
import telebot
from telebot.types import BotCommand

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, skip_pending=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot V8 Full Commands Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# هاي القائمة الي بالصورة
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
    except:
        pass

def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({"users": watched_users, "cases": cases}, f, ensure_ascii=False, indent=2)

BANINFO = """📋🔥 انواع الباند بالتفصيل:

1️⃣ فيك اكاونت 3X - 80% يرجع ✅
2️⃣ نيو اكاونت 2X - 75% يرجع ⚠️ (creating new accounts)
3️⃣ الاباحي 10X - 10% فقط 💀
4️⃣ الفراود 3X - 80% يرجع 💰
5️⃣ اطفال 100X - 1% صعب جدا 😭
6️⃣ السبام 1X-4X - 80% اسهل باند ✅
"""

def extract_ban(text):
    low = text.lower()
    if "new accounts" in low or "creating another" in low or "avoiding" in low or "bypass" in low:
        return "🔵 نيو اكاونت 2X - 75% يرجع ⚠️ (تجاوز الحظر بحساب جديد)"
    elif "pretend to be" in low or "impersonation" in low or "impersonating" in low:
        return "🟣 فيك اكاونت 3X - 80% يرجع ✅"
    elif "under 13" in low:
        return "👶 اطفال 100X - 1% 😭"
    elif "sexual" in low or "nudity" in low:
        return "🔞 اباحي 10X - 10% 💀"
    elif "fraud" in low:
        return "💰 فراود 3X - 80%"
    elif "spam" in low:
        return "📨 سبام 1X-4X - 80% ✅"
    else:
        return "🟣 فيك اكاونت 3X - 80% ✅"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"❤️ هلا بالبوت الاسطوري V8 محمد صباح\n\n{BANINFO}")

@bot.message_handler(commands=['baninfo'])
def baninfo(m):
    bot.reply_to(m, BANINFO)

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m):
    bot.reply_to(m, "📱 فك حظر IP للاندرويد:\n1- وضع طيران 10 ثواني\n2- مسح بيانات انستا\n3- شغل WARP 1.1.1.1\n4- VPN Proton\n5- اطعن من متصفح خفي")

@bot.message_handler(commands=['pending'])
def pending(m):
    bot.reply_to(m, "Hello Instagram Support Team,\nMy account @[username] was disabled by mistake. Please review manually.\nUsername: @[username]\nThank you")

@bot.message_handler(commands=['verifytip'])
def verifytip(m):
    bot.reply_to(m, "✅ طريقة التوثيق المجاني MAX:\nوثق حساب جديد بنفس ايميل المعطل فئة MAX مجاني وتعال ارجعلك المعطل ❤️")

@bot.message_handler(commands=['list'])
def lst(m):
    users = watched_users.get(m.chat.id, [])
    if users:
        bot.reply_to(m, "📋 اليوزرات:\n" + "\n".join([f"@{u}" for u in users]))
    else:
        bot.reply_to(m, "القائمة فارغة")

@bot.message_handler(commands=['add'])
def add_u(m):
    try:
        u = m.text.split()[1].replace("@","").lower()
        watched_users.setdefault(m.chat.id, [])
        if u not in watched_users[m.chat.id]:
            watched_users[m.chat.id].append(u)
            save()
        bot.reply_to(m, f"✅ ضفت @{u}")
    except:
        bot.reply_to(m, "استخدم: /add @يوزر")

@bot.message_handler(commands=['remove'])
def rem(m):
    try:
        u = m.text.split()[1].replace("@","").lower()
        if u in watched_users.get(m.chat.id, []):
            watched_users[m.chat.id].remove(u)
            save()
            bot.reply_to(m, f"✅ حذفت @{u}")
        else:
            bot.reply_to(m, f"@{u} مو موجود")
    except:
        bot.reply_to(m, "استخدم: /remove @يوزر")

@bot.message_handler(commands=['check'])
def chk(m):
    try:
        u = m.text.split()[1].replace("@","").lower()
        headers = {"User-Agent":"Mozilla/5.0","X-IG-App-ID":"936619743392459"}
        r = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={u}", headers=headers, timeout=10)
        if r.status_code==200 and len(r.text)>500:
            bot.reply_to(m, f"🟢 @{u} رجع! 🎉 مبروك")
        else:
            bot.reply_to(m, f"🔴 @{u} لسه معطل")
    except Exception as e:
        bot.reply_to(m, f"❓ ما كدرت افحص: {e}")

@bot.message_handler(commands=['addcase'])
def addcase(m):
    try:
        case_id = m.text.split()[1]
        cases[case_id] = {"chat_id": m.chat.id}
        save()
        bot.reply_to(m, f"✅ ضفت القضية {case_id}")
    except:
        bot.reply_to(m, "استخدم