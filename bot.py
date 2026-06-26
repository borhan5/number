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

# রিকোয়েস্ট সেশন (স্পিড বাড়ানোর জন্য)
session = requests.Session()

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
    "421": {"name": "Slovakia", " Slovak Republic": "🇸🇰"}, "423": {"name": "Liechtenstein", "flag": "🇱🇮"},
    "43": {"name": "Austria", "flag": "🇦🇹"}, "44": {"name": "UK", "flag": "🇬🇧"},
    "45": {"name": "Denmark", "flag": "🇩🇰"}, "46": {"name": "Sweden", "flag": "🇸🇪"},
    "47": {"name": "Norway", "flag": "🇳🇴"}, "48": {"name": "Poland", "flag": "🇵🇱"},
    "49": {"name": "Germany", "flag": "🇩🇪"}, "880": {"name": "Bangladesh", "flag": "🇧🇩"},
    "91": {"name": "India", "flag": "🇮🇳"}, "92": {"name": "Pakistan", "flag": "🇵🇰"}
}

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "BSNUMBER OTP SYSTEM IS ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def get_headers(): return {"mauthapi": VOLTX_KEY, "Content-Type": "application/json"}

def detect_country(range_str):
    for length in [3, 2, 1]:
        p = range_str[:length]
        if p in COUNTRY_DATA:
            return p
    return None

def monitor_otp(chat_id, number, svc):
    """প্রতি ২ সেকেন্ড অন্তর ওটিপি চেক করবে"""
    start_time = time.time()
    bot.send_message(chat_id, f"⏳ ওটিপি-র জন্য অপেক্ষা করা হচ্ছে... ({svc})", parse_mode="Markdown")
    
    while time.time() - start_time < 600: # ১০ মিনিট ট্রাই করবে
        try:
            res = session.get(f"{BASE_URL}/success-otp", headers=get_headers(), timeout=5).json()
            if res.get('meta', {}).get('code') == 200:
                otps = res['data'].get('otps', [])
                for item in otps:
                    if item['number'] == str(number):
                        msg = item['message']
                        
                        # ওটিপি ফরম্যাটিং লজিক
                        if "facebook" in svc.lower():
                            # ফেসবুকের জন্য কোড বের করবে (সাধারণত ৬ ডিজিট)
                            code_match = re.search(r'\b\d{4,8}\b', msg)
                            otp_code = code_match.group(0) if code_match else "Extracting..."
                            final_text = f"✅ *FACEBOOK OTP RECEIVED!*\n\n🔢 Code: `{otp_code}`\n💬 Full Msg: `{msg}`"
                        else:
                            # ইনস্টাগ্রাম বা অন্যান্য সার্ভিসের জন্য ফুল মেসেজ
                            final_text = f"✅ *{svc.upper()} OTP RECEIVED!*\n\n💬 Message: `{msg}`\n📱 Number: `{number}`"

                        bot.send_message(chat_id, final_text, parse_mode="Markdown")
                        
                        # গ্রুপে লগ পাঠানো
                        bot.send_message(GROUP_ID, f"🔔 *New OTP Log*\nService: {svc}\nNumber: `{number}`\nMessage: {msg}", parse_mode="Markdown")
                        return # ওটিপি পাওয়ার পর লুপ বন্ধ
        except Exception as e:
            print(f"Error checking OTP: {e}")
        
        time.sleep(2) # ২ সেকেন্ড পর পর ওটিপি চেক

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("📦 Stock Number"),
        types.KeyboardButton("📊 Stats"), types.KeyboardButton("💰 Balance")
    )
    welcome_text = f"🤖 *BSNUMBER* | 👋 Hello {message.from_user.first_name}!\n\nপ্যানেল থেকে সব দেশের ট্রাফিক লাইভ আছে। আপনার প্রয়োজনীয় সার্ভিসটি সিলেক্ট করুন।"
    bot.send_photo(message.chat.id, WELCOME_IMAGE, caption=welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_reply_buttons(message):
    if "📞 Get Number" in message.text:
        mk = types.InlineKeyboardMarkup(row_width=2)
        mk.add(
            types.InlineKeyboardButton("📘 FACEBOOK", callback_data="svc_Facebook"),
            types.InlineKeyboardButton("📸 INSTAGRAM", callback_data="svc_Instagram"),
            types.InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_WhatsApp"),
            types.InlineKeyboardButton("✈️ TELEGRAM", callback_data="svc_Telegram")
        )
        bot.send_message(message.chat.id, "🛠 *সার্ভিস সিলেক্ট করুন:*", parse_mode="Markdown", reply_markup=mk)
    
    elif "💰 Balance" in message.text:
        bot.send_message(message.chat.id, "💳 আপনার ব্যালেন্স ও ট্রানজাকশন হিস্টোরি মেইন সার্ভারে সেভ করা হচ্ছে।")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data.startswith("svc_"):
        svc = call.data.split("_")[1]
        bot.edit_message_text(f"🔍 Fetching Full Traffic Countries for *{svc}*...", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        try:
            res = session.get(f"{BASE_URL}/liveaccess", headers=get_headers()).json()
            if res.get('meta', {}).get('code') == 200:
                mk = types.InlineKeyboardMarkup(row_width=1)
                found_countries = {}

                for s in res['data']['services']:
                    if s['sid'].lower() == svc.lower():
                        for r in s['ranges']:
                            c_code = detect_country(r)
                            if c_code and c_code not in found_countries:
                                found_countries[c_code] = r # প্রথম পাওয়া রেঞ্জটি নিচ্ছে
                
                for code, rid in found_countries.items():
                    info = COUNTRY_DATA.get(code, {"name": "Unknown", "flag": "🏳️"})
                    mk.add(types.InlineKeyboardButton(f"{info['flag']} {info['name']} (Live Traffic)", callback_data=f"buy_{svc}_{rid}"))
                
                if not found_countries:
                    bot.send_message(call.message.chat.id, "❌ বর্তমানে কোনো ট্রাফিক পাওয়া যায়নি।")
                else:
                    bot.edit_message_text(f"🌍 *{svc} Available Countries:*", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
        except:
            bot.send_message(call.message.chat.id, "❌ সার্ভার এরর!")

    elif call.data.startswith("buy_"):
        _, svc, rid = call.data.split("_")
        bot.answer_callback_query(call.id, "অর্ডার প্রসেস হচ্ছে...")
        
        try:
            order_res = session.post(f"{BASE_URL}/getnum", json={"rid": rid.replace("XXX", "")}, headers=get_headers()).json()
            if order_res['meta']['code'] == 200:
                num = order_res['data']['full_number']
                
                mk = types.InlineKeyboardMarkup()
                mk.add(types.InlineKeyboardButton("📢 JOIN TELEGRAM", url=GROUP_LINK))
                
                bot.edit_message_text(f"✅ *Number Allocated*\n━━━━━━━━━━━━━━━━━━━━\n"
                                     f"📱 Number: `{num}`\n"
                                     f"🛠 Service: `{svc}`\n"
                                     f"🕒 Status: Waiting for OTP...\n━━━━━━━━━━━━━━━━━━━━", 
                                     call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
                
                # ওটিপি মনিটরিং শুরু
                Thread(target=monitor_otp, args=(call.message.chat.id, num, svc)).start()
            else:
                bot.send_message(call.message.chat.id, f"❌ অর্ডার ফেইল: {order_res['meta'].get('msg', 'Insufficient Balance')}")
        except:
            bot.send_message(call.message.chat.id, "❌ এপিআই কানেকশন এরর!")

if __name__ == "__main__":
    keep_alive()
    print("Bot is running...")
    bot.infinity_polling()
