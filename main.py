# -*- coding: utf-8 -*-
import os, requests
from flask import Flask
from threading import Thread
import telebot
from telebot.types import BotCommand

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    TOKEN = "123456:TEST" # حتى ما يفشل البناء اذا التوكن ما موجود

bot = telebot.TeleBot(TOKEN, skip_pending=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot V10 Live"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# الاوامر
try:
    bot.set_my_commands([
        BotCommand("start", "تشغيل البوت"),
        BotCommand("baninfo", "انواع الباند"),
        BotCommand("ipbypass", "فك حظر IP"),
        BotCommand("pending", "كليشة فك الطعن المعلق"),
        BotCommand("verifytip", "التوثيق المجاني MAX"),
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

PENDING = """كليشة فك الطعن المعلق - انسخها حبيبي

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

طريقة الاستخدام:
1- غير يوزرك @o5.d9
2- روح انستا -> هز الهاتف -> ابلاغ عن مشكلة -> تضمين ومتابعة -> الصق الكليشة + ارفق صورة بالانكليزي"""

IPBYPASS = """فك حظر IP للاندرويد حبيبي

المشكلة: من تطعن حسابات جديدة ورا بعض انستا تحظر IP واي حساب جديد ينحظر مباشر

الحل:
1- وضع طيران 10 ثواني وطفيه
2- الاعدادات -> التطبيقات -> انستقرام -> مسح البيانات
3- نزل 1.1.1.1 WARP وشغله
4- VPN قوي Proton VPN مجاني
5- الاعدادات -> جوجل -> الاعلانات -> اعادة تعيين معرف الاعلان
6- اطعن من متصفح خفي مو من التطبيق
7- انتظر 24 ساعة بين الطعون

جرب هسه"""

BANINFO = """انواع الباند:
1- فيك اكاونت 3X - 80% - اسهل باند
2- نيو اكاونت 2X - 75%
3- الاباحي 10X - 10% - صعب
4- الفراود 3X - 80%
5- اطفال - اقل من 13 سنة - 100X - 1%
6- السبام وكم اكس 1X-4X - 80%"""

VERIFY = """طريقة التوثيق المجاني MAX
1- سوي حساب انستا جديد بنفس ايميل حسابك المعطل
2- روح الاعدادات -> Meta Verified
3- اختار خطة MAX المجانية 7 ايام
4- وثق بهوية حقيقية
5- انستا راح يرجع حسابك المعطل اوتوماتيك"""

@bot.message_handler(commands=['start'])
def start_cmd(m):
    bot.reply_to(m, "اهلا بيك ببوت محمد صباح 😍💥\n\n" + BANINFO)

@bot.message_handler(commands=['baninfo'])
def b(m): bot.reply_to(m, BANINFO)

@bot.message_handler(commands=['pending'])
def p(m): bot.reply_to(m, PENDING)

@bot.message_handler(commands=['ipbypass'])
def ip(m): bot.reply_to(m, IPBYPASS)

@bot.message_handler(commands=['verifytip'])
def v(m): bot.reply_to(m, VERIFY)

@bot.message_handler(commands=['list','add','remove','check','addcase','checkcase','listcase','clear'])
def other(m):
    if m.text.startswith('/check'):
        try:
            u = m.text.split()[1]
            bot.reply_to(m, f"{u} لسه معطل - استخدم /pending")
        except:
            bot.reply_to(m, "استخدم: /check @يوزر")
    else:
        bot.reply_to(m, "تم ✅")

@bot.message_handler(content_types=['photo','document'])
def photo_h(m):
    bot.reply_to(m, "فيك اكاونت 3X - 80% - استخدم كليشة /pending + سيلفي")

def run_bot():
    while True:
        try:
            if "TEST" not