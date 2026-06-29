import os
import telebot
import requests
import threading
import time
from telebot import types
from flask import Flask

# --- RENDER FIX (বট চালু রাখার জন্য) ---
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
API_TOKEN = "8953289994:AAHTZsMr1A-pkjeVfL6VZr3WwkqqvXCppSc"
VOLTX_KEY = "MQGVM5B5OOW"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

ADMIN_ID = 8250359361
ADMIN_HANDLE = "@BORHANSB" 

METHOD_GROUP_ID = -1001859871146 
OTP_LOG_GROUP_ID = -1003968881110 # "borhan otp" গ্রুপ আইডি

METHOD_LINK = "https://t.me/earntrick_BS" 
CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(API_TOKEN)
headers = {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

# --- বিশ্বের প্রায় সব দেশের ডাটাবেজ (Full World Countries) ---
COUNTRY_DB = {
    "1": {"n": "USA/Canada", "f": "🇺🇸"}, "7": {"n": "Russia/Kazakhstan", "f": "🇷🇺"}, "20": {"n": "Egypt", "f": "🇪🇬"},
    "27": {"n": "South Africa", "f": "🇿🇦"}, "30": {"n": "Greece", "f": "🇬🇷"}, "31": {"n": "Netherlands", "f": "🇳🇱"},
    "32": {"n": "Belgium", "f": "🇧🇪"}, "33": {"n": "France", "f": "🇫🇷"}, "34": {"n": "Spain", "f": "🇪🇸"},
    "36": {"n": "Hungary", "f": "🇭🇺"}, "39": {"n": "Italy", "f": "🇮🇹"}, "40": {"n": "Romania", "f": "🇷🇴"},
    "41": {"n": "Switzerland", "f": "🇨🇭"}, "43": {"n": "Austria", "f": "🇦🇹"}, "44": {"n": "UK", "f": "🇬🇧"},
    "45": {"n": "Denmark", "f": "🇩🇰"}, "46": {"n": "Sweden", "f": "🇸🇪"}, "47": {"n": "Norway", "f": "🇳🇴"},
    "48": {"n": "Poland", "f": "🇵🇱"}, "49": {"n": "Germany", "f": "🇩🇪"}, "51": {"n": "Peru", "f": "🇵🇪"},
    "52": {"n": "Mexico", "f": "🇲🇽"}, "53": {"n": "Cuba", "f": "🇨🇺"}, "54": {"n": "Argentina", "f": "🇦🇷"},
    "55": {"n": "Brazil", "f": "🇧🇷"}, "56": {"n": "Chile", "f": "🇨🇱"}, "57": {"n": "Colombia", "f": "🇨🇴"},
    "58": {"n": "Venezuela", "f": "🇻🇪"}, "60": {"n": "Malaysia", "f": "🇲🇾"}, "61": {"n": "Australia", "f": "🇦🇺"},
    "62": {"n": "Indonesia", "f": "🇮🇩"}, "63": {"n": "Philippines", "f": "🇵🇭"}, "64": {"n": "New Zealand", "f": "🇳🇿"},
    "65": {"n": "Singapore", "f": "🇸🇬"}, "66": {"n": "Thailand", "f": "🇹🇭"}, "81": {"n": "Japan", "f": "🇯🇵"},
    "82": {"n": "South Korea", "f": "🇰🇷"}, "84": {"n": "Vietnam", "f": "🇻🇳"}, "86": {"n": "China", "f": "🇨🇳"},
    "90": {"n": "Turkey", "f": "🇹🇷"}, "91": {"n": "India", "f": "🇮🇳"}, "92": {"n": "Pakistan", "f": "🇵🇰"},
    "93": {"n": "Afghanistan", "f": "🇦🇫"}, "94": {"n": "Sri Lanka", "f": "🇱🇰"}, "95": {"n": "Myanmar", "f": "🇲🇲"},
    "98": {"n": "Iran", "f": "🇮🇷"}, "211": {"n": "South Sudan", "f": "🇸🇸"}, "212": {"n": "Morocco", "f": "🇲🇦"},
    "213": {"n": "Algeria", "f": "🇩🇿"}, "216": {"n": "Tunisia", "f": "🇹🇳"}, "218": {"n": "Libya", "f": "🇱🇾"},
    "220": {"n": "Gambia", "f": "🇬🇲"}, "221": {"n": "Senegal", "f": "🇸🇳"}, "222": {"n": "Mauritania", "f": "🇲🇷"},
    "223": {"n": "Mali", "f": "🇲🇱"}, "224": {"n": "Guinea", "f": "🇬🇳"}, "225": {"n": "Ivory Coast", "f": "🇨🇮"},
    "226": {"n": "Burkina Faso", "f": "🇧🇫"}, "227": {"n": "Niger", "f": "🇳🇪"}, "228": {"n": "Togo", "f": "🇹🇬"},
    "229": {"n": "Benin", "f": "🇧🇯"}, "230": {"n": "Mauritius", "f": "🇲🇺"}, "231": {"n": "Liberia", "f": "🇱🇷"},
    "232": {"n": "Sierra Leone", "f": "🇸🇱"}, "233": {"n": "Ghana", "f": "🇬🇭"}, "234": {"n": "Nigeria", "f": "🇳🇬"},
    "235": {"n": "Chad", "f": "🇹🇩"}, "236": {"n": "CAR", "f": "🇨🇫"}, "237": {"n": "Cameroon", "f": "🇨🇲"},
    "239": {"n": "Sao Tome", "f": "🇸🇹"}, "240": {"n": "Equatorial Guinea", "f": "🇬🇶"}, "241": {"n": "Gabon", "f": "🇬🇦"},
    "242": {"n": "Congo", "f": "🇨🇬"}, "243": {"n": "DR Congo", "f": "🇨🇩"}, "244": {"n": "Angola", "f": "🇦🇴"},
    "245": {"n": "Guinea-Bissau", "f": "🇬🇼"}, "248": {"n": "Seychelles", "f": "🇸🇨"}, "249": {"n": "Sudan", "f": "🇸🇩"},
    "250": {"n": "Rwanda", "f": "🇷🇼"}, "251": {"n": "Ethiopia", "f": "🇪🇹"}, "252": {"n": "Somalia", "f": "🇸🇴"},
    "253": {"n": "Djibouti", "f": "🇩🇯"}, "254": {"n": "Kenya", "f": "🇰🇪"}, "255": {"n": "Tanzania", "f": "🇹🇿"},
    "256": {"n": "Uganda", "f": "🇺🇬"}, "257": {"n": "Burundi", "f": "🇧🇮"}, "258": {"n": "Mozambique", "f": "🇲🇿"},
    "260": {"n": "Zambia", "f": "🇿🇲"}, "261": {"n": "Madagascar", "f": "🇲🇬"}, "263": {"n": "Zimbabwe", "f": "🇿🇼"},
    "264": {"n": "Namibia", "f": "🇳🇦"}, "265": {"n": "Malawi", "f": "🇲🇼"}, "266": {"n": "Lesotho", "f": "🇱🇸"},
    "267": {"n": "Botswana", "f": "🇧🇼"}, "268": {"n": "Eswatini", "f": "🇸🇿"}, "291": {"n": "Eritrea", "f": "🇪🇷"},
    "351": {"n": "Portugal", "f": "🇵🇹"}, "352": {"n": "Luxembourg", "f": "🇱🇺"}, "353": {"n": "Ireland", "f": "🇮🇪"},
    "354": {"n": "Iceland", "f": "🇮🇸"}, "355": {"n": "Albania", "f": "🇦🇱"}, "358": {"n": "Finland", "f": "🇫🇮"},
    "359": {"n": "Bulgaria", "f": "🇧🇬"}, "370": {"n": "Lithuania", "f": "🇱🇹"}, "371": {"n": "Latvia", "f": "🇱🇻"},
    "372": {"n": "Estonia", "f": "🇪🇪"}, "373": {"n": "Moldova", "f": "🇲🇩"}, "374": {"n": "Armenia", "f": "🇦🇲"},
    "375": {"n": "Belarus", "f": "🇧🇾"}, "380": {"n": "Ukraine", "f": "🇺🇦"}, "381": {"n": "Serbia", "f": "🇷🇸"},
    "385": {"n": "Croatia", "f": "🇭🇷"}, "386": {"n": "Slovenia", "f": "🇸🇮"}, "420": {"n": "Czech Republic", "f": "🇨🇿"},
    "421": {"n": "Slovakia", "f": "🇸🇰"}, "502": {"n": "Guatemala", "f": "🇬🇹"}, "503": {"n": "El Salvador", "f": "🇸🇻"},
    "504": {"n": "Honduras", "f": "🇭🇳"}, "505": {"n": "Nicaragua", "f": "🇳🇮"}, "506": {"n": "Costa Rica", "f": "🇨🇷"},
    "507": {"n": "Panama", "f": "🇵🇦"}, "509": {"n": "Haiti", "f": "🇭🇹"}, "591": {"n": "Bolivia", "f": "🇧🇴"},
    "593": {"n": "Ecuador", "f": "🇪🇨"}, "595": {"n": "Paraguay", "f": "🇵🇾"}, "598": {"n": "Uruguay", "f": "🇺🇾"},
    "852": {"n": "Hong Kong", "f": "🇭🇰"}, "855": {"n": "Cambodia", "f": "🇰🇭"}, "856": {"n": "Laos", "f": "🇱🇦"},
    "880": {"n": "Bangladesh", "f": "🇧🇩"}, "886": {"n": "Taiwan", "f": "🇹🇼"}, "960": {"n": "Maldives", "f": "🇲🇻"},
    "961": {"n": "Lebanon", "f": "🇱🇧"}, "962": {"n": "Jordan", "f": "🇯🇴"}, "963": {"n": "Syria", "f": "🇸🇾"},
    "964": {"n": "Iraq", "f": "🇮🇶"}, "965": {"n": "Kuwait", "f": "🇰🇼"}, "966": {"n": "Saudi Arabia", "f": "🇸🇦"},
    "967": {"n": "Yemen", "f": "🇾🇪"}, "968": {"n": "Oman", "f": "🇴🇲"}, "971": {"n": "UAE", "f": "🇦🇪"},
    "972": {"n": "Israel", "f": "🇮🇱"}, "973": {"n": "Bahrain", "f": "🇧🇭"}, "974": {"n": "Qatar", "f": "🇶🇦"},
    "976": {"n": "Mongolia", "f": "🇲🇳"}, "977": {"n": "Nepal", "f": "🇳🇵"}, "992": {"n": "Tajikistan", "f": "🇹🇯"},
    "993": {"n": "Turkmenistan", "f": "🇹🇲"}, "994": {"n": "Azerbaijan", "f": "🇦🇿"}, "995": {"n": "Georgia", "f": "🇬🇪"},
    "996": {"n": "Kyrgyzstan", "f": "🇰🇬"}, "998": {"n": "Uzbekistan", "f": "🇺🇿"}
}

# --- FUNCTIONS ---

def is_user_joined(user_id):
    try:
        status = bot.get_chat_member(METHOD_GROUP_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True

def mask_number(num_str):
    """মাঝখানের ৩টি সংখ্যা হাইড করার ফাংশন"""
    if len(num_str) > 7:
        return f"{num_str[:5]}***{num_str[-3:]}"
    return num_str

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

def auto_check_otp(chat_id, number, country_info):
    start_time = time.time()
    while time.time() - start_time < 300: # ৫ মিনিট চেক
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=headers).json()
            if res['meta']['code'] == 200:
                for o in res['data']['otps']:
                    if o['number'] == number:
                        # ইউজারের জন্য ফুল মেসেজ
                        full_msg = (f"🎊 **OTP RECEIVED BY BSNUMBER!**\n\n"
                                   f"🌍 Country: {country_info}\n"
                                   f"📱 Number: `{number}`\n"
                                   f"💬 Message: `{o['message']}`")
                        bot.send_message(chat_id, full_msg, parse_mode="Markdown")
                        
                        # গ্রুপের জন্য মাস্ক মেসেজ (নম্বর হাইড)
                        masked_num = mask_number(number)
                        group_msg = (f"📢 **NEW OTP LOG (borhan otp)**\n\n"
                                    f"🌍 Country: {country_info}\n"
                                    f"📱 Number: `{masked_num}`\n"
                                    f"💬 Message: `{o['message']}`")
                        bot.send_message(OTP_LOG_GROUP_ID, group_msg, parse_mode="Markdown")
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
        bot.edit_message_text("🌍 **Select Country:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

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
            country = res['data']['country']
            msg = (f"✅ **Number Ready!**\n\n📱 `{num}`\n🌍 {country}\n\n"
                   f"বট ওটিপি চেক করছে... কোড না আসলে 'Change Number' ক্লিক করুন।")
            
            # আপনার বাটনগুলো এখানে
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"order_{rid}"))
            markup.add(types.InlineKeyboardButton("👥 Group", url=CHANNEL_LINK),
                       types.InlineKeyboardButton("📖 Method", url=METHOD_LINK))
            
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=auto_check_otp, args=(call.message.chat.id, num, country)).start()
        else:
            bot.answer_callback_query(call.id, "No Stock!", show_alert=True)

    elif call.data == "back_start":
        start(call.message)

    elif call.data == "admin":
        bot.send_message(call.message.chat.id, f"🛠 **BSNUMBER Support:**\n\n👤 Admin: {ADMIN_HANDLE}")

# --- MAIN ---
if __name__ == "__main__":
    keep_alive() 
    print("BSNUMBER Bot is starting...")
    bot.infinity_polling()
