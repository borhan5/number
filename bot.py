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
WELCOME_IMAGE = "https://i.ibb.co/hC4nFfC/welcome-image.jpg"

ALLOWED_SERVICES = ["Facebook", "Instagram", "WhatsApp"]

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- Render Web Server ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- ওটিপি ফিল্টার (৫ ও ৬ সংখ্যা) ---
def extract_otp(msg):
    match6 = re.search(r'\b\d{6}\b', str(msg))
    if match6: return match6.group(0)
    match5 = re.search(r'\b\d{5}\b', str(msg))
    if match5: return match5.group(0)
    return msg

# --- নাম্বার মাস্কিং ---
def mask_number(num_str):
    num_str = str(num_str)
    if len(num_str) > 6:
        return f"{num_str[:4]}****{num_str[-2:]}"
    return num_str

# --- মেইন মেনু ---
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

# --- ওটিপি পোলিং ---
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
                        bot.send_message(chat_id, f"📩 **New OTP Received!**\n━━━━━━━━━━━━━━\n📱 Number: `{num}`\n🔑 Code: `{display_code}`\n━━━━━━━━━━━━━━", parse_mode="Markdown")
                        
                        masked_num = mask_number(num)
                        group_log = (f"📢 **New Successful Hit**\n━━━━━━━━━━━━━━\n"
                                     f"📱 Number: `{masked_num}`\n🔑 Code: `{display_code}`\n"
                                     f"👤 User: {user_name}\n━━━━━━━━━━━━━━")
                        try: bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        except: pass
                        return
        except: pass
        time.sleep(10)

# --- স্মার্ট ট্রাফিক ট্র্যাকিং ফাংশন (কনসোল থেকে একটিভ রেঞ্জ বের করা) ---
def get_high_traffic_ranges(service_id):
    active_ranges = []
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS, timeout=10).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            # কনসোলে এই সার্ভিসের যে রেঞ্জগুলোতে ওটিপি হিট হয়েছে সেগুলো ফিল্টার করা
            for hit in hits:
                if hit['sid'] == service_id:
                    active_ranges.append(hit['range'])
    except: pass
    return list(set(active_ranges)) # ইউনিক রেঞ্জ লিস্ট

# --- স্টার্ট কমান্ড ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = f"🤖 The Profit Player | 👋 Hello, {message.from_user.first_name}!\n✔️ Select a service from the buttons below:"
    try:
        bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, reply_markup=main_menu())
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# --- গেট নাম্বার (স্মার্ট সিলেকশনসহ) ---
@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def show_services(m):
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            markup = types.InlineKeyboardMarkup(row_width=1)
            for s in services:
                if s['sid'] in ALLOWED_SERVICES:
                    markup.add(types.InlineKeyboardButton(f"📱 {s['sid']}", callback_data=f"ser_{s['sid']}"))
            markup.add(types.InlineKeyboardButton("🌍 Custom Range", callback_data="custom_range"))
            bot.send_message(m.chat.id, "✨ **একটি সার্ভিস নির্বাচন করুন:**", reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    bot.edit_message_text(f"⏳ **{sid}** এর জন্য হাই-ট্রাফিক রেঞ্জ চেক করা হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    try:
        # ১. কনসোল থেকে হাই-ট্রাফিক রেঞ্জগুলো খুঁজে বের করা
        hot_ranges = get_high_traffic_ranges(sid)
        
        # ২. সাধারণ এভেইলেবল রেঞ্জগুলো নেওয়া
        res_live = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        selected = next((item for item in res_live['data']['services'] if item['sid'] == sid), None)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # প্রথমে হাই-ট্রাফিক রেঞ্জগুলো দেখাবে
        for hr in hot_ranges:
            rid = hr.replace("XXX", "").replace("X", "")
            markup.add(types.InlineKeyboardButton(f"🔥 {hr} (High Traffic)", callback_data=f"buy_Any_{rid}"))
        
        # তারপর বাকি সব রেঞ্জ
        if selected:
            for r in selected['ranges']:
                if r not in hot_ranges: # ডুপ্লিকেট এড়াতে
                    rid = r.replace("XXX", "").replace("X", "")
                    markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_Any_{rid}"))
        
        bot.edit_message_text(f"🎯 **{sid}** এর রেঞ্জ সিলেক্ট করুন:\n(🔥 চিহ্নিত রেঞ্জগুলো থেকে বর্তমানে ওটিপি আসছে)", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup)
    except: pass

# --- নাম্বার ক্রয় ও ওটিপি প্রসেস ---
def buy_action(m, rid):
    user_name = m.from_user.first_name
    bot.send_message(m.chat.id, "⏳ নাম্বার সংগ্রহ করা হচ্ছে...")
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

@bot.callback_query_handler(func=lambda call: call.data == "custom_range")
def custom_range_input(call):
    msg = bot.send_message(call.message.chat.id, "⌨️ **রেঞ্জটি লিখুন (যেমন: 224654):**")
    bot.register_next_step_handler(msg, lambda m: buy_action(m, m.text.strip().replace("X","").replace("x","")))

# --- রান বোট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    bot.polling(none_stop=True)
