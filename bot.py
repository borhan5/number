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

# সেশন ডাটা স্টোরেজ
user_sessions = {} # {chat_id: {'sid': sid, 'rid': rid, 'country': name, 'numbers': []}}

# --- Render Web Server ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- ওটিপি ও ট্রাফিক ফাংশন ---
def extract_otp(msg):
    match = re.search(r'\b\d{5,6}\b', str(msg))
    return match.group(0) if match else msg

def get_high_traffic_ranges(sid):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS, timeout=10).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            return list(set([h['range'] for h in hits if h['sid'] == sid]))
    except: pass
    return []

# --- ছবির মতো প্যানেল জেনারেটর ---
def generate_panel(chat_id):
    data = user_sessions.get(chat_id, {})
    numbers = data.get('numbers', [])
    country = data.get('country', 'Benin')
    sid = data.get('sid', 'Facebook')
    
    # আইকন সিলেকশন
    icon = "🔵"
    if "WhatsApp" in sid: icon = "🟢"
    elif "Instagram" in sid: icon = "🟣"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # নাম্বার বাটনগুলো (ছবির মতো)
    for num in numbers:
        markup.add(types.InlineKeyboardButton(f"{icon} 📋 {num}", callback_data="copy_alert"))
        
    # কন্ট্রোল বাটন
    markup.add(types.InlineKeyboardButton("⏩ Change Number", callback_data="act_change_num"))
    markup.add(types.InlineKeyboardButton("🌐 Change Country", callback_data="act_change_country"))
    
    # বটম বাটন
    btn_home = types.InlineKeyboardButton("🏘 Home", callback_data="act_home")
    btn_group = types.InlineKeyboardButton("📩 OTP Group ↗️", url=GROUP_LINK)
    markup.row(btn_home, btn_group)
    
    text = (f"🌐 **Country : 🇧🇯 {country}**\n"
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
                        code = extract_otp(o['message'])
                        bot.send_message(chat_id, f"📩 **OTP Received!**\n📱 `{num}`\n🔑 Code: `{code}`")
                        try: bot.send_message(GROUP_ID, f"📢 **Success Hit**\n📱 `{num}` | 🔑 `{code}`\n👤 `{user_name}`")
                        except: pass
                        return
        except: pass
        time.sleep(10)

# --- কমান্ড ও কলব্যাক হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_photo(m.chat.id, WELCOME_IMAGE, caption="🤖 **The Profit Player Bot Active!**", 
                   reply_markup=main_menu())

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("📞 Get Number", "📦 Stock Number", "🔐 Get 2FA", "🔎 Extract OTP", "📊 Stats", "💰 Balance")
    return markup

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def select_service_step(m):
    res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
    services = [s for s in res['data']['services'] if s['sid'] in ALLOWED_SERVICES]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for s in services:
        markup.add(types.InlineKeyboardButton(f"📱 {s['sid']}", callback_data=f"sel_ser_{s['sid']}"))
    bot.send_message(m.chat.id, "✨ **সার্ভিস সিলেক্ট করুন:**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_ser_"))
def select_range_step(call):
    sid = call.data.split("_")[2]
    hot_ranges = get_high_traffic_ranges(sid)
    res_live = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
    selected = next((s for s in res_live['data']['services'] if s['sid'] == sid), None)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    # হাই ট্রাফিক রেঞ্জ আগে দেখাবে
    for hr in hot_ranges:
        rid = hr.replace("XXX","").replace("X","")
        markup.add(types.InlineKeyboardButton(f"🔥 {hr} (High Traffic)", callback_data=f"buy_{sid}_{rid}"))
    
    if selected:
        for r in selected['ranges']:
            if r not in hot_ranges:
                rid = r.replace("XXX","").replace("X","")
                markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_{sid}_{rid}"))
    
    bot.edit_message_text(f"🎯 **{sid}** এর রেঞ্জ সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# --- বাই ও প্যানেল আপডেট ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data == "act_change_num")
def buy_process(call):
    chat_id = call.message.chat.id
    if call.data.startswith("buy_"):
        _, sid, rid = call.data.split("_")
        user_sessions[chat_id] = {'sid': sid, 'rid': rid, 'numbers': [], 'country': 'Benin'}
    else:
        data = user_sessions.get(chat_id)
        if not data: return
        sid, rid = data['sid'], data['rid']

    bot.answer_callback_query(call.id, "⏳ নাম্বার নেওয়া হচ্ছে...")
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            full_num = res['data']['full_number']
            clean_num = res['data']['no_plus_number']
            country = res['data'].get('country', 'Benin')
            
            # সেশনে নাম্বার আপডেট (সর্বোচ্চ ৩টি ছবির মতো)
            user_sessions[chat_id]['numbers'].insert(0, full_num)
            user_sessions[chat_id]['numbers'] = user_sessions[chat_id]['numbers'][:3]
            user_sessions[chat_id]['country'] = country
            
            text, markup = generate_panel(chat_id)
            bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            threading.Thread(target=poll_otp, args=(chat_id, clean_num, call.from_user.first_name)).start()
        else:
            bot.answer_callback_query(call.id, f"❌ {res['message']}", show_alert=True)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "act_change_country")
def change_country_call(call):
    select_service_step(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "act_home")
def home_call(call):
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "copy_alert")
def copy_alert(call):
    bot.answer_callback_query(call.id, "✅ নাম্বারটি কপি করে আপনার অ্যাপে ব্যবহার করুন।")

# --- রান বোট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    bot.polling(none_stop=True)
