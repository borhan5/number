import os, requests, telebot, re, time
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAFNySB7QBvzsYz4k_EntbwB_cwWf0QE21E"
VOLTX_KEY = "MQGVM5B5OOW"
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"
WELCOME_IMAGE = "https://telegra.ph/file/0c9a3c988b4c0d9a6c4b1.jpg" 

session = requests.Session()

# পূর্ণাঙ্গ কান্ট্রি ডাটাবেস
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

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "BSNUMBER SYSTEM ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def get_headers(): return {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

def detect_country(range_str):
    for length in [3, 2, 1]:
        p = range_str[:length]
        if p in COUNTRY_DATA:
            return p
    return None

def monitor_otp(chat_id, number, svc):
    """ওটিপি মনিটর করবে এবং ফেসবুক হলে কোড এক্সট্রাক্ট করবে"""
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    if str(item['number']) == str(number):
                        msg = item['message']
                        if "facebook" in svc.lower():
                            # ফেসবুক ওটিপি এক্সট্রাক্ট
                            otp_match = re.findall(r'\b\d{4,8}\b', msg)
                            otp_code = otp_match[0] if otp_match else "EXTRACTED"
                            final_text = f"✅ *FACEBOOK OTP RECEIVED!*\n\n🔢 OTP CODE: `{otp_code}`\n💬 MESSAGE: `{msg}`\n📱 NUMBER: `{number}`"
                        else:
                            # অন্য সব সার্ভিসের জন্য ফুল মেসেজ
                            final_text = f"✅ *{svc.upper()} OTP RECEIVED!*\n\n💬 MESSAGE: `{msg}`\n📱 NUMBER: `{number}`"
                        
                        bot.send_message(chat_id, final_text, parse_mode="Markdown")
                        # গ্রুপে লগ পাঠানো
                        bot.send_message(GROUP_ID, f"🔔 *OTP LOG*\nService: {svc}\nNumber: `{number}`\nMessage: {msg}")
                        return
        except: pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📞 Get Number", "💰 Balance")
    bot.send_photo(message.chat.id, WELCOME_IMAGE, caption="👋 Hello!\nWelcome to **BSNUMBER OTP BOT**.\n\n✅ Sync Mode: **Active** 🟢", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 Get Number")
def get_service(message):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("📘 FACEBOOK", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("📸 INSTAGRAM", callback_data="svc_Instagram"),
        types.InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "🛠 সার্ভিস সিলেক্ট করুন (সব দেশ লাইভ):", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # সার্ভিস রেঞ্জ লোড করা (Sync Mode 1-5)
    if call.data.startswith("svc_"):
        svc = call.data.split("_")[1]
        try:
            res = session.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                mk = types.InlineKeyboardMarkup(row_width=1)
                sync_list = []
                for s in res['data']['services']:
                    if s['sid'].lower() == svc.lower():
                        for r in s['ranges']:
                            c_code = detect_country(r)
                            if c_code: sync_list.append((c_code, r))
                
                # প্রথম ৫টি টপ রেঞ্জ
                top_5 = sync_list[:5]
                for code, rid in top_5:
                    c = COUNTRY_DATA[code]
                    clean_rid = rid.replace("XXX", "")
                    mk.add(types.InlineKeyboardButton(f"⚡ {c['flag']} {c['name']} (Traffic Range)", callback_data=f"buy_{svc}_{clean_rid}"))
                
                bot.edit_message_text(f"🚀 *SYNC MODE:* Top 5 {svc} Active Ranges:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except: pass

    # নম্বর বাই এবং নম্বর চেঞ্জ লজিক
    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "Allocating Fast Number...")
        
        try:
            order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
            if order['meta']['code'] == 200:
                num = order['data']['full_number']
                
                # নম্বর চেঞ্জ এবং গ্রুপ জয়েন বাটন
                mk = types.InlineKeyboardMarkup(row_width=1)
                mk.add(
                    types.InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data=f"buy_{svc}_{rid}"),
                    types.InlineKeyboardButton("📢 JOIN OTP GROUP", url=GROUP_LINK)
                )
                
                bot.edit_message_text(f"✅ *Number Allocated*\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"📞 Number: `{num}`\n"
                                     f"🛠 Service: `{svc}`\n"
                                     f"🕒 Status: Waiting for OTP...\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"💡 ওটিপি না আসলে Change এ ক্লিক করুন।", 
                                     call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                
                Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, "❌ Error: Stock Empty or No Balance.")
        except: pass

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
