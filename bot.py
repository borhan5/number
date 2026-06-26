import telebot
import requests
import time
import threading
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8953289994:AAEAO-JUoARj2RJRkOoi7BHuXqbHwjfvahw'
API_KEY = 'MQGVM5B5OOW'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# ওটিপি গ্রুপ ও লিঙ্ক
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- কান্ট্রি ফ্ল্যাগ হেল্পার ---
def get_flag(country_name):
    flags = {
        "Benin": "🇧🇯", "Ivory Coast": "🇨🇮", "Guinea": "🇬🇳", 
        "Central African Rep.": "🇨🇫", "United Kingdom": "🇬🇧", 
        "Bangladesh": "🇧🇩", "USA": "🇺🇸", "India": "🇮🇳", "Vietnam": "🇻🇳"
    }
    return flags.get(country_name, "🌍")

# --- ওয়েব সার্ভার (বট সচল রাখতে) ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Bot is Running"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- মেইন মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("💰 Balance"),
        types.KeyboardButton("🖥️ Console"), types.KeyboardButton("📊 Stats")
    )
    return markup

# --- ওটিপি চেক ফাংশন ---
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        otp_msg = (
                            f"⚡️ **Borhan OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        # গ্রুপে লগ
                        group_log = (
                            f"📢 **Borhan OTP Success**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num[:6]}***{num[-2:]}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"🌐 Service: {service_name}\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        return
        except: pass
        time.sleep(10)

# --- কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"🤖 **Welcome to Borhan OTP!**\n\n"
        f"Hello {message.from_user.first_name}, বোরহান ওটিপি সার্ভিস থেকে "
        f"আপনার পছন্দের সার্ভিসটি বেছে নিন।"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_service(m):
    bot.send_chat_action(m.chat.id, 'typing')
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            # প্যানেলের প্রথম ৪টি সার্ভিস ফিল্টার করা হচ্ছে
            services = res['data']['services'][:4]
            markup = types.InlineKeyboardMarkup(row_width=1)
            
            for s in services:
                markup.add(types.InlineKeyboardButton(f"📲 {s['sid']}", callback_data=f"ser_{s['sid']}"))
            
            bot.send_message(m.chat.id, "💎 **প্রথম ৪টি মেইন সার্ভিস (Full Traffic):**", reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(m.chat.id, "❌ সার্ভার সমস্যা। আবার চেষ্টা করুন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
    services = res['data']['services']
    selected = next((item for item in services if item['sid'] == sid), None)
    
    if selected:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for r in selected['ranges']:
            rid = r.replace("XXX", "")
            markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_{sid}_{rid}"))
        
        bot.edit_message_text(f"📍 **Service: {sid}**\nএকটি রেঞ্জ সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(("buy_", "change_")))
def buy_process(call):
    data = call.data.split("_")
    sid, rid = data[1], data[2]
    user_name = call.from_user.first_name
    
    bot.edit_message_text(f"⏳ **{sid} এর নাম্বার চেক হচ্ছে...**", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num_data = res['data']
            full_num = num_data['full_number']
            clean_num = num_data['no_plus_number']
            country = num_data['country']
            flag = get_flag(country)
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{sid}_{rid}"),
                types.InlineKeyboardButton("🌍 Change Country", callback_data=f"ser_{sid}")
            )
            markup.add(types.InlineKeyboardButton("📢 Join OTP Group", url=GROUP_LINK))
            
            response_text = (
                f"✅ **নাম্বার পাওয়া গেছে!**\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"{flag} **Country:** {country}\n"
                f"📱 **Number:** `{full_num}`\n"
                f"🧩 **Service:** {sid}\n"
                f"━━━━━━━━━━━━━━\n"
                f"⏳ **ওটিপির জন্য অপেক্ষা করুন...**"
            )
            bot.edit_message_text(response_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            threading.Thread(target=poll_otp, args=(call.message.chat.id, clean_num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Stock Out:** {res['message']}", call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, "❌ কানেকশন এরর।")

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def check_balance(m):
    bot.reply_to(m, "💳 **Account Balance:**\nব্যালেন্স রিফিলের জন্য অ্যাডমিনের সাথে যোগাযোগ করুন।")

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def show_console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            text = "🖥️ **Borhan OTP Live Hits:**\n\n"
            for h in hits[:5]:
                text += f"🔹 {h['sid']} | `{h['range']}` | ✅ Hit\n"
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
    except: pass

# --- বট স্টার্ট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan OTP Pro is Starting...")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except:
            time.sleep(10)
