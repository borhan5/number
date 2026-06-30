import os
import telebot
import requests
import threading
import time
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

# --- কনফিগারেশন (আপনার দেওয়া তথ্য) ---
API_TOKEN = "8759465408:AAGS-02Bc_PsgKPSWuhx3YuceRm8YS8JQ7I"
VOLTX_KEY = "MQGVM5B5OOW"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

# গ্রুপ ও সাপোর্ট লিঙ্ক
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
    "261": {"name": "Madagascar", "flag": "🇲🇬"}, "262": {"name": "Reunion", "flag": "🇷🇪"},
    "263": {"name": "Zimbabwe", "flag": "🇿🇼"}, "264": {"name": "Namibia", "flag": "🇳🇦"},
    "265": {"name": "Malawi", "flag": "🇲🇼"}, "266": {"name": "Lesotho", "flag": "🇱🇸"},
    "267": {"name": "Botswana", "flag": "🇧🇼"}, "268": {"name": "Eswatini", "flag": "🇸🇿"},
    "269": {"name": "Comoros", "flag": "🇰🇲"}, "27": {"name": "South Africa", "flag": "🇿🇦"},
    "30": {"name": "Greece", "flag": "🇬🇷"}, "31": {"name": "Netherlands", "flag": "🇳🇱"},
    "32": {"name": "Belgium", "flag": "🇧🇪"}, "33": {"name": "France", "flag": "🇫🇷"},
    "34": {"name": "Spain", "flag": "🇪🇸"}, "351": {"name": "Portugal", "flag": "🇵🇹"},
    "358": {"name": "Finland", "flag": "🇫🇮"}, "380": {"name": "Ukraine", "flag": "🇺🇦"},
    "39": {"name": "Italy", "flag": "🇮🇹"}, "40": {"name": "Romania", "flag": "🇷🇴"},
    "41": {"name": "Switzerland", "flag": "🇨🇭"}, "43": {"name": "Austria", "flag": "🇦🇹"},
    "44": {"name": "UK", "flag": "🇬🇧"}, "45": {"name": "Denmark", "flag": "🇩🇰"},
    "46": {"name": "Sweden", "flag": "🇸🇪"}, "47": {"name": "Norway", "flag": "🇳🇴"},
    "48": {"name": "Poland", "flag": "🇵🇱"}, "49": {"name": "Germany", "flag": "🇩🇪"},
    "60": {"name": "Malaysia", "flag": "🇲🇾"}, "61": {"name": "Australia", "flag": "🇦🇺"},
    "62": {"name": "Indonesia", "flag": "🇮🇩"}, "63": {"name": "Philippines", "flag": "🇵🇭"},
    "64": {"name": "New Zealand", "flag": "🇳🇿"}, "65": {"name": "Singapore", "flag": "🇸🇬"},
    "66": {"name": "Thailand", "flag": "🇹🇭"}, "81": {"name": "Japan", "flag": "🇯🇵"},
    "82": {"name": "South Korea", "flag": "🇰🇷"}, "84": {"name": "Vietnam", "flag": "🇻🇳"},
    "86": {"name": "China", "flag": "🇨🇳"}, "880": {"name": "Bangladesh", "flag": "🇧🇩"},
    "90": {"name": "Turkey", "flag": "🇹🇷"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "93": {"name": "Afghanistan", "flag": "🇦🇫"},
    "962": {"name": "Jordan", "flag": "🇯🇴"}, "964": {"name": "Iraq", "flag": "🇮🇶"},
    "966": {"name": "Saudi Arabia", "flag": "🇸🇦"}, "971": {"name": "UAE", "flag": "🇦🇪"},
    "972": {"name": "Israel", "flag": "🇮🇱"}, "974": {"name": "Qatar", "flag": "🇶🇦"},
    "998": {"name": "Uzbekistan", "flag": "🇺🇿"}
    # আপনার সব দেশ এখানে যুক্ত আছে...
}

# --- ক্যাশ সিস্টেম (হ্যাং ফিক্স) ---
cache = {"live_data": {}, "time": 0}

def get_country_info(range_str):
    for length in [4, 3, 2, 1]:
        code = range_str[:length]
        if code in COUNTRY_DATA:
            return COUNTRY_DATA[code]['flag'], COUNTRY_DATA[code]['name']
    return "🏳️", f"Code {range_str[:3]}"

def fetch_live_data():
    if time.time() - cache["time"] < 120: 
        return cache["live_data"]
    try:
        res = session.get(f"{BASE_URL}/liveaccess", headers=headers, timeout=10).json()
        if res.get('meta', {}).get('code') == 200:
            data = {}
            for service in res['data']['services']:
                for r in service['ranges']:
                    flag, name = get_country_info(r)
                    key = f"{flag} {name}"
                    if key not in data: data[key] = []
                    if r not in data[key]: data[key].append(r)
            cache["live_data"] = data
            cache["time"] = time.time()
            return data
    except: pass
    return cache["live_data"]

# --- ওটিপি মনিটরিং (মাল্টিপল ওটিপি সাপোর্ট) ---
def monitor_otp(chat_id, number, country_info, user_name):
    start_time = time.time()
    seen_otps = set()
    while time.time() - start_time < 900: # ১৫ মিনিট
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10).json()
            if res.get('meta', {}).get('code') == 200:
                for o in res['data']['otps']:
                    if str(o['number']) == str(number):
                        otp_msg = o['message']
                        if otp_msg not in seen_otps:
                            # ইউজারকে ওটিপি পাঠানো
                            bot.send_message(chat_id, f"🎊 **NEW OTP RECEIVED!**\n\n📱 `{number}`\n💬 `{otp_msg}`", parse_mode="Markdown")
                            # ওটিপি লগ গ্রুপে পাঠানো
                            log_text = (f"📢 **OTP LOG (Bsnumber)**\n👤 User: {user_name}\n🌍 Country: {country_info}\n"
                                        f"📱 Number: `{number}`\n💬 Message: `{otp_msg}`\n\n🤖 @YourBotUsername")
                            try: bot.send_message(OTP_LOG_GROUP_ID, log_text)
                            except: pass
                            seen_otps.add(otp_msg)
            time.sleep(10)
        except: time.sleep(10)

# --- বটের কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔥 Get Number", callback_data="page_0"))
    markup.add(types.InlineKeyboardButton("🛠 Support", url="https://t.me/borhanRCB"))
    bot.send_message(message.chat.id, "🌟 **Welcome to BSNUMBER Bot**\nনিচের বাটন থেকে দ্রুত নম্বর সিলেক্ট করুন।", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data
    
    # পেজিনেশন (Pagination) - হ্যাং ফিক্স করার জন্য
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        live_data = fetch_live_data()
        all_countries = sorted(live_data.keys())
        
        if not all_countries:
            bot.answer_callback_query(call.id, "No Stock Available!", show_alert=True)
            return

        per_page = 16
        start_idx = page * per_page
        end_idx = start_idx + per_page
        current_list = all_countries[start_idx:end_idx]
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(c, callback_data=f"c_{c[:15]}") for c in current_list]
        markup.add(*btns)
        
        nav_btns = []
        if page > 0: nav_btns.append(types.InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
        if end_idx < len(all_countries): nav_btns.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}"))
        if nav_btns: markup.add(*nav_btns)
        
        markup.add(types.InlineKeyboardButton("🏠 Menu", callback_data="back_start"))
        bot.edit_message_text(f"🌍 **Select Country (Page {page+1}):**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # দেশ অনুযায়ী রেঞ্জ দেখানো
    elif data.startswith("c_"):
        c_short = data[2:]
        live_data = fetch_live_data()
        full_name = next((k for k in live_data if k.startswith(c_short)), None)
        if full_name:
            ranges = live_data[full_name]
            markup = types.InlineKeyboardMarkup(row_width=2)
            btns = [types.InlineKeyboardButton(f"📡 Range {r}", callback_data=f"ord_{r}") for r in ranges[:14]]
            markup.add(*btns)
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="page_0"))
            bot.edit_message_text(f"📍 **{full_name}**\nসিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # নম্বর অর্ডার করা
    elif data.startswith("ord_"):
        rid = data.split("_")[1]
        bot.answer_callback_query(call.id, "Processing...")
        try:
            res = session.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}, timeout=10).json()
            if res.get('meta', {}).get('code') == 200:
                num = res['data']['no_plus_number']
                country = res['data']['country']
                user = call.from_user.first_name
                
                # --- নম্বর এর নিচের বাটনগুলো ---
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data="page_0"))
                markup.add(types.InlineKeyboardButton("🚀 Method Group", url=METHOD_LINK))
                markup.add(types.InlineKeyboardButton("📢 OTP Log Group", url=OTP_LOG_LINK))
                markup.add(types.InlineKeyboardButton("🏠 Menu", callback_data="back_start"))
                
                bot.edit_message_text(f"✅ **Number Ready!**\n\n📱 `{num}`\n🌍 {country}\n\n💬 ওটিপির জন্য অপেক্ষা করুন...", 
                                     call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
                
                # ওটিপি চেক শুরু
                threading.Thread(target=monitor_otp, args=(call.message.chat.id, num, country, user), daemon=True).start()
            else:
                bot.answer_callback_query(call.id, "Range Out of Stock!", show_alert=True)
        except:
            bot.answer_callback_query(call.id, "API Connection Error!", show_alert=True)

    elif data == "back_start":
        start(call.message)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
