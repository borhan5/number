import telebot
import requests
import time
import threading
import re
from flask import Flask
from telebot import types
from waitress import serve

# --- CONFIGURATION ---
BOT_TOKEN = 'BOT_TOKEN = '8953289994:AAF_s1M9_kcPufc4bmo_FIOcTdiL3YzxNtA' 
API_KEY = 'MQGVM5B5OOW'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"
DEV_LINK = "https://t.me/BORHANSB"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# Session tracking for Cancel/Change logic
active_sessions = {} 

# --- ULTIMATE GLOBAL COUNTRY DATABASE (200+ Countries) ---
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

def get_flag_info(range_val):
    clean = str(range_val).replace("+", "").replace("X", "").strip()
    sorted_codes = sorted(COUNTRY_DATA.keys(), key=len, reverse=True)
    for code in sorted_codes:
        if clean.startswith(code):
            return COUNTRY_DATA[code]
    return {"name": "International", "flag": "🌍"}

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Bot: ONLINE"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("📞 Get Number", "🎯 Custom Range", "🖥️ Console", "📊 Stats")
    return markup

# --- OTP POLLING ---
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    active_sessions[chat_id] = num
    
    while time.time() - start_time < 600:
        if chat_id not in active_sessions or active_sessions[chat_id] != num:
            return

        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        raw_msg = o['message']
                        otp_match = re.search(r'\d{4,8}', raw_msg)
                        code = otp_match.group() if otp_match else raw_msg
                        
                        bot.send_message(chat_id, 
                            f"⚡️ **OTP RECEIVED!**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{code}`\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"💡 *Tap to copy code.*", parse_mode="Markdown")
                        
                        # Log to Group
                        log = (f"📢 **SUCCESSFUL ACTIVATION**\n"
                               f"👤 User: {user_name}\n"
                               f"📱 Number: `{num}`\n"
                               f"🔑 OTP: `{code}`\n"
                               f"🌐 Service: {service_name}")
                        bot.send_message(GROUP_ID, log, parse_mode="Markdown")
                        
                        if chat_id in active_sessions: del active_sessions[chat_id]
                        return
        except: pass
        time.sleep(8)

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = (f"👋 **Hello {message.from_user.first_name}!**\n\n"
               f"Welcome to **Borhan Premium OTP**.\n"
               f"Instant numbers for WhatsApp, Facebook & more.\n\n"
               f"👨‍💻 **Dev:** [BORHAN](https://t.me/BORHANSB)")
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu(), parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_service(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📘 Facebook", callback_data="select_facebook"))
    markup.add(types.InlineKeyboardButton("🟢 WhatsApp", callback_data="select_whatsapp"))
    bot.send_message(m.chat.id, "💎 **Choose Service:**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def show_countries(call):
    service_type = call.data.split("_")[1]
    bot.edit_message_text(f"🔍 Analyzing global traffic for {service_type.upper()}...", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            markup = types.InlineKeyboardMarkup(row_width=1)
            seen = set()
            target_keys = ["fb", "facebook"] if service_type=="facebook" else ["wa", "whatsapp"]
            
            for s in res['data']['services']:
                if any(k in s['sid'].lower() for k in target_keys):
                    for r in s['ranges']:
                        info = get_flag_info(r)
                        if info['name'] not in seen:
                            rid = r.replace("X", "")
                            markup.add(types.InlineKeyboardButton(f"{info['flag']} {info['name']} ({r})", callback_data=f"buy_{s['sid']}_{rid}"))
                            seen.add(info['name'])
                        if len(seen) >= 15: break
            
            bot.edit_message_text(f"🌍 **Available Countries ({service_type.title()}):**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_") or call.data.startswith("change_"))
def buy_number(call):
    parts = call.data.split("_")
    sid, rid = parts[1], parts[2]
    chat_id = call.message.chat.id
    
    if chat_id in active_sessions: del active_sessions[chat_id]
    
    bot.edit_message_text("⏳ **Securing new number...**", chat_id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            data = res['data']
            num = data['no_plus_number']
            info = get_flag_info(num)
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{sid}_{rid}"))
            markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_order"))
            markup.add(types.InlineKeyboardButton("📢 Join Channel", url=GROUP_LINK))

            msg = (f"✅ **Number Purchased!**\n━━━━━━━━━━━━━━━━━━\n"
                   f"🌍 Country: {info['flag']} {info['name']}\n"
                   f"📱 Number: `{data['full_number']}`\n"
                   f"🌐 Service: {sid}\n━━━━━━━━━━━━━━━━━━\n"
                   f"⏳ *Monitoring for incoming OTP...*")
            
            bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(chat_id, num, call.from_user.first_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Stock Alert:** {res['message']}", chat_id, call.message.message_id)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "cancel_order")
def cancel_order(call):
    chat_id = call.message.chat.id
    if chat_id in active_sessions: del active_sessions[chat_id]
    bot.edit_message_text("❌ **Order cancelled successfully.**", chat_id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text == "🎯 Custom Range")
def custom_range(m):
    msg = bot.send_message(m.chat.id, "🎯 **Enter Range Prefix (e.g., 88017):**", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_custom)

def process_custom(m):
    rid = m.text.strip()
    info = get_flag_info(rid)
    loading = bot.send_message(m.chat.id, f"⏳ Searching {info['flag']} {info['name']} number...")
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            data = res['data']
            bot.edit_message_text(f"✅ **Purchased:** `{data['full_number']}`\n🌍 {info['flag']} {info['name']}", m.chat.id, loading.message_id, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(m.chat.id, data['no_plus_number'], m.from_user.first_name, "Custom")).start()
        else: bot.edit_message_text("❌ This range is out of stock.", m.chat.id, loading.message_id)
    except: pass

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            text = "🖥️ **Live Global Traffic:**\n\n"
            for h in res['data'].get('hits', [])[:10]:
                info = get_flag_info(h['range'])
                text += f"{info['flag']} `{h['range']}` | {h['sid']}\n"
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
    except: pass

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats(m):
    text = (f"📊 **Bot Status:** Online\n"
            f"⚡ **Speed:** High Performance\n"
            f"👨‍💻 **Dev:** [BORHAN](https://t.me/BORHANSB)")
    bot.reply_to(m, text, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan Global OTP Bot is Running...")
    bot.polling(none_stop=True)
