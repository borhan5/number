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

# আপনার দেওয়া সব দেশের লিস্ট (Full Database)
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
    "34": {"name": "Spain", "flag": "🇪🇸"}, "39": {"name": "Italy", "flag": "🇮🇹"},
    "40": {"name": "Romania", "flag": "🇷🇴"}, "41": {"name": "Switzerland", "flag": "🇨🇭"},
    "43": {"name": "Austria", "flag": "🇦🇹"}, "44": {"name": "UK", "flag": "🇬🇧"},
    "45": {"name": "Denmark", "flag": "🇩🇰"}, "46": {"name": "Sweden", "flag": "🇸🇪"},
    "47": {"name": "Norway", "flag": "🇳🇴"}, "48": {"name": "Poland", "flag": "🇵🇱"},
    "49": {"name": "Germany", "flag": "🇩🇪"}, "51": {"name": "Peru", "flag": "🇵🇪"},
    "52": {"name": "Mexico", "flag": "🇲🇽"}, "54": {"name": "Argentina", "flag": "🇦🇷"},
    "55": {"name": "Brazil", "flag": "🇧🇷"}, "60": {"name": "Malaysia", "flag": "🇲🇾"},
    "61": {"name": "Australia", "flag": "🇦🇺"}, "62": {"name": "Indonesia", "flag": "🇮🇩"},
    "63": {"name": "Philippines", "flag": "🇵🇭"}, "65": {"name": "Singapore", "flag": "🇸🇬"},
    "66": {"name": "Thailand", "flag": "🇹🇭"}, "81": {"name": "Japan", "flag": "🇯🇵"},
    "82": {"name": "South Korea", "flag": "🇰🇷"}, "84": {"name": "Vietnam", "flag": "🇻🇳"},
    "86": {"name": "China", "flag": "🇨🇳"}, "880": {"name": "Bangladesh", "flag": "🇧🇩"},
    "90": {"name": "Turkey", "flag": "🇹🇷"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "93": {"name": "Afghanistan", "flag": "🇦🇫"},
    "94": {"name": "Sri Lanka", "flag": "🇱🇰"}, "95": {"name": "Myanmar", "flag": "🇲🇲"},
    "966": {"name": "Saudi Arabia", "flag": "🇸🇦"}, "971": {"name": "UAE", "flag": "🇦🇪"},
    "977": {"name": "Nepal", "flag": "🇳🇵"}, "998": {"name": "Uzbekistan", "flag": "🇺🇿"}
}

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "SYSTEM ONLINE"
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
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    if item['number'] == str(number):
                        msg = item['message']
                        if "facebook" in svc.lower():
                            otp_code = re.findall(r'\b\d{4,8}\b', msg)
                            code = otp_code[0] if otp_code else "CHECK MSG"
                            final_text = f"✅ *FACEBOOK OTP*\n\n🔢 CODE: `{code}`\n💬 MSG: `{msg}`"
                        else:
                            final_text = f"✅ *{svc.upper()} OTP*\n\n💬 MESSAGE: `{msg}`"
                        
                        bot.send_message(chat_id, final_text, parse_mode="Markdown")
                        bot.send_message(GROUP_ID, f"🔔 *OTP RECEIVED*\nService: {svc}\nNum: {number}\nMsg: {msg}")
                        return
        except: pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📞 Get Number", "💰 Balance")
    bot.send_photo(message.chat.id, WELCOME_IMAGE, caption="👋 Welcome to BSNUMBER!\nAccess Sync Mode is **ON** 🟢", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 Get Number")
def get_num_menu(message):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("📘 FACEBOOK", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("📸 INSTAGRAM", callback_data="svc_Instagram"),
        types.InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "Select Service:", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data.startswith("svc_"):
        svc = call.data.split("_")[1]
        try:
            res = session.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                mk = types.InlineKeyboardMarkup(row_width=1)
                sync_list = []
                
                # এপিআই থেকে প্রাপ্ত সব রেঞ্জ চেক করা
                for s in res['data']['services']:
                    if s['sid'].lower() == svc.lower():
                        for r in s['ranges']:
                            c_code = detect_country(r)
                            if c_code:
                                sync_list.append((c_code, r))

                # আপনার রিকোয়েস্ট অনুযায়ী প্রথম ১-৫টি টপ রেঞ্জ দেখানো
                top_5 = sync_list[:5]

                for code, rid in top_5:
                    c = COUNTRY_DATA[code]
                    clean_rid = rid.replace("XXX", "")
                    mk.add(types.InlineKeyboardButton(f"🟢 {c['flag']} {c['name']} (Range: {clean_rid})", callback_data=f"buy_{svc}_{clean_rid}"))
                
                if not top_5:
                    bot.send_message(call.message.chat.id, "❌ No Traffic Found.")
                else:
                    bot.edit_message_text(f"🚀 *Sync Mode Active* (Top 5 {svc} Ranges):", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except: pass

    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "Processing Order...")
        order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
        if order['meta']['code'] == 200:
            num = order['data']['full_number']
            bot.edit_message_text(f"✅ *Number Allocated*\n📞 Number: `{num}`\n🛠 Service: `{svc}`\n⏳ Waiting for OTP...", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
            Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
        else:
            bot.send_message(call.message.chat.id, "❌ Error: Stock Empty or No Balance.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
