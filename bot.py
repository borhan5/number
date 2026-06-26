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

# সারা বিশ্বের দেশের লিস্ট (বড় ডাটাবেস)
COUNTRY_DATA = {
    "1": {"n": "USA/Canada", "f": "🇺🇸"}, "7": {"n": "Russia/Kazakhstan", "f": "🇷🇺"},
    "20": {"n": "Egypt", "f": "🇪🇬"}, "212": {"n": "Morocco", "f": "🇲🇦"},
    "213": {"n": "Algeria", "f": "🇩🇿"}, "216": {"n": "Tunisia", "f": "🇹🇳"},
    "221": {"n": "Senegal", "f": "🇸🇳"}, "223": {"n": "Mali", "f": "🇲🇱"},
    "225": {"n": "Ivory Coast", "f": "🇨🇮"}, "228": {"n": "Togo", "f": "🇹🇬"},
    "232": {"n": "Sierra Leone", "f": "🇸🇱"}, "234": {"n": "Nigeria", "f": "🇳🇬"},
    "243": {"n": "DR Congo", "f": "🇨🇩"}, "244": {"n": "Angola", "f": "🇦🇴"},
    "254": {"n": "Kenya", "f": "🇰🇪"}, "255": {"n": "Tanzania", "f": "🇹🇿"},
    "261": {"n": "Madagascar", "f": "🇲🇬"}, "33": {"n": "France", "f": "🇫🇷"},
    "44": {"n": "UK", "f": "🇬🇧"}, "60": {"n": "Malaysia", "f": "🇲🇾"},
    "62": {"n": "Indonesia", "f": "🇮🇩"}, "63": {"n": "Philippines", "f": "🇵🇭"},
    "66": {"n": "Thailand", "f": "🇹🇭"}, "84": {"n": "Vietnam", "f": "🇻🇳"},
    "880": {"n": "Bangladesh", "f": "🇧🇩"}, "91": {"n": "India", "f": "🇮🇳"},
    "92": {"n": "Pakistan", "f": "🇵🇰"}, "998": {"n": "Uzbekistan", "f": "🇺🇿"}
}

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "BSNUMBER UI ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def get_headers(): return {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

def get_country_info(number):
    num_str = str(number)
    for length in [3, 2, 1]:
        code = num_str[:length]
        if code in COUNTRY_DATA:
            return COUNTRY_DATA[code]['f'], COUNTRY_DATA[code]['n']
    return "🌍", "Other Country"

def get_live_ranges(service_name):
    active_ranges = []
    try:
        res = requests.get(f"{BASE_URL}/success-otp", headers=get_headers()).json()
        if res.get('meta', {}).get('code') == 200:
            for item in res['data']['otps']:
                if service_name.lower() in item['message'].lower() or service_name.lower() in item['app_name'].lower():
                    num = str(item['number'])
                    range_id = num[:-3] 
                    flag, c_name = get_country_info(num)
                    data = {"rid": range_id, "flag": flag, "country": c_name}
                    if data not in active_ranges:
                        active_ranges.append(data)
    except: pass
    return active_ranges[:12]

def monitor_otp(chat_id, number, svc):
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data']['otps']:
                    if str(item['number']) == str(number):
                        msg = item['message']
                        if "facebook" in svc.lower():
                            match = re.search(r'\b\d{6}\b', msg)
                            otp = match.group(0) if match else "Check Full Msg"
                        else:
                            otp = "See Message Below"
                        
                        bot.send_message(chat_id, f"✅ *{svc.upper()} OTP RECEIVED!*\n\n📱 Number: `{number}`\n🔢 OTP: `{otp}`\n\n💬 Message: `{msg}`", parse_mode="Markdown")
                        return
        except: pass
        time.sleep(10)

# --- UI HANDLERS ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    # মেইন কিবোর্ড (আপনার স্ক্রিনশটের মতো)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("📂 Stock Number"),
        types.KeyboardButton("🔐 Get 2FA"), types.KeyboardButton("📟 Extract OTP"),
        types.KeyboardButton("📊 Stats"), types.KeyboardButton("💰 Balance")
    )
    
    welcome_text = (
        f"🌌 *BSNUMBER* | 👋 Hello, {message.from_user.first_name}!\n"
        f"✅ *Select a service from the buttons below:*"
    )
    
    try:
        bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_menu_clicks(message):
    if message.text == "📞 Get Number":
        mk = types.InlineKeyboardMarkup(row_width=1)
        mk.add(
            types.InlineKeyboardButton("📘 FACEBOOK", callback_data="get_Facebook"),
            types.InlineKeyboardButton("📸 INSTAGRAM", callback_data="get_Instagram"),
            types.InlineKeyboardButton("💬 WHATSAPP", callback_data="get_WhatsApp")
        )
        bot.send_message(message.chat.id, "🛠 *সার্ভিস সিলেক্ট করুন (Live Console):*", parse_mode="Markdown", reply_markup=mk)
    
    elif message.text == "💰 Balance":
        bot.send_message(message.chat.id, "💳 *আপনার ব্যালেন্স মেইন কনসোলে চেক করুন।*", parse_mode="Markdown")
    
    elif message.text == "📊 Stats":
        bot.send_message(message.chat.id, "📈 *সিস্টেম স্ট্যাটাস:* ১০০% কার্যকর।", parse_mode="Markdown")
    
    else:
        bot.send_message(message.chat.id, f"⚠️ '{message.text}' ফিচারটি শীঘ্রই যোগ করা হবে।")

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def show_ranges(call):
    svc = call.data.split("_")[1]
    bot.edit_message_text(f"📡 *{svc}* এর জন্য লাইভ রেঞ্জ খোঁজা হচ্ছে...", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    
    ranges = get_live_ranges(svc)
    if not ranges:
        bot.send_message(call.message.chat.id, "❌ বর্তমানে কোনো একটিভ রেঞ্জ পাওয়া যায়নি।")
        return

    mk = types.InlineKeyboardMarkup(row_width=1)
    for r in ranges:
        mk.add(types.InlineKeyboardButton(f"{r['flag']} {r['country']} | {r['rid']}XXX", callback_data=f"buy_{svc}_{r['rid']}"))
    
    bot.edit_message_text(f"🌍 *Available Live Ranges for {svc}:*", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_buy(call):
    _, svc, rid = call.data.split("_")
    bot.answer_callback_query(call.id, "অর্ডার প্রসেস হচ্ছে...")
    
    res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=get_headers()).json()
    if res.get('meta', {}).get('code') == 200:
        num = res['data']['full_number']
        bot.edit_message_text(f"✅ *Number Allocated!*\n\n📞 Number: `{num}`\n🌍 Range: `{rid}`\n\n⏳ ওটিপি আসার জন্য অপেক্ষা করুন...", 
                              call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
    else:
        bot.send_message(call.message.chat.id, "❌ নম্বর পাওয়া যায়নি। ব্যালেন্স চেক করুন।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
