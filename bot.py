import telebot
import requests
import time
import threading
import re
from flask import Flask
from telebot import types
from waitress import serve

# --- CONFIGURATION ---
BOT_TOKEN = '8953289994:AAHalks0v_QNWta40jorqobnfwS1trW8pJQ'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# Group Log Settings
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- COUNTRY DATA ---
COUNTRY_MAP = {
    "225": {"name": "Ivory Coast", "flag": "🇨🇮"},
    "229": {"name": "Benin", "flag": "🇧🇯"},
    "224": {"name": "Guinea", "flag": "🇬🇳"},
    "234": {"name": "Nigeria", "flag": "🇳🇬"},
    "44": {"name": "United Kingdom", "flag": "🇬🇧"},
    "1": {"name": "USA/Canada", "flag": "🇺🇸"},
    "880": {"name": "Bangladesh", "flag": "🇧🇩"},
    "91": {"name": "India", "flag": "🇮🇳"},
    "84": {"name": "Vietnam", "flag": "🇻🇳"},
    "233": {"name": "Ghana", "flag": "🇬🇭"},
    "236": {"name": "Central Africa", "flag": "🇨🇫"}
}

def get_country_info(range_val):
    for prefix, info in COUNTRY_MAP.items():
        if range_val.startswith(prefix):
            return info
    return {"name": "Unknown", "flag": "🌍"}

# --- WEB SERVER FOR UPTIME ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Bot is Running"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("🎯 Custom Range"),
        types.KeyboardButton("🖥️ Console"), types.KeyboardButton("📊 Stats")
    )
    return markup

# --- OTP POLLING LOGIC ---
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    # 10 Minute Timeout
    while time.time() - start_time < 600:
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        raw_message = o['message']
                        otp_match = re.search(r'\d{5,6}', raw_message)
                        extracted_code = otp_match.group() if otp_match else raw_message

                        otp_msg = (
                            f"⚡️ **OTP RECEIVED!**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📱 **Number:** `{num}`\n"
                            f"🔑 **OTP Code:** `{extracted_code}`\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"💡 *Tap the code to copy.*"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        group_log = (
                            f"📢 **SUCCESSFUL ACTIVATION**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num[:6]}***{num[-2:]}`\n"
                            f"🔑 Code: `{extracted_code}`\n"
                            f"🌐 Service: {service_name}\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━━━━━"
                        )
                        bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        return
        except: pass
        time.sleep(8)

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"👋 **Hello {message.from_user.first_name}!**\n\n"
        f"Welcome to **Borhan Premium OTP**. Get high-quality virtual numbers "
        f"for Facebook and WhatsApp instantly."
    )
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_service(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📘 Facebook", callback_data="select_facebook"))
    markup.add(types.InlineKeyboardButton("🟢 WhatsApp", callback_data="select_whatsapp"))
    bot.send_message(m.chat.id, "💎 **Choose Service Type:**", reply_markup=markup)

# --- CUSTOM RANGE FEATURE ---
@bot.message_handler(func=lambda m: m.text == "🎯 Custom Range")
def custom_range_prompt(m):
    msg = bot.send_message(m.chat.id, "🎯 **Enter Custom Range Prefix:**\nExample: `22467XXX`", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_custom_range)

def process_custom_range(message):
    rid = message.text.strip()
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    if len(rid) < 4:
        bot.send_message(chat_id, "❌ Invalid Range Format.")
        return

    loading = bot.send_message(chat_id, f"⏳ Requesting number for range: `{rid}`...", parse_mode="Markdown")
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num_data = res['data']
            full_num = num_data['full_number']
            clean_num = num_data['no_plus_number']
            
            response_text = (
                f"✅ **Number Purchased!**\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🌍 **Country:** {num_data['country']}\n"
                f"📱 **Number:** `{full_num}`\n"
                f"🎯 **Range:** {rid}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⏳ Waiting for OTP code..."
            )
            bot.edit_message_text(response_text, chat_id, loading.message_id, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(chat_id, clean_num, user_name, "Custom Range")).start()
        else:
            bot.edit_message_text(f"❌ **Error:** {res.get('message', 'Stock Out')}", chat_id, loading.message_id)
    except:
        bot.send_message(chat_id, "❌ API Connection Error.")

# --- CALLBACKS ---

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def show_countries(call):
    service_type = call.data.split("_")[1]
    bot.edit_message_text(f"🔍 Searching best ranges for {service_type.upper()}...", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            all_services = res['data']['services']
            target = ["fb", "facebook"] if service_type == "facebook" else ["wa", "whatsapp"]
            filtered = [s for s in all_services if any(k in s['sid'].lower() for k in target)]
            
            unique_countries = []
            seen = set()
            for s in filtered:
                for r in s['ranges']:
                    prefix = r[:3]
                    if prefix not in seen:
                        info = get_country_info(r)
                        unique_countries.append({"info": info, "range": r, "sid": s['sid']})
                        seen.add(prefix)
                    if len(unique_countries) >= 6: break
            
            if not unique_countries:
                bot.edit_message_text("❌ No stock available currently.", call.message.chat.id, call.message.message_id)
                return

            markup = types.InlineKeyboardMarkup(row_width=1)
            for item in unique_countries:
                rid = item['range'].replace("XXX", "")
                btn_text = f"{item['info']['flag']} {item['info']['name']} ({item['range']})"
                markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"buy_{item['sid']}_{rid}"))
            
            bot.edit_message_text(f"🌍 **Select {service_type.title()} Region:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(call.message.chat.id, "❌ Failed to fetch country list.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_number(call):
    _, sid, rid = call.data.split("_")
    chat_id = call.message.chat.id
    user_name = call.from_user.first_name
    
    bot.edit_message_text("⏳ **Generating Number...**", chat_id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            data = res['data']
            clean_num = data['no_plus_number']
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Get Another", callback_data=f"buy_{sid}_{rid}"))
            markup.add(types.InlineKeyboardButton("📢 Join Channel", url=GROUP_LINK))
            
            msg = (
                f"✅ **Ready to use!**\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📱 **Number:** `{data['full_number']}`\n"
                f"🌐 **Service:** {sid}\n"
                f"🌍 **Region:** {data['country']}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⏳ System is monitoring for OTP..."
            )
            bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(chat_id, clean_num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Stock Alert:** {res['message']}", chat_id, call.message.message_id)
    except: pass

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            text = "📊 **Live Network Traffic:**\n\n"
            for h in hits[:6]:
                text += f"🔹 {h['sid']} | `{h['range']}` | ✅ Active\n"
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
    except: bot.reply_to(m, "❌ Console unavailable.")

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats(m):
    bot.reply_to(m, "📈 **Server Status:** Online\n⚡ **Speed:** Ultra Fast\n🛡️ **Status:** Secure")

# --- START BOT ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan OTP Bot Started Successfully!")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(5)
