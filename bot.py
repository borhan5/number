import os
import telebot
import requests
import threading
import time
from telebot import types
from flask import Flask

# --- RENDER FIX (এই অংশটুকু ছাড়া Render-এ বট চলবে না) ---
app = Flask('')

@app.route('/')
def home():
    return "BSNUMBER Bot is Live!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web_server)
    t.start()
# ---------------------------------------------------

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAEysnwZYlyOKPTG2onlNs6KZesFoTQzCr4"
VOLTX_KEY = "MQGVM5B5OOW"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

ADMIN_ID = 8250359361
ADMIN_HANDLE = "@BORHANSB" 

METHOD_GROUP_ID = -1001859871146 
METHOD_LINK = "https://t.me/earntrick_BS" 
CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(API_TOKEN)
headers = {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

# --- ১০০% সবগুলো দেশের লিস্ট (আপনার অরিজিনাল ডাটাবেজ) ---
COUNTRY_DB = {
    "880": {"n": "Bangladesh", "f": "🇧🇩"}, "91": {"n": "India", "f": "🇮🇳"}, "1": {"n": "USA/Canada", "f": "🇺🇸"},
    "44": {"n": "UK", "f": "🇬🇧"}, "7": {"n": "Russia", "f": "🇷🇺"}, "62": {"n": "Indonesia", "f": "🇮🇩"},
    "84": {"n": "Vietnam", "f": "🇻🇳"}, "63": {"n": "Philippines", "f": "🇵🇭"}, "234": {"n": "Nigeria", "f": "🇳🇬"},
    "225": {"n": "Ivory Coast", "f": "🇨🇮"}, "224": {"n": "Guinea", "f": "🇬🇳"}, "261": {"n": "Madagascar", "f": "🇲🇬"},
    "236": {"n": "CAR", "f": "🇨🇫"}, "229": {"n": "Benin", "f": "🇧🇯"}, "223": {"n": "Mali", "f": "🇲🇱"},
    "251": {"n": "Ethiopia", "f": "🇪🇹"}, "255": {"n": "Tanzania", "f": "🇹🇿"}, "20": {"n": "Egypt", "f": "🇪🇬"},
    "212": {"n": "Morocco", "f": "🇲🇦"}, "27": {"n": "South Africa", "f": "🇿🇦"}, "55": {"n": "Brazil", "f": "🇧🇷"},
    "60": {"n": "Malaysia", "f": "🇲🇾"}, "66": {"n": "Thailand", "f": "🇹🇭"}, "92": {"n": "Pakistan", "f": "🇵🇰"},
    "994": {"n": "Azerbaijan", "f": "🇦🇿"}, "90": {"n": "Turkey", "f": "🇹🇷"}, "49": {"n": "Germany", "f": "🇩🇪"},
    "33": {"n": "France", "f": "🇫🇷"}, "39": {"n": "Italy", "f": "🇮🇹"}, "34": {"n": "Spain", "f": "🇪🇸"},
    "48": {"n": "Poland", "f": "🇵🇱"}, "380": {"n": "Ukraine", "f": "🇺🇦"}, "971": {"n": "UAE", "f": "🇦🇪"},
    "966": {"n": "Saudi Arabia", "f": "🇸🇦"}, "233": {"n": "Ghana", "f": "🇬🇭"}, "254": {"n": "Kenya", "f": "🇰🇪"},
    "94": {"n": "Sri Lanka", "f": "🇱🇰"}, "977": {"n": "Nepal", "f": "🇳🇵"}, "95": {"n": "Myanmar", "f": "🇲🇲"},
    "855": {"n": "Cambodia", "f": "🇰🇭"}, "98": {"n": "Iran", "f": "🇮🇷"}, "964": {"n": "Iraq", "f": "🇮🇶"},
    "93": {"n": "Afghanistan", "f": "🇦🇫"}, "998": {"n": "Uzbekistan", "f": "🇺🇿"}, "31": {"n": "Netherlands", "f": "🇳🇱"},
    "32": {"n": "Belgium", "f": "🇧🇪"}, "46": {"n": "Sweden", "f": "🇸🇪"}, "52": {"n": "Mexico", "f": "🇲🇽"},
    "54": {"n": "Argentina", "f": "🇦🇷"}, "57": {"n": "Colombia", "f": "🇨🇴"}, "216": {"n": "Tunisia", "f": "🇹🇳"},
    "256": {"n": "Uganda", "f": "🇺🇬"}, "243": {"n": "DR Congo", "f": "🇨🇩"}, "244": {"n": "Angola", "f": "🇦🇴"},
    "250": {"n": "Rwanda", "f": "🇷🇼"}, "252": {"n": "Somalia", "f": "🇸🇴"}, "268": {"n": "Eswatini", "f": "🇸🇿"}
}

# --- FUNCTIONS ---

def is_user_joined(user_id):
    try:
        status = bot.get_chat_member(METHOD_GROUP_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True

def get_country_info(range_str):
    for length in [4, 3, 2, 1]:
        code = range_str[:length]
        if code in COUNTRY_DB:
            return COUNTRY_DB[code]['f'], COUNTRY_DB[code]['n']
    return "🏳️", f"Other({range_str[:3]})"

def fetch_live_data():
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=headers).json()
        live_stats = {}
        if res['meta']['code'] == 200:
            for service in res['data']['services']:
                if any(x in service['sid'].lower() for x in ["facebook", "instagram"]):
                    for r in service['ranges']:
                        flag, name = get_country_info(r)
                        key = f"{flag} {name}"
                        if key not in live_stats: live_stats[key] = []
                        live_stats[key].append(r)
        return live_stats
    except: return {}

def auto_check_otp(chat_id, number):
    start_time = time.time()
    while time.time() - start_time < 300:
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=headers).json()
            if res['meta']['code'] == 200:
                for o in res['data']['otps']:
                    if o['number'] == number:
                        bot.send_message(chat_id, f"🎊 **OTP RECEIVED BY BSNUMBER!**\n\n📱 `{number}`\n💬 `{o['message']}`", parse_mode="Markdown")
                        return
            time.sleep(5)
        except: break

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚀 Join Our Method Group", url=METHOD_LINK))
        markup.add(types.InlineKeyboardButton("✅ Joined (Check Again)", callback_data="check_joined"))
        bot.send_message(message.chat.id, "⚠️ **Access Denied!**\n\nবটটি ব্যবহার করতে হলে আপনাকে আমাদের মেথড গ্রুপে জয়েন থাকতে হবে।", reply_markup=markup)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🔥 Number Nin", callback_data="buy_menu"))
    markup.add(types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
               types.InlineKeyboardButton("🛠 Admin Support", callback_data="admin"))
    markup.add(types.InlineKeyboardButton("💳 Add Fund", url="https://voltxsms.com"))
    
    bot.send_message(message.chat.id, "🌟 **Welcome to BSNUMBER Bot** 🌟\n\nনিচের বাটন থেকে দ্রুত নম্বর সিলেক্ট করুন।", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if not is_user_joined(user_id) and call.data != "check_joined":
        bot.answer_callback_query(call.id, "Please join the group first!", show_alert=True)
        return

    if call.data == "check_joined":
        if is_user_joined(user_id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            start(call.message)
        else:
            bot.answer_callback_query(call.id, "আপনি এখনো জয়েন করেননি!", show_alert=True)

    elif call.data == "buy_menu":
        live_data = fetch_live_data()
        if not live_data:
            bot.answer_callback_query(call.id, "No Live Ranges Available!", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(f"{c} ({len(r)})", callback_data=f"list_{c}") for c, r in live_data.items()]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("⬅️ Back Menu", callback_data="back_start"))
        bot.edit_message_text("🌍 **Select Country (Live First):**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("list_"):
        c_key = call.data.replace("list_", "")
        live_data = fetch_live_data()
        ranges = live_data.get(c_key, [])
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(f"📡 Range: {r}", callback_data=f"order_{r}") for r in ranges[:12]]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="buy_menu"))
        bot.edit_message_text(f"📍 **{c_key}**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("order_"):
        rid = call.data.split("_")[1].replace("XXX", "")
        res = requests.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}).json()
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            msg = (f"✅ **Number Ready!**\n\n📱 `{num}`\n🌍 {res['data']['country']}\n\n"
                   f"বট ওটিপি চেক করছে... কোড না আসলে 'Change Number' ক্লিক করুন।")
            
            # আপনার সেই হারিয়ে যাওয়া বাটনগুলো (Group এবং Method) এখানে আছে
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"order_{rid}"))
            markup.add(types.InlineKeyboardButton("👥 Group", url=CHANNEL_LINK),
                       types.InlineKeyboardButton("📖 Method", url=METHOD_LINK))
            
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=auto_check_otp, args=(call.message.chat.id, num)).start()
        else:
            bot.answer_callback_query(call.id, "No Stock!", show_alert=True)

    elif call.data == "back_start":
        start(call.message)

    elif call.data == "admin":
        bot.send_message(call.message.chat.id, f"🛠 **BSNUMBER Support:**\n\n👤 Admin: {ADMIN_HANDLE}")

# --- MAIN ---
if __name__ == "__main__":
    # ১. Render-কে বোঝানোর জন্য একটি ওয়েব সার্ভার আলাদা থ্রেডে চালু হবে
    keep_alive() 
    
    # ২. বটের মেইন পোলিং চালু হবে
    print("BSNUMBER Bot is starting...")
    bot.infinity_polling()
