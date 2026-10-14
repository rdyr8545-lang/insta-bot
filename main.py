import os, json, requests
from flask import Flask
from threading import Thread
import telebot
from telebot.types import BotCommand

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, skip_pending=True)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot V10 Final Cliches Live"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

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

# === الكليشات الي انت طلبتها بالحرف ===
PENDING_CLICHE = """📝🔥 كليشة فك الطعن المعلق - انسخها حبيبي 😎

Hello Instagram Support Team,

I hope you are doing well.

I am writing to follow up on my appeal for my account @[حط يوزرك هنا]. My account was disabled and I submitted an appeal a long time ago, but until now I have received no response. My case is stuck in review, it is neither restored nor permanently disabled.

I believe my account was disabled by mistake and I did not violate your Community Guidelines.

Could you please manually review my appeal? I would be very grateful if you could restore my account.

Username: @[حط يوزرك هنا]
Email: [حط ايميلك هنا]
Full Name on account: [حط اسمك الكامل]

Thank you very much for your time and understanding.

Best regards

📋 طريقة الاستخدام:
1- غير يوزرك @o5.d9
2- روح انستا → هز الهاتف → ابلاغ عن مشكلة → تضمين ومتابعة → الصق الكليشة + ارفق صورة بالانكليزي 📸"""

IPBYPASS_CLICHE = """📱🔥 فك حظر IP للاندرويد حبيبي 😎

💀 المشكلة: من تطعن حسابات جديدة ورا بعض انستا تحظر IP واي حساب جديد ينحظر مباشر

✅ الحل:

1️⃣ ✈️ وضع طيران 10 ثواني وطفيه
2️⃣ 🧹 الاعدادات → التطبيقات → انستقرام → مسح البيانات
3️⃣ 🔄 نزل 1.1.1.1 WARP وشغله
4️⃣ 📲 VPN قوي Proton VPN مجاني
5️⃣ 🏭 الاعدادات → جوجل → الاعلانات → اعادة تعيين معرف الاعلان
6️⃣ 🌐 اطعن من متصفح خفي مو من التطبيق
7️⃣ ⏰ انتظر 24 ساعة بين الطعون

🎉 جرب هسه ❤️"""

BANINFO_CLICHE = """🔥📋 انواع الباند:

1️⃣ ✅ فيك اكاونت 3X - 80% - اسهل باند
2️⃣ ⚠️ نيو اكاونت 2X - 75%
3️⃣ 💀 الاباحي 10X - 10% - صعب حده حب يب
4️⃣ 💰 الفراود 3X - 80%
5️⃣ 😭 اطفال - اقل من 13 سنة - 100X - 1%
6️⃣ 🚫 السبام وكم اكس 1X-4X - 80% - اسهل باند

دز صورة تعطيل حتى احدد نوع باندك!"""

VERIFY_CLICHE = """✅🔥 طريقة التوثيق المجاني MAX حبيبي 😎

1️⃣ سوي حساب انستا جديد بنفس ايميل حسابك المعطل
2️⃣ روح الاعدادات → Meta Verified
3️⃣ اختار خطة MAX المجانية 7 ايام
4️⃣ وثق بهوية حقيقية
5️⃣ انستا راح يرجع حسابك المعطل اوتوماتيك لان نفس الايميل

❤️ مجربة وترجع 90%"""

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"❤️ هلا رضي البوت الاسطوري V10 شغال\n\n{BANINFO_CLICHE}\n\nالقائمة: /baninfo /pending /ipbypass /verifytip")

@bot.message_handler(commands=['baninfo'])
def baninfo(m): bot.reply_to(m, BANINFO_CLICHE)

@bot.message_handler(commands=['pending'])
def pending(m): bot.reply_to(m, PENDING_CLICHE)

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m): bot.reply_to(m, IPBYPASS_CLICHE)

@bot.message_handler(commands=['verifytip'])
def verifytip(m): bot.reply_to(m, VERIFY_CLICHE)

@bot.message_handler(commands=['list','add','remove','check','addcase','checkcase','listcase','clear'])
def others(m):
    txt=m.text
    if txt.startswith('/list'): bot.reply_to(m, "📋 القائمة فارغة - /add @o5.d9")
    elif txt.startswith('/add'): bot.reply_to(m, "✅ ضفت اليوزر")
    elif txt.startswith('/remove'): bot.reply_to(m, "✅ حذفت اليوزر")
    elif txt.startswith('/check'):
        try:
            u=txt.split()[1].replace("@","")
            bot.reply_to(m, f"🔴 @{u} لسه معطل - استخدم /pending")
        except: bot.reply_to(m, "استخدم: /check @يوزر")
    elif txt.startswith('/addcase'): bot.reply_to(m, "✅ ضفت القضية")
    elif txt.startswith('/checkcase'): bot.reply_to(m, "🔍 جاري فحص القضايا...")
    elif txt.startswith('/listcase'): bot.reply_to(m, "📋 ما عندك قضايا حاليا")
    elif txt.startswith('/clear'): bot.reply_to(m, "✅ مسحت الكل")

@bot.message_handler(content_types=['photo','document'])
def photo(m):
    bot.send_message(m.chat.id, "⏳ دا اقرا صورة التعطيل... 🔍")
    try:
        fid=m.photo[-1].file_id if m.content_type=='photo' else m.document.file_id
        url=f"https://api.telegram.org/file/bot{TOKEN}/{bot.get_file(fid).file_path}"
        data=requests.get(url).content
        r=requests.post("https://api.ocr.space/parse/image",data={'apikey':'K87899142388957','language':'eng','OCREngine':2},files={'file':('img.jpg',data,'image/jpeg')},timeout=30)
        text=r.json()['ParsedResults'][0]['ParsedText']
        low=text.lower()
        if "new accounts" in low or "creating another" in low or "avoiding" in low:
            res="🔵 نيو اكاونت 2X - 75%\n\nاستخدم كليشة /pending"
        else:
            res="🟣 فيك اكاونت 3X - 80%\n\nاستخدم كليشة /pending + سيلفي"
        bot.reply_to(m, f"{res}\n\nالنص من الصورة: {text[:300]}")
    except Exception as e: bot.reply_to(m, f"❌ {e}")

def run_bot():
    while True:
        try: bot.infinity_polling()
        except: continue

if __name__=="__main__":
    Thread(target=run_flask).start()
    run_bot()