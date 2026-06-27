import os, requests, telebot, re, time
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAEpzTRZtGS-K3MBrVC2sT05r5sTb_n7mu8"
VOLTX_KEY = "MQGVM5B5OOW"
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"
WELCOME_IMAGE = "https://telegra.ph/file/0c9a3c988b4c0d9a6c4b1.jpg" 

session = requests.Session()

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
def home(): return "OTP SYSTEM MASKED LOG ACTIVE"
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
    """ওটিপি মনিটর করবে এবং ম্যাচ করলে ফুল মেসেজ পাঠাবে"""
    start_time = time.time()
    target_num = re.sub(r'\D', '', str(number))
    
    while time.time() - start_time < 600:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    found_num = re.sub(r'\D', '', str(item['number']))
                    
                    if target_num == found_num:
                        msg = item['message']
                        display_svc = "Facebook/Instagram" if svc == "Facebook" else svc
                        
                        # ইউজারের জন্য ফুল মেসেজ
                        final_text = f"✅ *{display_svc.upper()} OTP RECEIVED!*\n\n💬 MESSAGE: `{msg}`\n📱 NUMBER: `{number}`"
                        bot.send_message(chat_id, final_text, parse_mode="Markdown")
                        
                        # গ্রুপের জন্য নম্বর মাস্কিং লজিক
                        num_str = str(number)
                        length = len(num_str)
                        if length > 5:
                            mid = length // 2
                            masked_num = num_str[:mid-1] + "***" + num_str[mid+2:]
                        else:
                            masked_num = "***" + num_str[-2:] if length > 2 else "***"
                            
                        bot.send_message(GROUP_ID, f"🔔 *OTP LOG*\nSvc: {svc}\nNum: `{masked_num}`\nMsg: {msg}")
                        return
        except: pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📞 Get Number", "💰 Balance")
    try:
        bot.send_photo(message.chat.id, WELCOME_IMAGE, caption="👋 Hello!\n**Sync Mode** (Facebook/Instagram) চালু আছে।", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "👋 Hello!\n**Sync Mode** (Facebook/Instagram) চালু আছে।", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 Get Number")
def service_menu(message):
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton("📘 FACEBOOK / 📸 INSTAGRAM", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "🛠 সার্ভিস সিলেক্ট করুন:", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
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
                
                top_ranges = sync_list[:10] 
                for code, rid in top_ranges:
                    c = COUNTRY_DATA[code]
                    clean_rid = rid.replace("XXX", "")
                    mk.add(types.InlineKeyboardButton(f"⚡ {c['flag']} {c['name']} (Range: {clean_rid})", callback_data=f"buy_{svc}_{clean_rid}"))
                
                display_svc = "Facebook/Instagram" if svc == "Facebook" else svc
                bot.edit_message_text(f"🚀 *SYNC MODE:* {display_svc} Available Ranges:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except:
            bot.answer_callback_query(call.id, "Error fetching ranges.")

    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "Allocating Number...")
        
        try:
            order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
            if order.get('meta', {}).get('code') == 200:
                num = order['data']['full_number']
                display_svc = "Facebook/Instagram" if svc == "Facebook" else svc
                
                mk = types.InlineKeyboardMarkup()
                mk.add(types.InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data=f"buy_{svc}_{rid}"))
                mk.add(types.InlineKeyboardButton("📢 JOIN GROUP", url=GROUP_LINK))
                
                bot.edit_message_text(f"✅ *Number Allocated*\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"📞 Number: `{num}`\n"
                                     f"🛠 Service: `{display_svc}`\n"
                                     f"⏳ Status: Waiting for OTP...\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"💡 ওটিপি না আসলে 'Change Number' ক্লিক করুন।", 
                                     call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                
                Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, "❌ Error: Stock empty or No Balance.")
        except:
            bot.send_message(call.message.chat.id, "❌ Server Error.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
