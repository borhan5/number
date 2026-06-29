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

# --- সম্পূর্ণ কান্ট্রি লিস্ট (৬১+ দেশ) ---
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

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🚀 Get Number"), types.KeyboardButton("💎 My Balance"))
    bot.send_message(message.chat.id, "👋 *Welcome to New FB Console Bot*\n\nএটি সরাসরি লাইভ কনসোল থেকে `➜<#>` ফরম্যাটের কোড আসা রেঞ্জগুলো খুঁজে বের করবে।", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🚀 Get Number")
def service_menu(message):
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton("🆕 NEW FACEBOOK (Live Hits) 🔥", callback_data="svc_LiveFB"),
        types.InlineKeyboardButton("📘 FACEBOOK (Normal)", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("💬 WHATSAPP BUSINESS", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "🛠 *সার্ভিস সিলেক্ট করুন:*", reply_markup=mk, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # --- স্পেশাল নিউ ফেসবুক লজিক (➜<#> ফিল্টার) ---
    if call.data == "svc_LiveFB":
        bot.answer_callback_query(call.id, "Filtering ➜<#> Format...")
        try:
            res = session.get(f"{BASE_URL}/console", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                hits = res['data'].get('hits', [])
                fresh_ranges = []
                seen = set()
                
                for hit in hits:
                    msg = hit.get('message', '')
                    # এখানে আপনার দেওয়া সেই নির্দিষ্ট ফরম্যাটটি চেক করা হচ্ছে
                    if "➜<#>" in msg and "is your Facebook code" in msg:
                        r = hit['range']
                        if r not in seen:
                            fresh_ranges.append(r)
                            seen.add(r)
                
                if not fresh_ranges:
                    bot.send_message(call.message.chat.id, "❌ বর্তমানে কনসোলে `➜<#>` ফরম্যাটের কোনো ফেসবুক হিট নেই।")
                    return

                mk = types.InlineKeyboardMarkup(row_width=1)
                for r in fresh_ranges[:12]:
                    c_code = detect_country(r)
                    c = COUNTRY_DATA.get(c_code, {"name": "Unknown", "flag": "🌍"})
                    clean_rid = r.replace("XXX", "")
                    mk.add(types.InlineKeyboardButton(f"🔥 {c['flag']} {c['name']} (Range: {clean_rid})", callback_data=f"buy_Facebook_{clean_rid}"))
                
                bot.edit_message_text("✅ *NEW FB SPECIAL RANGES*\nএই রেঞ্জগুলোতে বর্তমানে `➜<#>` কোড আসছে:", 
                                     call.message.chat.id, call.message.message_id, reply_markup=mk, parse_mode="Markdown")
        except: pass

    # --- অন্যান্য সার্ভিস ---
    elif call.data.startswith("svc_"):
        svc = call.data.split("_")[1]
        try:
            res = session.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                mk = types.InlineKeyboardMarkup(row_width=1)
                for s in res['data']['services']:
                    if s['sid'].lower() == svc.lower():
                        for r in s['ranges'][:15]:
                            c_code = detect_country(r)
                            c = COUNTRY_DATA.get(c_code, {"name": "Unknown", "flag": "🌍"})
                            clean_rid = r.replace("XXX", "")
                            mk.add(types.InlineKeyboardButton(f"{c['flag']} {c['name']} ({clean_rid})", callback_data=f"buy_{svc}_{clean_rid}"))
                bot.edit_message_text(f"🌍 *{svc} Stock*", call.message.chat.id, call.message.message_id, reply_markup=mk, parse_mode="Markdown")
        except: pass

    # --- নাম্বার কেনা ---
    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "Allocating...")
        try:
            order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
            if order.get('meta', {}).get('code') == 200:
                num = order['data']['full_number']
                bot.send_message(call.message.chat.id, f"✅ *Number:* `{num}`\n🛠 *Svc:* {svc}\n🌀 *Status:* Waiting for OTP...", parse_mode="Markdown")
            else:
                bot.send_message(call.message.chat.id, "❌ Stock Out!")
        except: pass

# --- SERVER ---
app = Flask('')
@app.route('/')
def home(): return "RUNNING"
def run(): app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
