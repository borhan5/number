import telebot
import requests
import time
import threading
import re
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8942060883:AAEkcbE5sQuWs9xiAkxftDdONPkTYSuFcr8'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
WELCOME_IMAGE = "https://i.ibb.co/hC4nFfC/welcome-image.jpg" # আপনার ছবির ডাইরেক্ট লিঙ্ক এখানে দিন

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- Render Web Server (বট সচল রাখতে) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- ৫ বা ৬ সংখ্যার ওটিপি ফিল্টার ---
def extract_otp(msg):
    match5 = re.search(r'\b\d{5}\b', str(msg))
    if match5: return match5.group(0)
    match6 = re.search(r'\b\d{6}\b', str(msg))
    if match6: return match6.group(0)
    return msg

# --- নাম্বার মাস্কিং ---
def mask_number(num_str):
    num_str = str(num_str)
    if len(num_str) > 6:
        return f"{num_str[:4]}****{num_str[-2:]}"
    return num_str

# --- মেইন মেনু (হুবহু স্ক্রিনশটের মতো) ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📞 Get Number")
    btn2 = types.KeyboardButton("📦 Stock Number")
    btn3 = types.KeyboardButton("🔐 Get 2FA")
    btn4 = types.KeyboardButton("🔎 Extract OTP")
    btn5 = types.KeyboardButton("📊 Stats")
    btn6 = types.KeyboardButton("💰 Balance")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# --- ওটিপি পোলিং ও ফরওয়ার্ডিং ---
def poll_otp(chat_id, num, user_name):
    start_time = time.time()
    while time.time() - start_time < 300: 
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                otps = r['data'].get('otps', [])
                for o in otps:
                    if str(o['number']) == str(num):
                        display_code = extract_otp(o['message'])
                        # ইউজারকে ওটিপি পাঠানো
                        bot.send_message(chat_id, f"📩 **New OTP Received!**\n━━━━━━━━━━━━━━\n📱 Number: `{num}`\n🔑 Code: `{display_code}`\n━━━━━━━━━━━━━━", parse_mode="Markdown")
                        
                        # গ্রুপে সাকসেস লগ পাঠানো
                        masked_num = mask_number(num)
                        group_log = (f"📢 **New Successful Hit**\n━━━━━━━━━━━━━━\n"
                                     f"📱 Number: `{masked_num}`\n🔑 Code: `{display_code}`\n"
                                     f"👤 User: {user_name}\n━━━━━━━━━━━━━━")
                        try: bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        except: pass
                        return
        except: pass
        time.sleep(10)

# --- স্টার্ট কমান্ড (ছবিসহ ওয়েলকাম মেসেজ) ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = f"🤖 The Profit Player | 👋 Hello, {message.from_user.first_name}!\n✔️ Select a service from the buttons below:"
    try:
        # ছবির লিঙ্ক ঠিক থাকলে ছবিসহ পাঠাবে
        bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, reply_markup=main_menu())
    except:
        # ছবি কাজ না করলে শুধু টেক্সট পাঠাবে
        bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# --- গেট নাম্বার প্রসেস ---
@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def show_services(m):
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            markup = types.InlineKeyboardMarkup(row_width=2)
            for s in services:
                markup.add(types.InlineKeyboardButton(f"📱 {s['sid']}", callback_data=f"ser_{s['sid']}"))
            # কাস্টম রেঞ্জ বাটন
            markup.add(types.InlineKeyboardButton("🌍 Custom Range", callback_data="custom_range"))
            bot.send_message(m.chat.id, "✨ **সার্ভিস নির্বাচন করুন:**", reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        selected = next((item for item in res['data']['services'] if item['sid'] == sid), None)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if selected:
            for r in selected['ranges']:
                rid = r.replace("XXX", "").replace("X", "")
                markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_Any_{rid}"))
        bot.edit_message_text(f"🎯 **{sid}** এর জন্য রেঞ্জ সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "custom_range")
def custom_range_input(call):
    msg = bot.send_message(call.message.chat.id, "⌨️ **রেঞ্জটি লিখুন (যেমন: 224654):**")
    bot.register_next_step_handler(msg, process_custom_buy)

def process_custom_buy(message):
    rid = message.text.strip().replace("X", "").replace("x", "")
    if rid.isdigit():
        buy_action(message, rid)
    else:
        bot.reply_to(message, "❌ ভুল রেঞ্জ ফরম্যাট।")

# --- নাম্বার ক্রয় ফাংশন ---
def buy_action(m, rid):
    user_name = m.from_user.first_name
    bot.send_message(m.chat.id, "⏳ নাম্বার খোঁজা হচ্ছে...")
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            full_num = res['data']['full_number']
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 আমাদের গ্রুপে জয়েন করুন", url=GROUP_LINK))
            bot.send_message(m.chat.id, f"✅ **Number Received!**\n📱 `{full_num}`\n⏳ ওটিপির জন্য অপেক্ষা করুন...", 
                             reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(m.chat.id, num, user_name)).start()
        else:
            bot.send_message(m.chat.id, f"❌ {res['message']}")
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_callback(call):
    rid = call.data.split("_")[2]
    buy_action(call.message, rid)

# --- কনসোল এবং ব্যালেন্স বাটন ---
@bot.message_handler(func=lambda m: True)
def handle_text(m):
    if m.text == "💰 Balance":
        bot.reply_to(m, "💰 আপনার ব্যালেন্স এপিআই ড্যাশবোর্ড থেকে চেক করুন।")
    elif m.text == "🖥️ Console":
        try:
            res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
            hits = res['data'].get('hits', [])
            txt = "🖥️ **Live Active Console**\n━━━━━━━━━━━━━━\n"
            for h in hits[:10]:
                txt += f"🔹 {h['sid']} | `{mask_number(h['range'])}` | Code: {extract_otp(h['message'])}\n"
            bot.send_message(m.chat.id, txt, parse_mode="Markdown")
        except: pass
    else:
        bot.reply_to(m, "⚙️ এই ফিচারটি শীঘ্রই যুক্ত করা হবে।")

# --- বট স্টার্ট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Bot is Starting...")
    bot.polling(none_stop=True)
