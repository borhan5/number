import telebot
import requests
import threading
import time
from telebot import types

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAHSON1Qjz7BQmZB1gvpu42vkiX0PaCbayA"
VOLTX_KEY = "MQGVM5B5OOW"
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

# অ্যাডমিন তথ্য
ADMIN_ID = 8250359361
ADMIN_HANDLE = "@BORHANSB" 

CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
METHOD_LINK = "https://t.me/earntrick_BS"

bot = telebot.TeleBot(API_TOKEN)

headers = {
    "mauthapi": VOLTX_KEY,
    "Content-Type": "application/json"
}

# --- ১০০+ দেশের বিশাল ডাটাবেজ ---
COUNTRY_DATA = {
    "880": "🇧🇩 Bangladesh", "91": "🇮🇳 India", "1": "🇺🇸 USA/Canada", "44": "🇬🇧 United Kingdom",
    "7": "🇷🇺 Russia", "62": "🇮🇩 Indonesia", "84": "🇻🇳 Vietnam", "63": "🇵🇭 Philippines",
    "234": "🇳🇬 Nigeria", "251": "🇪🇹 Ethiopia", "225": "🇨🇮 Ivory Coast", "255": "🇹🇿 Tanzania",
    "20": "🇪🇬 Egypt", "212": "🇲🇦 Morocco", "27": "🇿🇦 South Africa", "55": "🇧🇷 Brazil",
    "60": "🇲🇾 Malaysia", "66": "🇹🇭 Thailand", "92": "🇵🇰 Pakistan", "994": "🇦🇿 Azerbaijan",
    "90": "🇹🇷 Turkey", "49": "🇩🇪 Germany", "33": "🇫🇷 France", "39": "🇮🇹 Italy",
    "34": "🇪🇸 Spain", "48": "🇵🇱 Poland", "380": "🇺🇦 Ukraine", "971": "🇦🇪 UAE",
    "966": "🇸🇦 Saudi Arabia", "233": "🇬🇭 Ghana", "254": "🇰🇪 Kenya", "213": "🇩🇿 Algeria",
    "94": "🇱🇰 Sri Lanka", "977": "🇳🇵 Nepal", "95": "🇲🇲 Myanmar", "855": "🇰🇭 Cambodia",
    "98": "🇮🇷 Iran", "964": "🇮🇶 Iraq", "93": "🇦🇫 Afghanistan", "998": "🇺🇿 Uzbekistan",
    "77": "🇰🇿 Kazakhstan", "40": "🇷🇴 Romania", "31": "🇳🇱 Netherlands", "32": "🇧🇪 Belgium",
    "41": "🇨🇭 Switzerland", "46": "🇸🇪 Sweden", "47": "🇳🇴 Norway", "43": "🇦楯 Austria",
    "30": "🇬🇷 Greece", "351": "🇵🇹 Portugal", "52": "🇲🇽 Mexico", "54": "🇦🇷 Argentina",
    "57": "🇨🇴 Colombia", "56": "🇨🇱 Chile", "51": "🇵🇪 Peru", "58": "🇻🇪 Venezuela",
    "216": "🇹🇳 Tunisia", "231": "🇱🇷 Liberia", "260": "🇿🇲 Zambia", "263": "🇿🇼 Zimbabwe",
    "256": "🇺🇬 Uganda", "249": "🇸🇩 Sudan", "241": "🇬🇦 Gabon", "221": "🇸🇳 Senegal",
    "223": "🇲🇱 Mali", "224": "🇬🇳 Guinea", "227": "🇳🇪 Niger", "229": "🇧🇯 Benin",
    "228": "🇹🇬 Togo", "237": "🇨🇲 Cameroon", "242": "🇨🇬 Congo", "243": "🇨🇩 DR Congo",
    "244": "🇦🇴 Angola", "264": "🇳🇦 Namibia", "267": "🇧🇼 Botswana", "266": "🇱🇸 Lesotho",
    "258": "🇲🇿 Mozambique", "265": "🇲🇼 Malawi", "250": "🇷🇼 Rwanda", "257": "🇧🇮 Burundi",
    "252": "🇸🇴 Somalia", "253": "🇩🇯 Djibouti", "291": "🇪🇷 Eritrea", "211": "🇸🇸 South Sudan",
    "218": "🇱🇾 Libya", "961": "🇱🇧 Lebanon", "962": "🇯🇴 Jordan", "963": "🇸🇾 Syria",
    "965": "🇰🇼 Kuwait", "967": "🇾🇪 Yemen", "968": "🇴🇲 Oman", "970": "🇵🇸 Palestine",
    "972": "🇮🇱 Israel", "973": "🇧🇭 Bahrain", "974": "🇶🇦 Qatar", "975": "🇧🇹 Bhutan",
    "976": "🇲🇳 Mongolia", "856": "🇱🇦 Laos", "852": "🇭🇰 Hong Kong", "886": "🇹🇼 Taiwan",
    "65": "🇸🇬 Singapore", "81": "🇯🇵 Japan", "82": "🇰🇷 South Korea", "61": "🇦🇺 Australia",
    "64": "🇳🇿 New Zealand", "353": "🇮🇪 Ireland", "420": "🇨🇿 Czechia", "36": "🇭🇺 Hungary",
    "358": "🇫🇮 Finland", "45": "🇩🇰 Denmark", "370": "🇱🇹 Lithuania", "371": "🇱🇻 Latvia",
    "372": "🇪🇪 Estonia", "381": "🇷🇸 Serbia", "359": "🇧🇬 Bulgaria", "385": "🇭🇷 Croatia",
    "421": "🇸🇰 Slovakia", "386": "🇸🇮 Slovenia", "354": "🇮🇸 Iceland", "502": "🇬🇹 Guatemala",
    "503": "🇸🇻 El Salvador", "504": "🇭🇳 Honduras", "505": "🇳🇮 Nicaragua", "506": "🇨🇷 Costa Rica",
    "507": "🇵🇦 Panama", "591": "🇧🇴 Bolivia", "593": "🇪🇨 Ecuador", "595": "🇵🇾 Paraguay",
    "598": "🇺🇾 Uruguay"
}

def get_country_info(range_str):
    """রেঞ্জ থেকে দেশের নাম ও পতাকা বের করা"""
    for code in sorted(COUNTRY_DATA.keys(), key=len, reverse=True):
        if range_str.startswith(code):
            return COUNTRY_DATA[code]
    return f"🏳️ Unknown ({range_str[:3]})"

def fetch_live_data():
    """লাইভ এপিআই থেকে ডেটা নিয়ে সর্ট করা"""
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=headers).json()
        live_ranges = {}
        if res['meta']['code'] == 200:
            for service in res['data']['services']:
                # ফেসবুক ও ইন্সটাগ্রাম ফিল্টার
                if any(x in service['sid'].lower() for x in ["facebook", "instagram"]):
                    for r in service['ranges']:
                        c_info = get_country_info(r)
                        if c_info not in live_ranges: live_ranges[c_info] = []
                        live_ranges[c_info].append(r)
        return live_ranges
    except: return {}

# --- OTP AUTO CHECKER ---
active_checks = {}

def auto_check_otp(chat_id, number):
    start_time = time.time()
    active_checks[chat_id] = number
    while time.time() - start_time < 300: # ৫ মিনিট ওটিপির জন্য অপেক্ষা করবে
        if active_checks.get(chat_id) != number: break 
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=headers).json()
            if res['meta']['code'] == 200:
                for o in res['data']['otps']:
                    if o['number'] == number:
                        msg = (
                            f"📩 **NEW OTP RECEIVED!**\n\n"
                            f"📱 **Number:** `{number}`\n"
                            f"💬 **Message:** `{o['message']}`\n\n"
                            f"✨ **Full Content:**\n`{o['message']}`\n\n"
                            f"✅ ধন্যবাদ আমাদের সাথে থাকার জন্য!"
                        )
                        bot.send_message(chat_id, msg, parse_mode="Markdown")
                        return
            time.sleep(5)
        except: break

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📱 Number Nin (Live)", callback_data="buy_menu")
    btn2 = types.InlineKeyboardButton("👤 Profile", callback_data="profile")
    btn3 = types.InlineKeyboardButton("🛠 Admin Support", callback_data="admin_info")
    btn4 = types.InlineKeyboardButton("💳 Add Fund", url="https://voltxsms.com/payment")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    
    bot.send_message(message.chat.id, 
        "👋 **Welcome to VOLTX SMS Bot!**\n\n"
        "Facebook & Instagram এর কোড এখন আরও দ্রুত আসবে।\n"
        "বর্তমানে সচল কান্ট্রিগুলো সবার ওপরে দেওয়া হয়েছে।", 
        reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "buy_menu":
        live_data = fetch_live_data()
        if not live_data:
            bot.answer_callback_query(call.id, "দুঃখিত! বর্তমানে কোনো লাইভ রেঞ্জ নেই।", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        # সচল কান্ট্রিগুলো আগে সাজানো হচ্ছে
        for country in live_data.keys():
            markup.add(types.InlineKeyboardButton(f"🟢 {country}", callback_data=f"list_{country}"))
        
        bot.edit_message_text("🌍 **Select Country (Live First):**\nনিচের দেশগুলোতে বর্তমানে দ্রুত কোড আসছে:", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("list_"):
        c_name = call.data.replace("list_", "")
        live_data = fetch_live_data()
        ranges = live_data.get(c_name, [])
        
        if not ranges:
            bot.answer_callback_query(call.id, "এই রেঞ্জটি বর্তমানে শেষ হয়ে গেছে।", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup()
        for r in ranges[:8]:
            markup.add(types.InlineKeyboardButton(f"📡 Range: {r}", callback_data=f"order_{r}"))
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="buy_menu"))
        bot.edit_message_text(f"📍 **Country: {c_name}**\nএকটি রেঞ্জ সিলেক্ট করে নম্বর নিন:", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("order_"):
        rid = call.data.split("_")[1].replace("XXX", "")
        res = requests.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}).json()
        
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            msg = (
                f"✅ **Number Allocated!**\n\n"
                f"📱 **Number:** `{num}`\n"
                f"🌍 **Country:** {res['data']['country']}\n"
                f"⏳ **Status:** Waiting for OTP...\n\n"
                f"বট অটোমেটিক চেক করছে। কোড না আসলে 'Change Number' ক্লিক করুন।"
            )
            
            markup = types.InlineKeyboardMarkup()
            btn_change = types.InlineKeyboardButton("🔄 Change Number", callback_data=f"order_{rid}")
            btn_grp = types.InlineKeyboardButton("👥 Group", url=CHANNEL_LINK)
            btn_method = types.InlineKeyboardButton("📖 Method", url=METHOD_LINK)
            
            markup.add(btn_change)
            markup.add(btn_grp, btn_method)
            
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=auto_check_otp, args=(call.message.chat.id, num)).start()
        else:
            bot.answer_callback_query(call.id, "❌ No stock! Try another range.", show_alert=True)

    elif call.data == "admin_info":
        admin_text = (
            f"🛠 **Support Team**\n\n"
            f"👤 Admin 1 ID: `{ADMIN_ID}`\n"
            f"👤 Admin 2: {ADMIN_HANDLE}\n\n"
            f"যেকোনো সমস্যায় আমাদের নক দিন।"
        )
        bot.send_message(call.message.chat.id, admin_text, parse_mode="Markdown")

    elif call.data == "profile":
        bot.answer_callback_query(call.id, "Profile features will be added soon!", show_alert=True)

# বট চালু
print("VOLTX SMS Bot is running with 100+ Countries...")
bot.infinity_polling()
