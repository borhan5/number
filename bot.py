import os, requests, telebot, re, time
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAEpzTRZtGS-K3MBrVC2sT05r5sTb_n7mu8"
VOLTX_KEY = "MQGVM5B5OOW"
ADMIN_ID = 8250359361 
GROUP_ID = -1003968881110 
CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl" 
METHOD_LINK = "https://t.me/earntrick_BS"       

BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"
WELCOME_IMAGE = "https://telegra.ph/file/0c9a3c988b4c0d9a6c4b1.jpg" 

session = requests.Session()
bot = telebot.TeleBot(API_TOKEN)

LIVE_HITTING_RANGES = set()

# --- BACKGROUND CONSOLE SCANNER ---
def scan_public_console():
    while True:
        try:
            headers = {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}
            res = session.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    num = str(item.get('number', ''))
                    r_val = num.replace('+', '')[:6] # প্লাস সরিয়ে রেঞ্জ নেওয়া
                    if len(r_val) >= 5:
                        LIVE_HITTING_RANGES.add(r_val)
                if len(LIVE_HITTING_RANGES) > 40:
                    LIVE_HITTING_RANGES.clear()
        except: pass
        time.sleep(20)

def save_user(user_id):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f: f.write("")
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open("users.txt", "a") as f: f.write(f"{user_id}\n")

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
    "880": {"name": "Bangladesh", "flag": "🇧🇩"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "62": {"name": "Indonesia", "flag": "🇮🇩"},
    "84": {"name": "Vietnam", "flag": "🇻🇳"}, "63": {"name": "Philippines", "flag": "🇵🇭"},
    "90": {"name": "Turkey", "flag": "🇹🇷"}, "966": {"name": "Saudi Arabia", "flag": "🇸🇦"}
}

def get_headers(): return {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

def detect_country(range_str):
    for length in [3, 2, 1]:
        p = range_str[:length]
        if p in COUNTRY_DATA: return p
    return None

def monitor_otp(chat_id, number, svc):
    start_time = time.time()
    target_num = re.sub(r'\D', '', str(number))
    while time.time() - start_time < 600:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    found_num = re.sub(r'\D', '', str(item['number']))
                    if target_num == found_num:
                        original_msg = item['message']
                        masked_msg = re.sub(r'\d{4,8}', '******', original_msg)
                        
                        # ওটিপি প্রাপ্তির মেসেজেও নম্বর ফরম্যাট ঠিক করা হয়েছে
                        formatted_num = "+" + str(number).lstrip('+')
                        bot.send_message(chat_id, f"🎊 *OTP RECEIVED*\n━━━━━━━━━━\n📱 `{formatted_num}`\n📩 `{original_msg}`", parse_mode="Markdown")
                        
                        hidden_num = formatted_num[:6] + "xxx" + formatted_num[-2:]
                        bot.send_message(GROUP_ID, f"🔔 *[OTP LOG]*\nSvc: {svc}\nNum: `{hidden_num}`\nMsg: {masked_msg}")
                        return
        except: pass
        time.sleep(3)

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    save_user(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🚀 Get Number"), types.KeyboardButton("💎 My Balance"), types.KeyboardButton("📖 Method"))
    bot.send_message(message.chat.id, "👋 *Welcome to Premium Sync Bot*", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "📖 Method")
def method_handler(message):
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(types.InlineKeyboardButton("📢 Join Main Channel", url=CHANNEL_LINK), types.InlineKeyboardButton("📖 Join Method Group", url=METHOD_LINK))
    bot.send_message(message.chat.id, "📑 *আমাদের সাপোর্ট এবং মেথড লিংক সমূহ:*", reply_markup=mk, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🚀 Get Number")
def service_menu(message):
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton("🔥 LIVE NEW FB (Hits Only)", callback_data="svc_LiveFB"),
        types.InlineKeyboardButton("📘 FACEBOOK / 📸 INSTAGRAM", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("💬 WHATSAPP BUSINESS", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "🛠 *সার্ভিস সিলেক্ট করুন:*", reply_markup=mk, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data.startswith("svc_"):
        raw_svc = call.data.split("_")[1]
        svc = "Facebook" if raw_svc == "LiveFB" else raw_svc
        
        try:
            res = session.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                mk = types.InlineKeyboardMarkup(row_width=2)
                for s in res['data']['services']:
                    if s['sid'].lower() == svc.lower():
                        for r in s['ranges']:
                            clean_r = r.replace("XXX", "").replace('+', '')
                            prefix = clean_r[:6]
                            is_hit = prefix in LIVE_HITTING_RANGES
                            if raw_svc == "LiveFB" and not is_hit: continue
                            
                            icon = "🔥" if is_hit else "✅"
                            c_code = detect_country(clean_r)
                            flag = COUNTRY_DATA[c_code]['flag'] if c_code in COUNTRY_DATA else "🌍"
                            mk.add(types.InlineKeyboardButton(f"{icon} {flag} {clean_r}", callback_data=f"buy_{svc}_{clean_r}"))
                
                msg = "🔥 *Live Hitting Ranges Only:*" if raw_svc == "LiveFB" else f"🌍 *{svc} Available Stock*"
                bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except: pass

    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ Allocating...")
        try:
            order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
            if order.get('meta', {}).get('code') == 200:
                num = order['data']['full_number']
                
                # নম্বর থেকে অতিরিক্ত প্লাস পরিষ্কার করে মাত্র একটি প্লাস রাখা হলো
                formatted_num = "+" + str(num).lstrip('+')
                
                mk = types.InlineKeyboardMarkup(row_width=2)
                mk.add(
                    types.InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data=f"svc_{svc}"),
                    types.InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK),
                    types.InlineKeyboardButton("📖 METHOD GROUP", url=METHOD_LINK)
                )
                
                order_text = (
                    f"✅ *NUMBER READY*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📞 **Number:** `{formatted_num}`\n"
                    f"⏳ **Status:** `Waiting for OTP...` 🌀\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━"
                )
                
                bot.edit_message_text(order_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                Thread(target=monitor_otp, args=(call.message.chat.id, formatted_num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, "❌ No Stock for this range.")
        except: pass

@bot.message_handler(func=lambda message: message.text == "💎 My Balance")
def bal_h(message):
    try:
        res = session.get(f"{BASE_URL}/user-balance", headers=get_headers()).json()
        bot.send_message(message.chat.id, f"💰 *Balance:* `{res['data']['balance']} BDT`", parse_mode="Markdown")
    except: pass

@bot.message_handler(commands=['broadcast'])
def bc_h(message):
    if message.from_user.id == ADMIN_ID:
        txt = message.text.replace("/broadcast ", "")
        with open("users.txt", "r") as f: users = f.read().splitlines()
        for u in users:
            try: bot.send_message(u, txt)
            except: pass
        bot.reply_to(message, "✅ Broadcast Done!")

if __name__ == "__main__":
    Thread(target=scan_public_console).start()
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot.infinity_polling(skip_pending=True)
