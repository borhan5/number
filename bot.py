import os
import telebot
import requests
import threading
import time
import re
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

# --- ২০০+ দেশের ডাটাবেজ ---
COUNTRY_DATA = {
    "1": {"name": "USA/Canada", "flag": "🇺🇸"}, "7": {"name": "Russia/Kazakhstan", "flag": "🇷🇺"},
    "20": {"name": "Egypt", "flag": "🇪🇬"}, "211": {"name": "South Sudan", "flag": "🇸🇸"},
    "212": {"name": "Morocco", "flag": "🇲🇦"}, "213": {"name": "Algeria", "flag": "🇩🇿"},
    "216": {"name": "Tunisia", "flag": "🇹🇳"}, "218": {"name": "Libya", "flag": "🇱🇾"},
    "220": {"name": "Gambia", "flag": "🇬🇲"}, "221": {"name": "Senegal", "flag": "🇸🇳"},
    "222": {"name": "Mauritania", "flag": "🇲🇷"}, "223": {"name": "Mali", "flag": "🇲🇱"},
    "224": {"name": "Guinea", "flag": "🇬🇳"}, "225": {"name": "Ivory Coast", "flag": "🇨🇮"},
    "226": {"name": "Burkina Faso", "flag": "🇧🇫"}, "227": {"name": "Niger", "flag": "🇳🇪"},
    "228": {"name": "Togo", "flag": "🇹🇬"}, "229": {"name": "Benin", "flag": "🇧🇯"},
    "230": {"name": "Mauritius", "flag": "🇲🇺"}, "231": {"name": "Liberia", "flag": "🇱🇷"},
    "232": {"name": "Sierra Leone", "flag": "🇸🇱"}, "233": {"name": "Ghana", "flag": "🇬🇭"},
    "234": {"name": "Nigeria", "flag": "🇳🇬"}, "235": {"name": "Chad", "flag": "🇹🇩"},
    "236": {"name": "Central Africa", "flag": "🇨🇫"}, "237": {"name": "Cameroon", "flag": "🇨🇲"},
    "238": {"name": "Cape Verde", "flag": "🇨🇻"}, "239": {"name": "Sao Tome", "flag": "🇸🇹"},
    "240": {"name": "Equat. Guinea", "flag": "🇬🇶"}, "241": {"name": "Gabon", "flag": "🇬🇦"},
    "242": {"name": "Congo", "flag": "🇨🇬"}, "243": {"name": "DR Congo", "flag": "🇨🇩"},
    "244": {"name": "Angola", "flag": "🇦🇴"}, "245": {"name": "Guinea-Bissau", "flag": "🇬🇼"},
    "248": {"name": "Seychelles", "flag": "🇸🇨"}, "249": {"name": "Sudan", "flag": "🇸🇩"},
    "250": {"name": "Rwanda", "flag": "🇷🇼"}, "251": {"name": "Ethiopia", "flag": "🇪🇹"},
    "252": {"name": "Somalia", "flag": "🇸🇴"}, "253": {"name": "Djibouti", "flag": "🇩🇯"},
    "254": {"name": "Kenya", "flag": "🇰🇪"}, "255": {"name": "Tanzania", "flag": "🇹🇿"},
    "256": {"name": "Uganda", "flag": "🇺🇬"}, "257": {"name": "Burundi", "flag": "🇧🇮"},
    "258": {"name": "Mozambique", "flag": "🇲🇿"}, "260": {"name": "Zambia", "flag": "🇿🇲"},
    "261": {"name": "Madagascar", "flag": "🇲🇬"}, "263": {"name": "Zimbabwe", "flag": "🇿🇼"},
    "264": {"name": "Namibia", "flag": "🇳🇦"}, "265": {"name": "Malawi", "flag": "🇲🇼"},
    "266": {"name": "Lesotho", "flag": "🇱🇸"}, "267": {"name": "Botswana", "flag": "🇧🇼"},
    "268": {"name": "Eswatini", "flag": "🇸🇿"}, "269": {"name": "Comoros", "flag": "🇰🇲"},
    "27": {"name": "South Africa", "flag": "🇿🇦"}, "33": {"name": "France", "flag": "🇫🇷"},
    "44": {"name": "UK", "flag": "🇬🇧"}, "49": {"name": "Germany", "flag": "🇩🇪"},
    "62": {"name": "Indonesia", "flag": "🇮🇩"}, "66": {"name": "Thailand", "flag": "🇹🇭"},
    "880": {"name": "Bangladesh", "flag": "🇧🇩"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "971": {"name": "UAE", "flag": "🇦🇪"},
    "998": {"name": "Uzbekistan", "flag": "🇺🇿"}
}

# --- উন্নত ওটিপি এক্সট্রাক্ট ফাংশন (আপডেটেড) ---
def extract_otp(text):
    # ১. প্রথমে চেক করবে ৩+৩ ফরম্যাটে স্পেস দিয়ে কোড আছে কি না (যেমন: 139 265)
    match_with_space = re.search(r'\b(\d{3})\s(\d{3})\b', text)
    if match_with_space:
        return f"{match_with_space.group(1)}{match_with_space.group(2)}"
    
    # ২. যদি স্পেস ছাড়া ৪ থেকে ৮ ডিজিটের কোড থাকে (যেমন: 123456)
    match_straight = re.search(r'\b\d{4,8}\b', text)
    if match_straight:
        return match_straight.group(0)
    
    return "No Code Found"

# --- ক্যাশ সিস্টেম ---
cache = {"live_data": {}, "ordered_keys": [], "time": 0}

def get_country_info(range_str):
    for length in [4, 3, 2, 1]:
        code = range_str[:length]
        if code in COUNTRY_DATA:
            return COUNTRY_DATA[code]['flag'], COUNTRY_DATA[code]['name']
    return "🏳️", f"Code {range_str[:3]}"

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

# --- ওটিপি মনিটরিং ---
def monitor_otp(chat_id, number, country_info, user_name):
    start_time = time.time()
    seen_otps = set()
    while time.time() - start_time < 900:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10).json()
            if res.get('meta', {}).get('code') == 200:
                for o in res['data']['otps']:
                    if str(o['number']) == str(number):
                        otp_msg = o['message']
                        if otp_msg not in seen_otps:
                            # এখানে নতুন এক্সট্রাক্ট ফাংশন ব্যবহার হচ্ছে
                            extracted_code = extract_otp(otp_msg)
                            
                            otp_text = (
                                "┏━━━━━━━━━━━━━━━━━━┓\n"
                                "     🎉 **NEW OTP RECEIVED** 🎉\n"
                                "┗━━━━━━━━━━━━━━━━━━┛\n\n"
                                f"📟 **OTP CODE:** `{extracted_code}`\n\n"
                                f"📱 **Number:** `{number}`\n"
                                f"💬 **Full Message:** `{otp_msg}`\n\n"
                                "✨ *Thank you for using BSNUMBER!*"
                            )
                            bot.send_message(chat_id, otp_text, parse_mode="Markdown")
                            
                            log = (
                                "📢 **OTP LOG REPORT**\n"
                                f"👤 **User:** {user_name}\n"
                                f"🌍 **Country:** {country_info}\n"
                                f"📱 **Number:** `{number}`\n"
                                f"🔑 **OTP Code:** `{extracted_code}`\n"
                                f"💬 **Message:** `{otp_msg}`"
                            )
                            try: bot.send_message(OTP_LOG_GROUP_ID, log, parse_mode="Markdown")
                            except: pass
                            seen_otps.add(otp_msg)
            time.sleep(10)
        except: time.sleep(10)

# --- বটের কমান্ড হ্যান্ডলার ---
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
    
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        live_data, ordered_keys = fetch_live_data()
        if not ordered_keys:
            bot.answer_callback_query(call.id, "❌ No Stock Currently!", show_alert=True)
            return
        
        per_page = 16
        start_idx, end_idx = page * per_page, (page + 1) * per_page
        current_list = ordered_keys[start_idx:end_idx]
        
        text = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌍 **SELECT YOUR COUNTRY** 🌍\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💠 **Page:** `{page+1}`\n"
            "👇 নিচে থেকে দেশ সিলেক্ট করুন:"
        )
        
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
            text = (
                f"📍 **COUNTRY:** {full_name}\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📡 **Select Your Range:**\n"
                "সবচেয়ে ভালো রেঞ্জটি বেছে নিন।"
            )
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
                
                success_text = (
                    "┏━━━━━━━━━━━━━━━━━━┓\n"
                    "   ✅ **NUMBER GENERATED** ✅\n"
                    "┗━━━━━━━━━━━━━━━━━━┛\n\n"
                    f"🌍 **Country:** `{country}`\n"
                    f"📱 **Number:** `{num}`\n\n"
                    "⌛ **Status:** `Waiting for OTP... 🔄`"
                )
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"ord_{rid}"))
                markup.add(types.InlineKeyboardButton("🚀 Method Group", url=METHOD_LINK))
                markup.add(types.InlineKeyboardButton("📢 OTP Log Group", url=OTP_LOG_LINK))
                markup.add(types.InlineKeyboardButton("🏠 Menu", callback_data="back_start"))
                
                bot.edit_message_text(success_text, call.message.chat.id, call.message.message_id, 
                                     reply_markup=markup, parse_mode="Markdown")
                
                threading.Thread(target=monitor_otp, args=(call.message.chat.id, num, country, user), daemon=True).start()
            else:
                bot.send_message(call.message.chat.id, "❌ **Sorry!** No stock in this range. Try another.")
        except: pass

    elif data == "back_start":
        start(call.message)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
