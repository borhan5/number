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
# স্টার্ট মেনুর ছবির লিঙ্ক (আপনার কোনো পছন্দ থাকলে লিঙ্ক পাল্টে নিতে পারেন)
WELCOME_IMAGE = "https://telegra.ph/file/0c9a3c988b4c0d9a6c4b1.jpg" 

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
    "290": {"name": "Saint Helena", "flag": "🇸🇭"}, "291": {"name": "Eritrea", "flag": "🇪🇷"},
    "297": {"name": "Aruba", "flag": "🇦🇼"}, "298": {"name": "Faroe Islands", "flag": "🇫🇴"},
    "299": {"name": "Greenland", "flag": "🇬🇱"}, "30": {"name": "Greece", "flag": "🇬🇷"},
    "31": {"name": "Netherlands", "flag": "🇳🇱"}, "32": {"name": "Belgium", "flag": "🇧🇪"},
    "33": {"name": "France", "flag": "🇫🇷"}, "34": {"name": "Spain", "flag": "🇪🇸"},
    "350": {"name": "Gibraltar", "flag": "🇬🇮"}, "351": {"name": "Portugal", "flag": "🇵🇹"},
    "352": {"name": "Luxembourg", "flag": "🇱🇺"}, "353": {"name": "Ireland", "flag": "🇮🇪"},
    "354": {"name": "Iceland", "flag": "🇮🇸"}, "355": {"name": "Albania", "flag": "🇦🇱"},
    "356": {"name": "Malta", "flag": "🇲🇹"}, "357": {"name": "Cyprus", "flag": "🇨🇾"},
    "358": {"name": "Finland", "flag": "🇫🇮"}, "359": {"name": "Bulgaria", "flag": "🇧🇬"},
    "36": {"name": "Hungary", "flag": "🇭🇺"}, "370": {"name": "Lithuania", "flag": "🇱🇹"},
    "371": {"name": "Latvia", "flag": "🇱🇻"}, "372": {"name": "Estonia", "flag": "🇪🇪"},
    "373": {"name": "Moldova", "flag": "🇲🇩"}, "374": {"name": "Armenia", "flag": "🇦🇲"},
    "375": {"name": "Belarus", "flag": "🇧🇾"}, "376": {"name": "Andorra", "flag": "🇦🇩"},
    "377": {"name": "Monaco", "flag": "🇲🇨"}, "378": {"name": "San Marino", "flag": "🇸🇲"},
    "380": {"name": "Ukraine", "flag": "🇺🇦"}, "381": {"name": "Serbia", "flag": "🇷🇸"},
    "382": {"name": "Montenegro", "flag": "🇲🇪"}, "383": {"name": "Kosovo", "flag": "🇽🇰"},
    "385": {"name": "Croatia", "flag": "🇭🇷"}, "386": {"name": "Slovenia", "flag": "🇸🇮"},
    "387": {"name": "Bosnia", "flag": "🇧🇦"}, "389": {"name": "Macedonia", "flag": "🇲🇰"},
    "39": {"name": "Italy", "flag": "🇮🇹"}, "40": {"name": "Romania", "flag": "🇷🇴"},
    "41": {"name": "Switzerland", "flag": "🇨🇭"}, "420": {"name": "Czech Rep.", "flag": "🇨🇿"},
    "421": {"name": "Slovakia", "flag": "🇸🇰"}, "423": {"name": "Liechtenstein", "flag": "🇱🇮"},
    "43": {"name": "Austria", "flag": "🇦🇹"}, "44": {"name": "UK", "flag": "🇬🇧"},
    "45": {"name": "Denmark", "flag": "🇩🇰"}, "46": {"name": "Sweden", "flag": "🇸🇪"},
    "47": {"name": "Norway", "flag": "🇳🇴"}, "48": {"name": "Poland", "flag": "🇵🇱"},
    "49": {"name": "Germany", "flag": "🇩🇪"}, "500": {"name": "Falkland Isl.", "flag": "🇫🇰"},
    "501": {"name": "Belize", "flag": "🇧🇿"}, "502": {"name": "Guatemala", "flag": "🇬🇹"},
    "503": {"name": "El Salvador", "flag": "🇸🇻"}, "504": {"name": "Honduras", "flag": "🇭🇳"},
    "505": {"name": "Nicaragua", "flag": "🇳🇮"}, "506": {"name": "Costa Rica", "flag": "🇨🇷"},
    "507": {"name": "Panama", "flag": "🇵🇦"}, "508": {"name": "St. Pierre", "flag": "🇵🇲"},
    "509": {"name": "Haiti", "flag": "🇭🇹"}, "51": {"name": "Peru", "flag": "🇵🇪"},
    "52": {"name": "Mexico", "flag": "🇲🇽"}, "53": {"name": "Cuba", "flag": "🇨🇺"},
    "54": {"name": "Argentina", "flag": "🇦🇷"}, "55": {"name": "Brazil", "flag": "🇧🇷"},
    "56": {"name": "Chile", "flag": "🇨🇱"}, "57": {"name": "Colombia", "flag": "🇨🇴"},
    "58": {"name": "Venezuela", "flag": "🇻🇪"}, "590": {"name": "Guadeloupe", "flag": "🇬🇵"},
    "591": {"name": "Bolivia", "flag": "🇧🇴"}, "592": {"name": "Guyana", "flag": "🇬🇾"},
    "593": {"name": "Ecuador", "flag": "🇪🇨"}, "594": {"name": "French Guiana", "flag": "🇬🇫"},
    "595": {"name": "Paraguay", "flag": "🇵🇾"}, "596": {"name": "Martinique", "flag": "🇲🇶"},
    "597": {"name": "Suriname", "flag": "🇸🇷"}, "598": {"name": "Uruguay", "flag": "🇺🇾"},
    "599": {"name": "Curacao", "flag": "🇨🇼"}, "60": {"name": "Malaysia", "flag": "🇲🇾"},
    "61": {"name": "Australia", "flag": "🇦🇺"}, "62": {"name": "Indonesia", "flag": "🇮🇩"},
    "63": {"name": "Philippines", "flag": "🇵🇭"}, "64": {"name": "New Zealand", "flag": "🇳🇿"},
    "65": {"name": "Singapore", "flag": "🇸🇬"}, "66": {"name": "Thailand", "flag": "🇹🇭"},
    "670": {"name": "Timor-Leste", "flag": "🇹🇱"}, "672": {"name": "Norfolk Isl.", "flag": "🇳🇫"},
    "673": {"name": "Brunei", "flag": "🇧🇳"}, "674": {"name": "Nauru", "flag": "🇳🇷"},
    "675": {"name": "Papua N.G.", "flag": "🇵🇬"}, "676": {"name": "Tonga", "flag": "🇹🇴"},
    "677": {"name": "Solomon Isl.", "flag": "🇸🇧"}, "678": {"name": "Vanuatu", "flag": "🇻🇺"},
    "679": {"name": "Fiji", "flag": "🇫🇯"}, "680": {"name": "Palau", "flag": "🇵🇼"},
    "681": {"name": "Wallis/Futuna", "flag": "🇼🇫"}, "682": {"name": "Cook Isl.", "flag": "🇨🇰"},
    "683": {"name": "Niue", "flag": "🇳🇺"}, "685": {"name": "Samoa", "flag": "🇼🇸"},
    "686": {"name": "Kiribati", "flag": "🇰🇮"}, "687": {"name": "New Caledonia", "flag": "🇳🇨"},
    "688": {"name": "Tuvalu", "flag": "🇹🇻"}, "689": {"name": "Fr. Polynesia", "flag": "🇵🇫"},
    "690": {"name": "Tokelau", "flag": "🇹🇰"}, "691": {"name": "Micronesia", "flag": "🇫🇲"},
    "692": {"name": "Marshall Isl.", "flag": "🇲🇭"}, "81": {"name": "Japan", "flag": "🇯🇵"},
    "82": {"name": "South Korea", "flag": "🇰🇷"}, "84": {"name": "Vietnam", "flag": "🇻🇳"},
    "850": {"name": "North Korea", "flag": "🇰🇵"}, "852": {"name": "Hong Kong", "flag": "🇭🇰"},
    "853": {"name": "Macau", "flag": "🇲🇴"}, "855": {"name": "Cambodia", "flag": "🇰🇭"},
    "856": {"name": "Laos", "flag": "🇱🇦"}, "86": {"name": "China", "flag": "🇨🇳"},
    "880": {"name": "Bangladesh", "flag": "🇧🇩"}, "886": {"name": "Taiwan", "flag": "🇹🇼"},
    "90": {"name": "Turkey", "flag": "🇹🇷"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "93": {"name": "Afghanistan", "flag": "🇦🇫"},
    "94": {"name": "Sri Lanka", "flag": "🇱🇰"}, "95": {"name": "Myanmar", "flag": "🇲🇲"},
    "960": {"name": "Maldives", "flag": "🇲🇻"}, "961": {"name": "Lebanon", "flag": "🇱🇧"},
    "962": {"name": "Jordan", "flag": "🇯🇴"}, "963": {"name": "Syria", "flag": "🇸🇾"},
    "964": {"name": "Iraq", "flag": "🇮🇶"}, "965": {"name": "Kuwait", "flag": "🇰🇼"},
    "966": {"name": "Saudi Arabia", "flag": "🇸🇦"}, "967": {"name": "Yemen", "flag": "🇾🇪"},
    "968": {"name": "Oman", "flag": "🇴🇲"}, "970": {"name": "Palestine", "flag": "🇵🇸"},
    "971": {"name": "UAE", "flag": "🇦🇪"}, "972": {"name": "Israel", "flag": "🇮🇱"},
    "973": {"name": "Bahrain", "flag": "🇧🇭"}, "974": {"name": "Qatar", "flag": "🇶🇦"},
    "975": {"name": "Bhutan", "flag": "🇧🇹"}, "976": {"name": "Mongolia", "flag": "🇲🇳"},
    "977": {"name": "Nepal", "flag": "🇳🇵"}, "992": {"name": "Tajikistan", "flag": "🇹🇯"},
    "993": {"name": "Turkmenistan", "flag": "🇹🇲"}, "994": {"name": "Azerbaijan", "flag": "🇦🇿"},
    "995": {"name": "Georgia", "flag": "🇬🇪"}, "996": {"name": "Kyrgyzstan", "flag": "🇰🇬"},
    "998": {"name": "Uzbekistan", "flag": "🇺🇿"}
}

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "BSNUMBER ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def get_headers(): return {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

def detect_country(prefix_full):
    for length in [3, 2, 1]:
        p = prefix_full[:length]
        if p in COUNTRY_DATA:
            return p
    return None

def monitor_otp(chat_id, number, svc):
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                for item in res['data']['otps']:
                    if item['number'] == number:
                        otp = re.findall(r'\b\d{4,6}\b', item['message'])[0] if re.findall(r'\b\d{4,6}\b', item['message']) else "Received"
                        bot.send_message(chat_id, f"✅ *{svc} OTP RECEIVED!*\n\n📱 Number: `{number}`\n🔢 OTP: `{otp}`\n\n💬 Msg: `{item['message']}`", parse_mode="Markdown")
                        bot.send_message(GROUP_ID, f"🔔 *New OTP Log*\nService: {svc}\nNumber: `{number[:7]}***` \nOTP: `{otp}`", parse_mode="Markdown")
                        return
        except: pass
        time.sleep(5)

@bot.message_handler(commands=['start'])
def start_handler(message):
    name = message.from_user.first_name
    # মেইন রিপ্লাই কিবোর্ড (স্ক্রিনশটের মতো)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("📦 Stock Number"),
        types.KeyboardButton("🔐 Get 2FA"), types.KeyboardButton("Extract OTP"),
        types.KeyboardButton("📊 Stats"), types.KeyboardButton("💰 Balance")
    )
    
    welcome_text = f"🤖 *BSNUMBER* | 👋 Hello, {name}!\n✅ Select a service from the buttons below:"
    
    try:
        bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_reply_buttons(message):
    chat_id = message.chat.id
    text = message.text

    if "📞 Get Number" in text:
        mk = types.InlineKeyboardMarkup(row_width=1)
        mk.add(
            types.InlineKeyboardButton("📘 FACEBOOK", callback_data="svc_Facebook"),
            types.InlineKeyboardButton("📸 INSTAGRAM", callback_data="svc_Instagram"),
            types.InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_WhatsApp")
        )
        bot.send_message(chat_id, "🛠 *সার্ভিস সিলেক্ট করুন (All Countries Available):*", parse_mode="Markdown", reply_markup=mk)

    elif "💰 Balance" in text:
        bot.send_message(chat_id, "💳 Your current balance is tracked in the main console.")
    
    elif "📊 Stats" in text:
        bot.send_message(chat_id, "📈 System is running at 100% efficiency.")
    
    else:
        bot.send_message(chat_id, f"⚠️ '{text}' functionality will be added soon.")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data.startswith("svc_"):
        svc = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"Fetching All Countries for {svc}...")
        
        res = requests.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
        traffic_map = {}
        
        if res.get('meta', {}).get('code') == 200:
            for s in res['data']['services']:
                if s['sid'].lower() == svc.lower():
                    for r in s['ranges']:
                        c_code = detect_country(r)
                        if c_code:
                            traffic_map[c_code] = traffic_map.get(c_code, 0) + 1
        
        # সব দেশ দেখাবে (ট্রাফিক অনুযায়ী সাজানো)
        sorted_countries = sorted(traffic_map.items(), key=lambda x: x[1], reverse=True)
        
        mk = types.InlineKeyboardMarkup(row_width=1)
        for code, count in sorted_countries:
            info = COUNTRY_DATA[code]
            mk.add(types.InlineKeyboardButton(f"{info['flag']} {info['name']} (FULL TRAFFIC)", callback_data=f"buy_{svc}_{code}"))
        
        if not sorted_countries:
            bot.send_message(call.message.chat.id, "❌ বর্তমানে কোনো ট্রাফিক পাওয়া যায়নি।")
            return
            
        bot.edit_message_text(f"🌍 *{svc} Available Countries:*\n(সব দেশ এখানে দেওয়া হয়েছে)", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)

    elif call.data.startswith("buy_"):
        _, svc, code = call.data.split("_")
        bot.answer_callback_query(call.id, "Allocating Fast Number...")
        
        res = requests.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
        target_rid = None
        for s in res['data']['services']:
            if s['sid'].lower() == svc.lower():
                for r in s['ranges']:
                    if r.startswith(code):
                        target_rid = r.replace("XXX", "")
                        break
        
        if target_rid:
            order = requests.post(f"{BASE_URL}/getnum", json={"rid": target_rid}, headers=get_headers()).json()
            if order['meta']['code'] == 200:
                num = order['data']['full_number']
                mk = types.InlineKeyboardMarkup(row_width=1)
                mk.add(types.InlineKeyboardButton("🔄 CHANGE NUMBER", callback_data=f"buy_{svc}_{code}"))
                mk.add(types.InlineKeyboardButton("📢 JOIN OTP GROUP", url=GROUP_LINK))
                
                bot.edit_message_text(f"✅ *{svc} Number Allocated*\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"📞 Number: `{num}`\n"
                                     f"🌍 Country: {COUNTRY_DATA[code]['name']} {COUNTRY_DATA[code]['flag']}\n\n"
                                     f"⏳ ওটিপি কনসোল চেক করা হচ্ছে...", 
                                     call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                
                Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, "❌ স্টক শেষ বা ব্যালেন্স নেই।")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
