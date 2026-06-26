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

# বিশাল দেশ ও পতাকার ডাটাবেস (All Countries)
COUNTRY_DATA = {
    "1": {"name": "USA/Canada", "flag": "🇺🇸"}, "7": {"name": "Russia", "flag": "🇷🇺"},
    "20": {"name": "Egypt", "flag": "🇪🇬"}, "212": {"name": "Morocco", "flag": "🇲🇦"},
    "213": {"name": "Algeria", "flag": "🇩🇿"}, "216": {"name": "Tunisia", "flag": "🇹🇳"},
    "234": {"name": "Nigeria", "flag": "🇳🇬"}, "233": {"name": "Ghana", "flag": "🇬🇭"},
    "27": {"name": "South Africa", "flag": "🇿🇦"}, "30": {"name": "Greece", "flag": "🇬🇷"},
    "31": {"name": "Netherlands", "flag": "🇳🇱"}, "33": {"name": "France", "flag": "🇫🇷"},
    "34": {"name": "Spain", "flag": "🇪🇸"}, "39": {"name": "Italy", "flag": "🇮🇹"},
    "40": {"name": "Romania", "flag": "🇷🇴"}, "44": {"name": "UK", "flag": "🇬🇧"},
    "48": {"name": "Poland", "flag": "🇵🇱"}, "49": {"name": "Germany", "flag": "🇩🇪"},
    "52": {"name": "Mexico", "flag": "🇲🇽"}, "54": {"name": "Argentina", "flag": "🇦🇷"},
    "55": {"name": "Brazil", "flag": "🇧🇷"}, "60": {"name": "Malaysia", "flag": "🇲🇾"},
    "61": {"name": "Australia", "flag": "🇦🇺"}, "62": {"name": "Indonesia", "flag": "🇮🇩"},
    "63": {"name": "Philippines", "flag": "🇵🇭"}, "65": {"name": "Singapore", "flag": "🇸🇬"},
    "66": {"name": "Thailand", "flag": "🇹🇭"}, "81": {"name": "Japan", "flag": "🇯🇵"},
    "82": {"name": "South Korea", "flag": "🇰🇷"}, "84": {"name": "Vietnam", "flag": "🇻🇳"},
    "86": {"name": "China", "flag": "🇨🇳"}, "880": {"name": "Bangladesh", "flag": "🇧🇩"},
    "90": {"name": "Turkey", "flag": "🇹🇷"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "94": {"name": "Sri Lanka", "flag": "🇱🇰"},
    "966": {"name": "Saudi Arabia", "flag": "🇸🇦"}, "971": {"name": "UAE", "flag": "🇦🇪"},
    "98": {"name": "Iran", "flag": "🇮🇷"}, "998": {"name": "Uzbekistan", "flag": "🇺🇿"}
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
        if p in COUNTRY_DATA: return p
    return None

def monitor_otp(chat_id, number, svc):
    """প্রতি ২ সেকেন্ড অন্তর ওটিপি চেক করার ফাস্ট স্ক্যানার"""
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    if str(item['number']) == str(number):
                        msg = item['message']
                        # ফেসবুকের জন্য কোড এক্সট্রাক্ট, অন্যদের জন্য ফুল মেসেজ
                        if "facebook" in svc.lower():
                            match = re.findall(r'\b\d{4,8}\b', msg)
                            code = match[0] if match else "EXTRACTED"
                            final_text = f"✅ *FACEBOOK OTP RECEIVED!*\n\n🔢 OTP CODE: `{code}`\n💬 MESSAGE: `{msg}`\n📱 NUMBER: `{number}`"
                        else:
                            final_text = f"✅ *{svc.upper()} OTP RECEIVED!*\n\n💬 MESSAGE: `{msg}`\n📱 NUMBER: `{number}`"
                        
                        bot.send_message(chat_id, final_text, parse_mode="Markdown")
                        bot.send_message(GROUP_ID, f"🔔 *OTP LOG*\nService: {svc}\nNum: `{number}`\nMsg: {msg}")
                        return
        except: pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📞 Get Number", "💰 Balance")
    welcome_text = f"👋 Hello {message.from_user.first_name}!\n\n🚀 **Sync Mode (Access): ON** 🟢\nটপ ট্রাফিক রেঞ্জ থেকে নম্বর নেওয়ার জন্য নিচে ক্লিক করুন।"
    bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 Get Number")
def service_menu(message):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("📘 FACEBOOK", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("📸 INSTAGRAM", callback_data="svc_Instagram"),
        types.InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "🛠 **সার্ভিস সিলেক্ট করুন (সব দেশ লাইভ):**", parse_mode="Markdown", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # এপিআই থেকে সিঙ্ক মোডে টপ ৫টি রেঞ্জ বের করা
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
                
                # আপনার রিকোয়েস্ট অনুযায়ী প্রথম ৫টি দেশ (Sync Mode)
                top_5 = sync_list[:5]
                for code, rid in top_5:
                    c = COUNTRY_DATA[code]
                    clean_rid = rid.replace("XXX", "")
                    mk.add(types.InlineKeyboardButton(f"⚡ {c['flag']} {c['name']} (SYNC RANGE: {clean_rid})", callback_data=f"buy_{svc}_{clean_rid}"))
                
                if not top_5:
                    bot.send_message(call.message.chat.id, "❌ No Active Ranges Found.")
                else:
                    bot.edit_message_text(f"🚀 *SYNC MODE:* Top 5 {svc} Ranges:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except: pass

    # নম্বর বাই এবং নম্বর চেঞ্জ লজিক
    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "Allocating Number...")
        
        try:
            order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
            if order['meta']['code'] == 200:
                num = order['data']['full_number']
                
                # নম্বর চেঞ্জ এবং গ্রুপ জয়েন বাটন (নম্বরের নিচেই থাকবে)
                mk = types.InlineKeyboardMarkup(row_width=1)
                mk.add(
                    types.InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data=f"buy_{svc}_{rid}"),
                    types.InlineKeyboardButton("📢 JOIN OTP GROUP", url=GROUP_LINK)
                )
                
                bot.edit_message_text(f"✅ *Number Allocated (SYNC)*\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"📞 Number: `{num}`\n"
                                     f"🛠 Service: `{svc}`\n"
                                     f"🕒 Status: Waiting for OTP...\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"💡 ওটিপি না আসলে Change বাটনে ক্লিক করুন।", 
                                     call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                
                Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, f"❌ Error: {order['meta'].get('msg', 'Stock Empty')}")
        except: pass

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
