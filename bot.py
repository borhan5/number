import telebot
import requests
import time
import threading
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8942060883:AAH6VqwhkD4_FILqIQzrvluwhboPJY_R9qg'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- কান্ট্রি ম্যাপ (Prefix অনুযায়ী দেশ ও ফ্ল্যাগ) ---
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

# --- ওয়েব সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Bot is Running"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- মেইন মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("💰 Balance"),
        types.KeyboardButton("🖥️ Console"), types.KeyboardButton("📊 Stats")
    )
    return markup

# --- ওটিপি চেক ফাংশন ---
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        otp_msg = (
                            f"⚡️ **Borhan OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        group_log = (
                            f"📢 **Borhan OTP Success**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num[:6]}***{num[-2:]}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"🌐 Service: {service_name}\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        return
        except: pass
        time.sleep(10)

# --- স্টার্ট কমান্ড ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"🤖 **Welcome {message.from_user.first_name}!**\n\nনিচের বাটন থেকে আপনার প্রয়োজনীয় দেশ সিলেক্ট করে নাম্বার নিন।"
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu(), parse_mode="Markdown")

# --- অটোমেটিক কান্ট্রি ও রেঞ্জ ভিত্তিক নাম্বার বাটন ---
@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_service(m):
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            
            # ৫টি ভিন্ন দেশের রেঞ্জ বাছাই করা
            unique_countries = []
            seen_prefixes = set()
            
            for s in services:
                for r in s['ranges']:
                    # প্রথম ৩ ডিজিট দিয়ে দেশ চেনা (Prefix)
                    prefix = r[:3]
                    if prefix not in seen_prefixes:
                        info = get_country_info(r)
                        unique_countries.append({
                            "name": info['name'],
                            "flag": info['flag'],
                            "range": r,
                            "sid": s['sid']
                        })
                        seen_prefixes.add(prefix)
                    if len(unique_countries) >= 5: break
                if len(unique_countries) >= 5: break

            if not unique_countries:
                bot.send_message(m.chat.id, "❌ বর্তমানে কোনো স্টোক নেই।")
                return

            markup = types.InlineKeyboardMarkup(row_width=1)
            for item in unique_countries:
                btn_text = f"{item['flag']} {item['name']} ({item['range']})"
                # callback_data: buy_ServiceName_RangeID
                rid = item['range'].replace("XXX", "")
                markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"buy_{item['sid']}_{rid}"))
            
            bot.send_message(m.chat.id, "🌍 **বেস্ট ট্রাফিক কান্ট্রি লিস্ট:**\nএকটি দেশ সিলেক্ট করুন:", reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(m.chat.id, "❌ ডাটা লোড করতে সমস্যা হয়েছে।")

# --- নাম্বার কেনার প্রসেস ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_callback(call):
    _, sid, rid = call.data.split("_")
    user_name = call.from_user.first_name
    chat_id = call.message.chat.id
    
    bot.edit_message_text(f"⏳ **নাম্বার তোলা হচ্ছে...**", chat_id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num_data = res['data']
            full_num = num_data['full_number']
            clean_num = num_data['no_plus_number']
            country = num_data['country']
            
            response_text = (
                f"✅ **নাম্বার রেডি!**\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"🌍 **Country:** {country}\n"
                f"📱 **Number:** `{full_num}`\n"
                f"━━━━━━━━━━━━━━\n"
                f"⏳ ওটিপির জন্য অপেক্ষা করুন..."
            )
            bot.edit_message_text(response_text, chat_id, call.message.message_id, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(chat_id, clean_num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **ব্যর্থ:** {res['message']}", chat_id, call.message.message_id)
    except:
        bot.send_message(chat_id, "❌ এরর! আবার চেষ্টা করুন।")

# --- অন্যান্য বাটন ---
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def check_balance(m):
    bot.reply_to(m, "💳 আপনার অ্যাকাউন্টে পর্যাপ্ত ব্যালেন্স আছে।")

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def show_console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            text = "🖥️ **Live Traffic:**\n\n"
            for h in hits[:5]:
                text += f"🔹 {h['sid']} | `{h['range']}` | ✅ Success\n"
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
    except: pass

# --- বট স্টার্ট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan OTP Bot is Running...")
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
