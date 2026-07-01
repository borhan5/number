import os
import telebot
import requests
import threading
import time
import re  # OTP এক্সট্রাক্ট করার জন্য
from telebot import types
from flask import Flask

# --- রেন্ডার সার্ভার চালু রাখার জন্য ---
app = Flask('')
@app.route('/')
def home(): return "BSNUMBER Bot is Live!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web_server, daemon=True)
    t.start()

# --- কনফিগারেশন ---
API_TOKEN = "8759465408:AAGS-02Bc_PsgKPSWuhx3YuceRm8YS8JQ7I"
VOLTX_KEY = "MQGVM5B5OOW"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

ADMIN_HANDLE = "@borhanRCB"
METHOD_GROUP_ID = -1001859871146 
OTP_LOG_GROUP_ID = -1003968881110  
OTP_LOG_LINK = "https://t.me/Bsnumberotp" 
METHOD_LINK = "https://t.me/earntrick_BS" 

bot = telebot.TeleBot(API_TOKEN, threaded=True)
session = requests.Session()
headers = {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

# --- COUNTRY_DATA (আপনার দেওয়া লিস্টটি এখানে থাকবে) ---
COUNTRY_DATA = {
    "1": {"name": "USA/Canada", "flag": "🇺🇸"}, "7": {"name": "Russia/Kazakhstan", "flag": "🇷🇺"},
    "880": {"name": "Bangladesh", "flag": "🇧🇩"}, "91": {"name": "India", "flag": "🇮🇳"},
    # ... আপনার বাকি সব কান্ট্রি ডাটা এখানে আগের মতোই থাকবে ...
}

# --- ক্যাশ সিস্টেম ---
cache = {"live_data": {}, "ordered_keys": [], "time": 0}

def get_country_info(range_str):
    for length in [4, 3, 2, 1]:
        code = range_str[:length]
        if code in COUNTRY_DATA:
            return COUNTRY_DATA[code]['flag'], COUNTRY_DATA[code]['name']
    return "🏳️", f"Code {range_str[:3]}"

# --- OTP Extract করার ফাংশন ---
def extract_otp_code(text):
    # মেসেজ থেকে ৪ থেকে ৮ ডিজিটের সংখ্যা খুঁজে বের করবে
    match = re.search(r'\b\d{4,8}\b', text)
    return match.group(0) if match else "N/A"

def fetch_live_data():
    if time.time() - cache["time"] < 60:
        return cache["live_data"], cache["ordered_keys"]
    try:
        res = session.get(f"{BASE_URL}/liveaccess", headers=headers, timeout=10).json()
        if res.get('meta', {}).get('code') == 200:
            fb_ig_priority = []
            others = []
            all_data = {}
            for service in res['data']['services']:
                sid = service['sid'].lower()
                is_priority = "facebook" in sid or "instagram" in sid
                for r in service['ranges']:
                    flag, name = get_country_info(r)
                    key = f"{flag} {name}"
                    if key not in all_data: all_data[key] = []
                    if r not in all_data[key]: all_data[key].append(r)
                    if is_priority:
                        if key not in fb_ig_priority: fb_ig_priority.append(key)
                    else:
                        if key not in fb_ig_priority and key not in others: others.append(key)
            final_keys = fb_ig_priority + others
            cache["live_data"], cache["ordered_keys"], cache["time"] = all_data, final_keys, time.time()
            return all_data, final_keys
    except: pass
    return cache["live_data"], cache["ordered_keys"]

# --- ওটিপি মনিটরিং (Updated with Extraction) ---
def monitor_otp(chat_id, number, country_info, user_name):
    start_time = time.time()
    seen_otps = set()
    while time.time() - start_time < 900:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10).json()
            if res.get('meta', {}).get('code') == 200:
                for o in res['data']['otps']:
                    if str(o['number']) == str(number):
                        full_msg = o['message']
                        if full_msg not in seen_otps:
                            # ওটিপি কোডটি আলাদা করা হচ্ছে
                            extracted_otp = extract_otp_code(full_msg)
                            
                            otp_text = (
                                "┏━━━━━━━━━━━━━━━━━━┓\n"
                                "     🎉 **NEW OTP RECEIVED** 🎉\n"
                                "┗━━━━━━━━━━━━━━━━━━┛\n\n"
                                f"📟 **OTP CODE:** `{extracted_otp}`\n\n"
                                f"📱 **Number:** `{number}`\n"
                                f"💬 **Full Message:** `{full_msg}`\n\n"
                                "✨ *Thank you for using BSNUMBER!*"
                            )
                            bot.send_message(chat_id, otp_text, parse_mode="Markdown")
                            
                            log = (
                                "📢 **OTP LOG REPORT**\n"
                                f"👤 **User:** {user_name}\n"
                                f"🌍 **Country:** {country_info}\n"
                                f"📱 **Number:** `{number}`\n"
                                f"🔑 **OTP:** `{extracted_otp}`\n"
                                f"💬 **Full Msg:** `{full_msg}`"
                            )
                            try: bot.send_message(OTP_LOG_GROUP_ID, log, parse_mode="Markdown")
                            except: pass
                            seen_otps.add(full_msg)
            time.sleep(10)
        except: time.sleep(10)

# --- বাকি কমান্ড হ্যান্ডলারগুলো (আগের মতোই থাকবে) ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "┏━━━━━━━ ✨ ━━━━━━━┓\n"
        "   🌟 **BS-NUMBER PREMIUM** 🌟\n"
        "┗━━━━━━━ ✨ ━━━━━━━┛\n\n"
        "👋 **স্বাগতম!** আমাদের প্যানেলে আপনাকে স্বাগতম।\n"
        "এখানে আপনি দ্রুততম সময়ে সার্ভিস পাবেন।\n\n"
        "⚡ **Status:** `Active 🟢`"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔥 Facebook & Instagram", callback_data="page_0"),
        types.InlineKeyboardButton("🚀 Method Group", url=METHOD_LINK)
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data
    # ... এখানে আপনার বাকি হ্যান্ডলারগুলো (page_, c_, ord_, back_start) হুবহু একই থাকবে ...
    # (আপনার অরিজিনাল কোড থেকে এই অংশটুকু কপি করে বসাবেন)
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        live_data, ordered_keys = fetch_live_data()
        if not ordered_keys:
            bot.answer_callback_query(call.id, "❌ No Stock Currently!", show_alert=True)
            return
        per_page = 16
        start_idx, end_idx = page * per_page, (page + 1) * per_page
        current_list = ordered_keys[start_idx:end_idx]
        text = "━━━━━━━━━━━━━━━━━━━━\n🌍 **SELECT YOUR COUNTRY** 🌍\n━━━━━━━━━━━━━━━━━━━━\n\n👇 নিচে থেকে দেশ সিলেক্ট করুন:"
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(c, callback_data=f"c_{c[:15]}") for c in current_list]
        markup.add(*btns)
        nav_btns = []
        if page > 0: nav_btns.append(types.InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
        if end_idx < len(ordered_keys): nav_btns.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}"))
        if nav_btns: markup.add(*nav_btns)
        markup.add(types.InlineKeyboardButton("🏠 Back to Menu", callback_data="back_start"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("c_"):
        c_short = data[2:]
        live_data, ordered_keys = fetch_live_data()
        full_name = next((k for k in live_data if k.startswith(c_short)), None)
        if full_name:
            ranges = live_data[full_name]
            text = f"📍 **COUNTRY:** {full_name}\n📡 **Select Your Range:**"
            markup = types.InlineKeyboardMarkup(row_width=2)
            btns = [types.InlineKeyboardButton(f"📡 Range {r}", callback_data=f"ord_{r}") for r in ranges[:14]]
            markup.add(*btns)
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="page_0"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif data.startswith("ord_"):
        rid = data.split("_")[1]
        bot.answer_callback_query(call.id, "🔄 Fetching Number...")
        try:
            res = session.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}, timeout=10).json()
            if res.get('meta', {}).get('code') == 200:
                num = res['data']['no_plus_number']
                country = res['data']['country']
                user = call.from_user.first_name
                success_text = f"✅ **NUMBER GENERATED**\n\n🌍 **Country:** `{country}`\n📱 **Number:** `{num}`\n\n⌛ **Status:** `Waiting for OTP... 🔄`"
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"ord_{rid}"))
                markup.add(types.InlineKeyboardButton("🏠 Menu", callback_data="back_start"))
                bot.edit_message_text(success_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
                threading.Thread(target=monitor_otp, args=(call.message.chat.id, num, country, user), daemon=True).start()
            else:
                bot.send_message(call.message.chat.id, "❌ **Sorry!** No stock.")
        except: pass

    elif data == "back_start":
        start(call.message)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
