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

# --- ডাটা স্টোরেজ (নাম্বার চেঞ্জ করার জন্য) ---
user_data = {} # {chat_id: {'rid': rid, 'sid': sid, 'numbers': []}}

# --- Render Web Server ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- হেল্পার ফাংশন ---
def extract_otp(msg):
    match = re.search(r'\b\d{5,6}\b', str(msg))
    return match.group(0) if match else msg

def mask_number(num_str):
    num_str = str(num_str)
    return f"{num_str[:4]}****{num_str[-2:]}" if len(num_str) > 6 else num_str

# --- মেইন মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("📦 Stock Number"),
        types.KeyboardButton("🔐 Get 2FA"), types.KeyboardButton("🔎 Extract OTP"),
        types.KeyboardButton("📊 Stats"), types.KeyboardButton("💰 Balance")
    )
    return markup

# --- ওটিপি প্যানেল জেনারেটর (ছবির মতো UI) ---
def get_number_panel(chat_id, country_name="Unknown"):
    data = user_data.get(chat_id, {})
    numbers = data.get('numbers', [])
    sid = data.get('sid', 'Service')
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # বর্তমান নাম্বারগুলো বাটন হিসেবে (ছবির মতো)
    for num in numbers:
        markup.add(types.InlineKeyboardButton(f"📱 📋 {num}", callback_data="copy_num"))
        
    # কন্ট্রোল বাটন
    markup.add(types.InlineKeyboardButton("⏩ Change Number", callback_data="change_num"))
    markup.add(types.InlineKeyboardButton("🌐 Change Service", callback_data="get_num_start"))
    
    # বটম বাটন (Home & OTP Group)
    btn_home = types.InlineKeyboardButton("🏘 Home", callback_data="back_home")
    btn_group = types.InlineKeyboardButton("📩 OTP Group ↗️", url=GROUP_LINK)
    markup.row(btn_home, btn_group)
    
    text = (f"🌍 **Country : 🇧🇯 {country_name}**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🌀 *Waiting for OTP*")
    return text, markup

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
                        bot.send_message(chat_id, f"📩 **OTP Received!**\n📱 `{num}`\n🔑 Code: `{display_code}`")
                        
                        group_log = (f"📢 **Successful Hit**\n📱 `{mask_number(num)}` | 🔑 `{display_code}`\n👤 `{user_name}`")
                        try: bot.send_message(GROUP_ID, group_log)
                        except: pass
                        return
        except: pass
        time.sleep(10)

# --- কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, WELCOME_IMAGE, caption="🤖 **Welcome! Select a service:**", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def get_num_start_msg(m):
    show_services(m.chat.id)

def show_services(chat_id):
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        services = [s for s in res['data']['services'] if s['sid'] in ALLOWED_SERVICES]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for s in services:
            markup.add(types.InlineKeyboardButton(f"📱 {s['sid']}", callback_data=f"ser_{s['sid']}"))
        bot.send_message(chat_id, "✨ **সিলেক্ট করুন:**", reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "get_num_start")
def get_num_back(call):
    show_services(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_home")
def back_home(call):
    bot.send_message(call.message.chat.id, "🏘 মেইন মেনু", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def select_range(call):
    sid = call.data.split("_")[1]
    res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
    selected = next((s for s in res['data']['services'] if s['sid'] == sid), None)
    markup = types.InlineKeyboardMarkup(row_width=1)
    if selected:
        for r in selected['ranges']:
            rid = r.replace("XXX", "").replace("X", "")
            markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_{sid}_{rid}"))
    bot.edit_message_text(f"🎯 **{sid}** রেঞ্জ সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# --- নাম্বার ক্রয় ও প্যানেল আপডেট ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data == "change_num")
def process_buy(call):
    chat_id = call.message.chat.id
    user_name = call.from_user.first_name
    
    if call.data.startswith("buy_"):
        _, sid, rid = call.data.split("_")
        user_data[chat_id] = {'rid': rid, 'sid': sid, 'numbers': []}
    else:
        data = user_data.get(chat_id)
        if not data: return
        sid, rid = data['sid'], data['rid']

    bot.answer_callback_query(call.id, "⏳ নাম্বার নেওয়া হচ্ছে...")
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num = res['data']['full_number']
            clean_num = res['data']['no_plus_number']
            country = res['data'].get('country', 'Benin')
            
            # প্যানেলে নাম্বার আপডেট (সর্বোচ্চ ৩টি দেখাবে)
            user_data[chat_id]['numbers'].insert(0, num)
            user_data[chat_id]['numbers'] = user_data[chat_id]['numbers'][:3]
            
            text, markup = get_number_panel(chat_id, country)
            
            # আগের মেসেজ এডিট করে প্যানেল দেখানো
            bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            # ওটিপি পোলিং শুরু
            threading.Thread(target=poll_otp, args=(chat_id, clean_num, user_name)).start()
        else:
            bot.answer_callback_query(call.id, f"❌ {res['message']}", show_alert=True)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "copy_num")
def copy_alert(call):
    bot.answer_callback_query(call.id, "✅ নাম্বারটি কপি করে আপনার অ্যাপে ব্যবহার করুন।", show_alert=False)

# --- রান বোট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    bot.polling(none_stop=True)
