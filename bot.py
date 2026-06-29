import telebot
import requests
import threading
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAHSON1Qjz7BQmZB1gvpu42vkiX0PaCbayA"
VOLTX_KEY = "MQGVM5B5OOW"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

ADMIN_ID = 8250359361
ADMIN_HANDLE = "@BORHANSB" 
CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
METHOD_LINK = "https://t.me/earntrick_BS"

bot = telebot.TeleBot(API_TOKEN)
headers = {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

# --- ১৫৫+ দেশের বিশাল ডাটাবেজ ---
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
    "250": {"n": "Rwanda", "f": "🇷🇼"}, "252": {"n": "Somalia", "f": "🇸🇴"}, "82": {"n": "S. Korea", "f": "🇰🇷"},
    "81": {"n": "Japan", "f": "🇯🇵"}, "65": {"n": "Singapore", "f": "🇸🇬"}, "61": {"n": "Australia", "f": "🇦🇺"},
    "351": {"n": "Portugal", "f": "🇵🇹"}, "30": {"n": "Greece", "f": "🇬🇷"}, "353": {"n": "Ireland", "f": "🇮🇪"},
    "41": {"n": "Switzerland", "f": "🇨🇭"}, "43": {"n": "Austria", "f": "🇦🇹"}, "45": {"n": "Denmark", "f": "🇩🇰"},
    "47": {"n": "Norway", "f": "🇳🇴"}, "358": {"n": "Finland", "f": "🇫🇮"}, "372": {"n": "Estonia", "f": "🇪🇪"},
    "371": {"n": "Latvia", "f": "🇱🇻"}, "370": {"n": "Lithuania", "f": "🇱🇹"}, "420": {"n": "Czechia", "f": "🇨🇿"},
    "36": {"n": "Hungary", "f": "🇭🇺"}, "40": {"n": "Romania", "f": "🇷🇴"}, "359": {"n": "Bulgaria", "f": "🇧🇬"},
    "381": {"n": "Serbia", "f": "🇷🇸"}, "385": {"n": "Croatia", "f": "🇭🇷"}, "386": {"n": "Slovenia", "f": "🇸🇮"},
    "421": {"n": "Slovakia", "f": "🇸🇰"}, "354": {"n": "Iceland", "f": "🇮🇸"}, "356": {"n": "Malta", "f": "🇲🇹"},
    "357": {"n": "Cyprus", "f": "🇨🇾"}, "972": {"n": "Israel", "f": "🇮🇱"}, "962": {"n": "Jordan", "f": "🇯🇴"},
    "961": {"n": "Lebanon", "f": "🇱🇧"}, "965": {"n": "Kuwait", "f": "🇰🇼"}, "974": {"n": "Qatar", "f": "🇶🇦"},
    "973": {"n": "Bahrain", "f": "🇧🇭"}, "968": {"n": "Oman", "f": "🇴🇲"}, "967": {"n": "Yemen", "f": "🇾🇪"},
    "970": {"n": "Palestine", "f": "🇵🇸"}, "993": {"n": "Turkmenistan", "f": "🇹🇲"}, "992": {"n": "Tajikistan", "f": "🇹🇯"},
    "996": {"n": "Kyrgyzstan", "f": "🇰🇬"}, "995": {"n": "Georgia", "f": "🇬🇪"}, "374": {"n": "Armenia", "f": "🇦🇲"},
    "852": {"n": "Hong Kong", "f": "🇭🇰"}, "886": {"n": "Taiwan", "f": "🇹🇼"}, "853": {"n": "Macau", "f": "🇲🇴"},
    "856": {"n": "Laos", "f": "🇱🇦"}, "975": {"n": "Bhutan", "f": "🇧🇹"}, "976": {"n": "Mongolia", "f": "🇲🇳"},
    "64": {"n": "New Zealand", "f": "🇳🇿"}, "679": {"n": "Fiji", "f": "🇫🇯"}, "56": {"n": "Chile", "f": "🇨🇱"},
    "51": {"n": "Peru", "f": "🇵🇪"}, "58": {"n": "Venezuela", "f": "🇻🇪"}, "593": {"n": "Ecuador", "f": "🇪🇨"},
    "591": {"n": "Bolivia", "f": "🇧🇴"}, "595": {"n": "Paraguay", "f": "🇵🇾"}, "598": {"n": "Uruguay", "f": "🇺🇾"},
    "502": {"n": "Guatemala", "f": "🇬🇹"}, "503": {"n": "El Salvador", "f": "🇸🇻"}, "504": {"n": "Honduras", "f": "🇭🇳"},
    "505": {"n": "Nicaragua", "f": "🇳🇮"}, "506": {"n": "Costa Rica", "f": "🇨🇷"}, "507": {"n": "Panama", "f": "🇵🇦"},
    "237": {"n": "Cameroon", "f": "🇨🇲"}, "241": {"n": "Gabon", "f": "🇬🇦"}, "221": {"n": "Senegal", "f": "🇸🇳"},
    "231": {"n": "Liberia", "f": "🇱🇷"}, "232": {"n": "Sierra Leone", "f": "🇸🇱"}, "228": {"n": "Togo", "f": "🇹🇬"},
    "227": {"n": "Niger", "f": "🇳🇪"}, "226": {"n": "Burkina Faso", "f": "🇧🇫"}, "213": {"n": "Algeria", "f": "🇩🇿"},
    "218": {"n": "Libya", "f": "🇱🇾"}, "249": {"n": "Sudan", "f": "🇸🇩"}, "211": {"n": "South Sudan", "f": "🇸🇸"},
    "254": {"n": "Kenya", "f": "🇰🇪"}, "256": {"n": "Uganda", "f": "🇺🇬"}, "257": {"n": "Burundi", "f": "🇧🇮"},
    "258": {"n": "Mozambique", "f": "🇲🇿"}, "260": {"n": "Zambia", "f": "🇿🇲"}, "263": {"n": "Zimbabwe", "f": "🇿🇼"},
    "264": {"n": "Namibia", "f": "🇳🇦"}, "267": {"n": "Botswana", "f": "🇧🇼"}, "266": {"n": "Lesotho", "f": "🇱🇸"},
    "268": {"n": "Eswatini", "f": "🇸🇿"}
}

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

# --- OTP AUTO SENDER ---
def auto_check_otp(chat_id, number):
    start_time = time.time()
    while time.time() - start_time < 300:
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=headers).json()
            if res['meta']['code'] == 200:
                for o in res['data']['otps']:
                    if o['number'] == number:
                        bot.send_message(chat_id, f"🎊 **OTP RECEIVED!**\n\n📱 `{number}`\n💬 `{o['message']}`", parse_mode="Markdown")
                        return
            time.sleep(5)
        except: break

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🔥 Number Nin", callback_data="buy_menu"))
    markup.add(types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
               types.InlineKeyboardButton("🛠 Admin Support", callback_data="admin"))
    markup.add(types.InlineKeyboardButton("💳 Add Fund", url="https://voltxsms.com"))
    
    bot.send_message(message.chat.id, "🌟 **VOLTX SMS - Premium Bot** 🌟\nনিচের বাটন থেকে দ্রুত নম্বর নিন।", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "buy_menu":
        live_data = fetch_live_data()
        if not live_data:
            bot.answer_callback_query(call.id, "No Live Ranges Available!", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = []
        # সচল দেশগুলো আগে দেখাবে
        for c_info, ranges in live_data.items():
            count = len(ranges)
            btn_text = f"{c_info} ({count})"
            btns.append(types.InlineKeyboardButton(btn_text, callback_data=f"list_{c_info}"))
        
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("⬅️ Back Menu", callback_data="back_start"))
        
        bot.edit_message_text("🌍 **Select Country (Live):**\nবর্তমানে নিচের দেশগুলোতে দ্রুত কোড আসছে:", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("list_"):
        c_key = call.data.replace("list_", "")
        live_data = fetch_live_data()
        ranges = live_data.get(c_key, [])
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(f"📡 Range: {r}", callback_data=f"order_{r}") for r in ranges[:12]]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="buy_menu"))
        
        bot.edit_message_text(f"📍 **{c_key}**\nএকটি রেঞ্জ সিলেক্ট করুন:", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("order_"):
        rid = call.data.split("_")[1].replace("XXX", "")
        res = requests.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}).json()
        
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            msg = (f"✅ **Number Ready!**\n\n📱 `{num}`\n🌍 {res['data']['country']}\n\n"
                   f"বট ওটিপি চেক করছে... কোড না আসলে 'Change' এ ক্লিক করুন।")
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"order_{rid}"))
            markup.add(types.InlineKeyboardButton("👥 Group", url=CHANNEL_LINK),
                       types.InlineKeyboardButton("📖 Method", url=METHOD_LINK))
            
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=auto_check_otp, args=(call.message.chat.id, num)).start()
        else:
            bot.answer_callback_query(call.id, "No Stock in this range!", show_alert=True)

    elif call.data == "back_start":
        start(call.message)

    elif call.data == "admin":
        bot.send_message(call.message.chat.id, f"🛠 **Admin Support:**\n\n👤 Admin: {ADMIN_HANDLE}\nID: `{ADMIN_ID}`")

    elif call.data == "profile":
        bot.answer_callback_query(call.id, "Profile feature under development!", show_alert=True)

# Run
print("Bot is Live with 150+ Countries and Colorful UI...")
bot.infinity_polling()
