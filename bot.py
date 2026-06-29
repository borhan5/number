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
CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
METHOD_LINK = "https://t.me/earntrick_BS"

bot = telebot.TeleBot(API_TOKEN)

headers = {
    "mauthapi": VOLTX_KEY,
    "Content-Type": "application/json"
}

# কান্ট্রি ম্যাপ (১০০+ দেশের জন্য কমন কোডগুলো)
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
    "41": "🇨🇭 Switzerland", "46": "🇸🇪 Sweden", "47": "🇳🇴 Norway", "43": "🇦🇹 Austria",
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
    "976": "🇲🇳 Mongolia", "856": "🇱🇦 Laos"
}

def get_country_info(range_str):
    for code in sorted(COUNTRY_DATA.keys(), key=len, reverse=True):
        if range_str.startswith(code):
            return COUNTRY_DATA[code]
    return f"🏳️ Other ({range_str[:3]})"

def fetch_live_data():
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=headers).json()
        live_ranges = {}
        if res['meta']['code'] == 200:
            for service in res['data']['services']:
                # শুধুমাত্র ফেসবুক ও ইন্সটাগ্রাম ফিল্টার
                if any(x in service['sid'].lower() for x in ["facebook", "instagram"]):
                    for r in service['ranges']:
                        c_info = get_country_info(r)
                        if c_info not in live_ranges: live_ranges[c_info] = []
                        live_ranges[c_info].append(r)
        return live_ranges
    except: return {}

# --- OTP AUTO SENDER ---
def auto_check_otp(chat_id, number):
    start_time = time.time()
    while time.time() - start_time < 300: # ৫ মিনিট চেক করবে
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=headers).json()
            if res['meta']['code'] == 200:
                for o in res['data']['otps']:
                    if o['number'] == number:
                        msg = (
                            f"🔔 **NEW OTP RECEIVED!**\n\n"
                            f"📱 **Number:** `{number}`\n"
                            f"💬 **Message:** `{o['message']}`\n\n"
                            f"✅ ওটিপি কপি করতে ওপরে ক্লিক করুন।"
                        )
                        bot.send_message(chat_id, msg, parse_mode="Markdown")
                        return # ওটিপি পেলে লুপ বন্ধ
            time.sleep(5) # ৫ সেকেন্ড পর পর চেক করবে
        except: break

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📱 Number Nin (Live)", callback_data="buy_menu")
    btn2 = types.InlineKeyboardButton("👤 Profile", callback_data="profile")
    btn3 = types.InlineKeyboardButton("🛠 Admin", callback_data="admin_info")
    btn4 = types.InlineKeyboardButton("💳 Add Fund", url="https://voltxsms.com/payment")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    
    bot.send_message(message.chat.id, 
        "🔥 **VOLTX SMS - Fast OTP Service** 🔥\n\n"
        "Facebook & Instagram এর জন্য নম্বর নিতে নিচের বাটনে ক্লিক করুন।\n"
        "বর্তমানে সচল কান্ট্রিগুলো লিস্টের উপরে থাকবে।", 
        reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "buy_menu":
        live_data = fetch_live_data()
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # লাইভ কান্ট্রিগুলো আগে যোগ করা
        for country in live_data.keys():
            markup.add(types.InlineKeyboardButton(f"🟢 {country}", callback_data=f"list_{country}"))
            
        # বাকি কান্ট্রিগুলো যোগ করা (যদি লাইভ লিস্টে না থাকে)
        # (লিস্ট অনেক বড় হবে তাই এখানে মেইন লাইভ গুলোই গুরুত্ব পাবে)
        
        bot.edit_message_text("🌍 **Select Country:**\nসবুজ আইকনগুলো বর্তমানে সচল (Live):", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("list_"):
        c_name = call.data.replace("list_", "")
        live_data = fetch_live_data()
        ranges = live_data.get(c_name, [])
        
        if not ranges:
            bot.answer_callback_query(call.id, "এই দেশের লাইভ রেঞ্জ এখন শেষ। অন্য দেশ দেখুন।", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup()
        for r in ranges[:8]:
            markup.add(types.InlineKeyboardButton(f"📡 Range: {r}", callback_data=f"order_{r}"))
        
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="buy_menu"))
        bot.edit_message_text(f"📍 **Country: {c_name}**\nএকটি রেঞ্জ সিলেক্ট করুন:", 
                              call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("order_"):
        rid = call.data.split("_")[1].replace("XXX", "")
        res = requests.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}).json()
        
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            bot.edit_message_text(
                f"✅ **Number Ready!**\n\n"
                f"📱 **Number:** `{num}`\n"
                f"🌍 **Country:** {res['data']['country']}\n"
                f"⚙️ **Status:** Waiting for OTP...\n\n"
                f"বট অটোমেটিক ওটিপি চেক করছে, কোড আসা মাত্র এখানে জানিয়ে দেওয়া হবে।",
                call.message.chat.id, call.message.message_id, parse_mode="Markdown"
            )
            
            # মেথড ও গ্রুপ বাটন আলাদা ভাবে পাঠানো
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("👥 Join Group", url=CHANNEL_LINK),
                       types.InlineKeyboardButton("📖 Learn Method", url=METHOD_LINK))
            bot.send_message(call.message.chat.id, "নিচের লিংকগুলো চেক করতে পারেন:", reply_markup=markup)
            
            # ওটিপি চেক করার জন্য আলাদা থ্রেড চালু করা
            threading.Thread(target=auto_check_otp, args=(call.message.chat.id, num)).start()
        else:
            bot.answer_callback_query(call.id, "❌ নম্বর পাওয়া যায়নি! অন্য রেঞ্জ দেখুন।", show_alert=True)

    elif call.data == "admin_info":
        bot.send_message(call.message.chat.id, f"👤 **Admin Contact:**\nAdmin ID: `{ADMIN_ID}`\nযেকোনো সমস্যায় যোগাযোগ করুন।", parse_mode="Markdown")

    elif call.data == "profile":
        # এখানে এপিআই থেকে ব্যালেন্স দেখার ফাংশন যোগ করা যায়
        bot.answer_callback_query(call.id, "প্রোফাইল ফিচারটি শীঘ্রই যুক্ত হবে। সাইটে ব্যালেন্স চেক করুন।", show_alert=True)

print("Bot is running...")
bot.infinity_polling()
