import telebot
import requests
import time
import threading
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8942060883:AAEkcbE5sQuWs9xiAkxftDdONPkTYSuFcr8'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# ওটিপি ফরওয়ার্ড করার গ্রুপ আইডি এবং আপনার দেওয়া লিঙ্ক
GROUP_ID = -1003968881110  # আপনার গ্রুপ আইডি
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl" # আপনার দেওয়া নতুন লিঙ্ক

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- Render Web Server (বটকে জাগিয়ে রাখার জন্য) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- নাম্বারের মাঝখান থেকে ৩টি সংখ্যা মুছে *** দেওয়ার ফাংশন ---
def mask_number(num_str):
    num_str = str(num_str)
    if len(num_str) > 8:
        # শুরুর ৫টি এবং শেষের ৪টি রেখে মাঝখানে ৩টি সংখ্যা মুছে দিবে
        return f"{num_str[:5]}***{num_str[-4:]}"
    return num_str

# --- মেইন মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("🖥️ Console"),
        types.KeyboardButton("💰 Balance"), types.KeyboardButton("📊 Stats")
    )
    return markup

# --- ওটিপি পোলিং ও ফরওয়ার্ডিং ফাংশন ---
def poll_otp(chat_id, num, user_name):
    start_time = time.time()
    while time.time() - start_time < 300: 
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                otps = r['data'].get('otps', [])
                for o in otps:
                    if str(o['number']) == str(num):
                        # ১. ইউজারকে পার্সোনাল মেসেজ (সম্পূর্ণ নাম্বার)
                        otp_msg = (
                            f"📩 **New OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        # ২. মেইন গ্রুপে মাস্ক করা নাম্বার দিয়ে মেসেজ
                        masked_num = mask_number(num)
                        group_log = (
                            f"📢 **New Successful Hit**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{masked_num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        try:
                            bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        except: pass
                        return
        except: pass
        time.sleep(10)

# --- কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 **The Profit Player Bot Active!**", reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def show_services(m):
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS, timeout=10).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            markup = types.InlineKeyboardMarkup(row_width=2)
            for s in services:
                markup.add(types.InlineKeyboardButton(f"📱 {s['sid']}", callback_data=f"ser_{s['sid']}"))
            bot.send_message(m.chat.id, "🐸 **সেবা নির্বাচন করুন:**", reply_markup=markup, parse_mode="Markdown")
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        services = res['data']['services']
        selected = next((item for item in services if item['sid'] == sid), None)
        if selected:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for r in selected['ranges']:
                rid = r.replace("XXX", "")
                markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_{sid}_{rid}"))
            bot.edit_message_text(f"🌐 **{sid} Service**\nSelect range:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_process(call):
    _, sid, rid = call.data.split("_")
    user_name = call.from_user.first_name
    bot.edit_message_text(f"⏳ **নাম্বার খোঁজা হচ্ছে...**", call.message.chat.id, call.message.message_id)
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS, timeout=15).json()
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            full_num = res['data']['full_number']
            
            # নাম্বারের নিচেই গ্রুপের লিঙ্ক বাটন আকারে দেওয়া হলো
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 আমাদের গ্রুপে জয়েন করুন", url=GROUP_LINK))
            
            bot.edit_message_text(f"✅ **Number Received!**\n📱 `{full_num}`\n⏳ ওটিপির জন্য অপেক্ষা করুন...", 
                                  call.message.chat.id, call.message.message_id, 
                                  reply_markup=markup, parse_mode="Markdown")
            
            threading.Thread(target=poll_otp, args=(call.message.chat.id, num, user_name)).start()
        else:
            bot.answer_callback_query(call.id, f"❌ {res['message']}", show_alert=True)
    except: pass

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def check_balance(m):
    bot.reply_to(m, "💰 Your API account balance needs check.")

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def show_console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            console_text = "🖥️ **Live Hit Console**\n━━━━━━━━━━━━━━\n"
            for hit in hits[:5]:
                console_text += f"🔹 {hit['sid']} | `{hit['range']}`\n"
            bot.send_message(m.chat.id, console_text, parse_mode="Markdown")
    except: pass

# --- বট স্টার্ট লুপ ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Profit Player Bot is Starting...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=40)
        except:
            time.sleep(10)
