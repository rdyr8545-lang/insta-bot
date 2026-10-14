# -*- coding: utf-8 -*-
import os
import requests
from flask import Flask
from threading import Thread
import telebot
from telebot.types import BotCommand

TOKEN = os.getenv("BOT_TOKEN", "8276343460:AAENJ23ULVEqAnwxfHVY4vVvIWSkYTGDJ1E")
bot = telebot.TeleBot(TOKEN, skip_pending=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "اهلا بيك ببوت محمد صباح - Bot V10 Live"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

PENDING = """📝🔥 كليشة فك الطعن المعلق - انسخها حبيبي 😎

Hello Instagram Support Team,

I hope you are doing well.

I am writing to follow up on my appeal for my account @[حط يوزرك هنا]. My account was disabled and I submitted an appeal a long time ago