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

# COUNTRY DATA
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
def home(): return "BOT STATUS: ACTIVE"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive(): Thread(target=run).start()

def get_headers(): return {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

def detect_country(range_str):
    for length in [3, 2, 1]:
        p = range_str[:length]
        if p in COUNTRY_DATA: return p
    return None

def monitor_otp(chat_id, number, svc):
    start_time = time.time()
    target_num = re.sub(r'\D', '', str(number))
    
    while time.time() - start_time < 3600: # ১ ঘণ্টা মেয়াদ
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data'].get('otps', []):
                    found_num = re.sub(r'\D', '', str(item['number']))
                    
                    if target_num == found_num:
                        msg = item['message']
                        display_svc = "Facebook/Instagram" if svc == "Facebook" else svc
                        
                        final_text = (
                            f"🎊 *CONGRATULATIONS! OTP RECEIVED* 🎊\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"💠 *SERVICE:* `{display_svc.upper()}`\n"
                            f"📱 *NUMBER:* `{number}`\n"
                            f"📩 *MESSAGE:* `{msg}`\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"✅ *Verification Successful!*"
                        )
                        bot.send_message(chat_id, final_text, parse_mode="Markdown")
                        
                        num_str = str(number)
                        length = len(num_str)
                        masked_num = num_str[:3] + "***" + num_str[-3:] if length > 6 else "***" + num_str[-2:]
                            
                        bot.send_message(GROUP_ID, f"🔔 *[OTP LOG]*\nSvc: {svc}\nNum: `{masked_num}`\nMsg: {msg}")
                        return
        except: pass
        time.sleep(3)

# --- মূল হ্যান্ডলার ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🚀 Get Number"), 
        types.KeyboardButton("💎 My Balance"),
        types.KeyboardButton("📦 View Stock") # নতুন বাটন
    )
    
    welcome_text = (
        f"👋 *Welcome to Premium OTP Bot*\n\n"
        f"💠 *Status:* `Active` 🟢\n"
        f"💠 *Timeout:* `1 Hour` ⏳\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"নিচের মেনু থেকে সার্ভিস সিলেক্ট করুন।"
    )
    try:
        bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "📦 View Stock")
def stock_check(message):
    wait_msg = bot.send_message(message.chat.id, "📊 *Fetching Live Stock...*", parse_mode="Markdown")
    try:
        res = session.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
        if res.get('meta', {}).get('code') == 200:
            stock_info = "📦 *CURRENT LIVE STOCK*\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for s in res['data']['services']:
                svc_name = "FB/Insta" if s['sid'] == "Facebook" else s['sid']
                stock_info += f"🔹 *{svc_name.upper()}*:\n"
                
                # দেশ ভিত্তিক রেঞ্জ গণনা
                countries_found = {}
                for r in s['ranges']:
                    c_code = detect_country(r)
                    if c_code:
                        c_name = COUNTRY_DATA[c_code]['name']
                        c_flag = COUNTRY_DATA[c_code]['flag']
                        key = f"{c_flag} {c_name}"
                        countries_found[key] = countries_found.get(key, 0) + 1
                
                if not countries_found:
                    stock_info += " ❌ No Stock\n"
                else:
                    for c, count in countries_found.items():
                        stock_info += f" ├ {c}: `{count} Ranges` ✅\n"
                stock_info += "━━━━━━━━━━━━━━━━━━━━━━\n"
            
            bot.edit_message_text(stock_info, message.chat.id, wait_msg.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ স্টক ডাটা পাওয়া যায়নি।", message.chat.id, wait_msg.message_id)
    except:
        bot.edit_message_text("❌ সার্ভার এরর।", message.chat.id, wait_msg.message_id)

@bot.message_handler(func=lambda message: message.text in ["💎 My Balance", "💰 Balance"])
def balance_handler(message):
    try:
        res = session.get(f"{BASE_URL}/user-balance", headers=get_headers()).json()
        if res.get('meta', {}).get('code') == 200:
            bal = res['data']['balance']
            bal_text = f"💳 *WALLET INFO*\n━━━━━━━━━━━━━\n💰 *Balance:* `{bal} BDT`\n━━━━━━━━━━━━━"
            bot.send_message(message.chat.id, bal_text, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "❌ এরর।")

@bot.message_handler(func=lambda message: message.text in ["🚀 Get Number", "📞 Get Number"])
def service_menu(message):
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton("📘 FACEBOOK / 📸 INSTAGRAM", callback_data="svc_Facebook"),
        types.InlineKeyboardButton("💬 WHATSAPP BUSINESS", callback_data="svc_WhatsApp")
    )
    bot.send_message(message.chat.id, "🛠 *সার্ভিস সিলেক্ট করুন:*", reply_markup=mk, parse_mode="Markdown")

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
                
                if not sync_list:
                    bot.answer_callback_query(call.id, "❌ No stock!")
                    return

                for code, rid in sync_list[:15]:
                    c = COUNTRY_DATA[code]
                    clean_rid = rid.replace("XXX", "")
                    mk.add(types.InlineKeyboardButton(f"{c['flag']} {c['name']} ({clean_rid})", callback_data=f"buy_{svc}_{clean_rid}"))
                
                bot.edit_message_text(f"🌍 *{svc} Stock List*", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except:
            bot.answer_callback_query(call.id, "Error fetching data.")

    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "⚡ Allocating...")
        try:
            order = session.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
            if order.get('meta', {}).get('code') == 200:
                num = order['data']['full_number']
                order_text = (
                    f"✅ *NUMBER ALLOCATED*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📞 *Number:* `{num}`\n"
                    f"🛠 *Service:* `{svc}`\n"
                    f"⏳ *Status:* `Waiting (1 Hour)` 🌀\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━"
                )
                mk = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📢 JOIN CHANNEL", url=GROUP_LINK))
                bot.edit_message_text(order_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, "❌ No Balance or Stock Empty.")
        except:
            bot.send_message(call.message.chat.id, "❌ Server Error.")

if __name__ == "__main__":
    keep_alive()
    bot.set_my_commands([types.BotCommand("start", "মূল মেনু")])
    print("--- Premium Bot Live with Stock System ---")
    bot.infinity_polling(skip_pending=True)
