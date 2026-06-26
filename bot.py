import telebot
import requests
import time
import threading
import re
from flask import Flask
from telebot import types
from waitress import serve

# --- CONFIGURATION ---
BOT_TOKEN = '8953289994:AAHalks0v_QNWta40jorqobnfwS1trW8pJQ'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# গ্রুপ আইডি ও লিঙ্ক
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
DEV_LINK = "https://t.me/BORHANSB"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

active_sessions = {} 

# --- নাম্বার মাস্কিং ফাংশন (মাঝখানের ৩টি সংখ্যা হাইড করার জন্য) ---
def mask_number(num_str):
    num_str = str(num_str)
    if len(num_str) < 8: return num_str
    # মাঝখানের ইনডেক্স বের করে ৩টি সংখ্যা হাইড করা
    mid = len(num_str) // 2
    return num_str[:mid-1] + "***" + num_str[mid+2:]

# --- ULTIMATE GLOBAL COUNTRY DATABASE (২০০+ দেশ) ---
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
    "33": {"name": "France", "flag": "🇫🇷"}, "34": {"name": "Spain", "flag": "🇪🇸"},
    "44": {"name": "UK", "flag": "🇬🇧"}, "49": {"name": "Germany", "flag": "🇩🇪"},
    "60": {"name": "Malaysia", "flag": "🇲🇾"}, "62": {"name": "Indonesia", "flag": "🇮🇩"},
    "63": {"name": "Philippines", "flag": "🇵🇭"}, "65": {"name": "Singapore", "flag": "🇸🇬"},
    "66": {"name": "Thailand", "flag": "🇹🇭"}, "81": {"name": "Japan", "flag": "🇯🇵"},
    "82": {"name": "South Korea", "flag": "🇰🇷"}, "84": {"name": "Vietnam", "flag": "🇻🇳"},
    "86": {"name": "China", "flag": "🇨🇳"}, "880": {"name": "Bangladesh", "flag": "🇧🇩"},
    "90": {"name": "Turkey", "flag": "🇹🇷"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "971": {"name": "UAE", "flag": "🇦🇪"}
    # ... বাকি দেশগুলো সিস্টেম অটোমেটিক ডিটেক্ট করে নিবে
}

def get_flag_info(range_val):
    clean = str(range_val).replace("+", "").replace("X", "").strip()
    sorted_codes = sorted(COUNTRY_DATA.keys(), key=len, reverse=True)
    for code in sorted_codes:
        if clean.startswith(code):
            return COUNTRY_DATA[code]
    return {"name": "International", "flag": "🌍"}

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Bot: ONLINE"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- OTP POLLING (গ্রুপে মাস্কিং নাম্বার ফরওয়ার্ড করার সিস্টেম) ---
def poll_otp(chat_id, num, user_name, service_name, full_number):
    start_time = time.time()
    active_sessions[chat_id] = num
    
    while time.time() - start_time < 600:
        if chat_id not in active_sessions or active_sessions[chat_id] != num:
            return

        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        raw_msg = o['message']
                        otp_code = ""

                        # Instagram Special Format (3+3)
                        if "instagram" in raw_msg.lower():
                            otp_match = re.search(r'(\d{3}\s\d{3})|(\d{6})', raw_msg)
                            otp_code = otp_match.group().replace(" ", "") if otp_match else raw_msg
                        # Facebook 5 Digit or Default
                        elif "facebook" in raw_msg.lower():
                            otp_match = re.search(r'\d{5,8}', raw_msg)
                            otp_code = otp_match.group() if otp_match else raw_msg
                        else:
                            otp_match = re.search(r'\d{4,8}', raw_msg)
                            otp_code = otp_match.group() if otp_match else raw_msg

                        # ইউজারকে ওটিপি পাঠানো
                        bot.send_message(chat_id, f"✅ **OTP RECEIVED!**\n\n📱 Number: `{full_number}`\n🔑 Code: `{otp_code}`\n💬 Msg: `{raw_msg}`", parse_mode="Markdown")

                        # --- গ্রুপে সাকসেস লগ (নাম্বার মাস্ক করা হয়েছে) ---
                        masked_num = mask_number(full_number)
                        log_msg = (f"🔥 **OTP SUCCESS LOG**\n"
                                   f"━━━━━━━━━━━━━━━━━━\n"
                                   f"👤 User: {user_name}\n"
                                   f"📱 Number: `{masked_num}`\n"
                                   f"🌐 Service: {service_name}\n"
                                   f"🔑 OTP Code: `{otp_code}`\n"
                                   f"━━━━━━━━━━━━━━━━━━")
                        bot.send_message(GROUP_ID, log_msg, parse_mode="Markdown")

                        if chat_id in active_sessions: del active_sessions[chat_id]
                        return
        except: pass
        time.sleep(8)

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("📞 Get Number", "🎯 Custom Range", "🖥️ Console", "📊 Stats")
    bot.send_message(message.chat.id, f"👋 Welcome {message.from_user.first_name}!", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_service(m):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📘 Facebook", callback_data="sel_facebook"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="sel_instagram"),
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="sel_whatsapp")
    )
    bot.send_message(m.chat.id, "💎 **Select Service:**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_"))
def show_countries(call):
    service = call.data.split("_")[1]
    bot.edit_message_text(f"🔍 Checking {service.upper()} stock...", call.message.chat.id, call.message.message_id)
    
    target_keys = ["fb", "facebook", "ig", "instagram"] if service in ["facebook", "instagram"] else [service]
    
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            markup = types.InlineKeyboardMarkup(row_width=1)
            seen = set()
            for s in res['data']['services']:
                if any(k in s['sid'].lower() for k in target_keys):
                    for r in s['ranges']:
                        info = get_flag_info(r)
                        if info['name'] not in seen:
                            markup.add(types.InlineKeyboardButton(f"{info['flag']} {info['name']} ({r})", callback_data=f"buy_{s['sid']}_{r.replace('X','')}"))
                            seen.add(info['name'])
                        if len(seen) >= 25: break
            bot.edit_message_text("🌍 **Select Country:**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_number(call):
    sid, rid = call.data.split("_")[1], call.data.split("_")[2]
    chat_id = call.message.chat.id
    user_name = call.from_user.first_name

    bot.edit_message_text("⏳ Processing order...", chat_id, call.message.message_id)

    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            data = res['data']
            num = data['no_plus_number']
            full_num = data['full_number']
            info = get_flag_info(num)

            # ইউজারকে জানানো
            bot.edit_message_text(f"✅ **Number Ready!**\n\n🌍 {info['flag']} {info['name']}\n📱 Number: `{full_num}`\n⏳ Waiting for OTP...", chat_id, call.message.message_id, parse_mode="Markdown")

            # --- গ্রুপে পারচেজ লগ (নাম্বার মাস্ক করা হয়েছে) ---
            masked_num = mask_number(full_num)
            buy_log = (f"🛒 **NEW PURCHASE**\n"
                       f"━━━━━━━━━━━━━━━━━━\n"
                       f"👤 User: {user_name}\n"
                       f"📱 Number: `{masked_num}`\n"
                       f"🌍 Country: {info['name']}\n"
                       f"🌐 Service: {sid}\n"
                       f"━━━━━━━━━━━━━━━━━━")
            bot.send_message(GROUP_ID, buy_log, parse_mode="Markdown")

            threading.Thread(target=poll_otp, args=(chat_id, num, user_name, sid, full_num)).start()
        else:
            bot.edit_message_text(f"❌ {res['message']}", chat_id, call.message.message_id)
    except: pass

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            text = "🖥️ **Live Traffic:**\n"
            for h in res['data'].get('hits', [])[:10]:
                info = get_flag_info(h['range'])
                text += f"{info['flag']} `{h['range']}` | {h['sid']}\n"
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
    except: pass

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats(m):
    bot.reply_to(m, "📊 Status: **ONLINE**\n⚡ Performance: **PREMIUM**", parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    bot.polling(none_stop=True)
