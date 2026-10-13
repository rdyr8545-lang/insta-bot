import os, json, re, requests
from flask import Flask
from threading import Thread
import telebot
from telebot.types import BotCommand

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, skip_pending=True)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot V8 Full Commands Running"

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

FILE="watched_cases.json"
watched_users,cases={},{}
if os.path.exists(FILE):
    try:
        with open(FILE,"r",encoding="utf-8") as f:
            j=json.load(f)
            watched_users={int(k):v for k,v in j.get("users",{}).items()}
            cases=j.get("cases",{})
    except: pass

def save():
    with open(FILE,"w",encoding="utf-8") as f:
        json.dump({"users":watched_users,"cases":cases},f,ensure_ascii=False,indent=2)

BANINFO="""📋🔥 انواع الباند:
1️⃣ فيك اكاونت 3X - 80% ✅
2️⃣ نيو اكاونت 2X - 75% ⚠️
3️⃣ الاباحي 10X - 10% 💀
4️⃣ الفراود 3X - 80% 💰
5️⃣ اطفال 100X - 1% 😭
6️⃣ السبام 1X-4X - 80% ✅"""

def extract_ban(text):
    low=text.lower()
    if "new accounts" in low or "creating another" in low or "avoiding" in low or "bypass" in low:
        return "integrity_new","🔵 نيو اكاونت 2X - انشاء حسابات لتجاوز الحظر - 75% يرجع ⚠️"
    else:
        return "integrity_fake","🟣 فيك اكاونت 3X - انتحال - 80% يرجع ✅"

@bot.message_handler(commands=['start'])
def s(m): bot.reply_to(m,f"❤️ هلا بالبوت الاسطوري V8\n\n{BANINFO}\n\nدز صورة تعطيل!")

@bot.message_handler(commands=['baninfo'])
def bi(m): bot.reply_to(m,BANINFO)

@bot.message_handler(commands=['ipbypass'])
def ip(m): bot.reply_to(m,"📱 فك حظر IP:\n1- وضع طيران 10ث\n2- مسح بيانات انستا\n3- شغل WARP 1.1.1.1\n4- Proton VPN")

@bot.message_handler(commands=['pending'])
def pe(m): bot.reply_to(m,"Hello Instagram Team, My account @[يوزرك] disabled by mistake. Please review. Username: @[يوزرك] Thanks")

@bot.message_handler(commands=['verifytip'])
def ve(m): bot.reply_to(m,"✅ وثق حساب جديد بنفس ايميل المعطل فئة MAX مجاني وارجع المعطل ❤️")

@bot.message_handler(commands=['list'])
def li(m):
    u=watched_users.get(m.chat.id,[])
    bot.reply_to(m,"\n".join([f"@{x}" for x in u]) if u else "القائمة فارغة")

@bot.message_handler(commands=['add'])
def ad(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        watched_users.setdefault(m.chat.id,[])
        if u not in watched_users[m.chat.id]: watched_users[m.chat.id].append(u); save()
        bot.reply_to(m,f"✅ ضفت @{u}")
    except: bot.reply_to(m,"/add @يوزر")

@bot.message_handler(commands=['remove'])
def rem(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        if u in watched_users.get(m.chat.id,[]): watched_users[m.chat.id].remove(u); save()
        bot.reply_to(m,f"✅ حذفت @{u}")
    except: bot.reply_to(m,"/remove @يوزر")

@bot.message_handler(commands=['check'])
def ch(m):
    try:
        u=m.text.split()[1].replace("@","").lower()
        h={"User-Agent":"Mozilla/5.0","X-IG-App-ID":"936619743392459"}
        r=requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={u}",headers=h,timeout=10)
        bot.reply_to(m,f"🟢 @{u} رجع!" if r.status_code==200 and len(r.text)>500 else f"🔴 @{u} لسه")
    except: bot.reply_to(m,"❓ ما كدرت افحص")

@bot.message_handler(commands=['addcase'])
def ac(m):
    try: cases[m.text.split()[1]]={"chat_id":m.chat.id}; save(); bot.reply_to(m,"✅ ضفت القضية")
    except: bot.reply_to(m,"/addcase رقم")

@bot.message_handler(commands=['checkcase','listcase'])
def lc(m):
    uc=[k for k,v in cases.items() if v.get("chat_id")==m.chat.id]
    bot.reply_to(m,"\n".join(uc) if uc else "ما عندك قضايا")

@bot.message_handler(commands=['clear'])
def cl(m): watched_users[m.chat.id]=[]; save(); bot.reply_to(m,"✅ مسحت الكل")

@bot.message_handler(content_types=['photo','document'])
def ph(m):
    bot.send_message(m.chat.id,"⏳ دا اقرا الصورة...")
    try:
        fid=m.photo[-1].file_id if m.content_type=='photo' else m.document.file_id
        url=f"https://api.telegram.org/file/bot{TOKEN}/{bot.get_file(fid).file_path}"
        data=requests.get(url).content
        r=requests.post("https://api.ocr.space/parse/image",data={'apikey':'K87899142388957','language':'eng','OCREngine':2},files={'file':('img.jpg',data,'image/jpeg')},timeout=30)
        text=r.json()['ParsedResults'][0]['ParsedText']
        k,detail=extract_ban(text)
        bot.reply_to(m,f"{detail}\n\nالنص: {text[:300]}\n\n{BANINFO}")
    except Exception as e: bot.reply_to(m,f"❌ {e}")

def run_bot():
    while True:
        try: bot.infinity_polling()
        except: continue

if __name__=="__main__":
    Thread(target=run_flask).start()
    run_bot()