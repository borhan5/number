import telebot
import requests
import time
import threading
import re  # ওটিপি কোড খুঁজে বের করার জন্য রেজেক্স ইম্পোর্ট করা হয়েছে
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8942060883:AAHYvPhZZspoVTsr_Uh2SpIkkV4plCW1L5s'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# ওটিপি গ্রুপ ও লিঙ্ক
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- কান্ট্রি ম্যাপ ---
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

# --- ওটিপি চেক ফাংশন (আপডেটেড) ---
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    while time.time() - start_time < 600:
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        # মেসেজ থেকে ৫ বা ৬ ডিজিটের কোড খুঁজে বের করার লজিক
                        raw_message = o['message']
                        # \d{5,6} মানে হচ্ছে পরপর ৫ অথবা ৬ টি সংখ্যা খুঁজবে
                        otp_match = re.search(r'\d{5,6}', raw_message)
                        
                        if otp_match:
                            extracted_code = otp_match.group() # শুধু কোডটি নিবে
                        else:
                            extracted_code = raw_message # যদি কোড না পায় তবে পুরো মেসেজ দিবে

                        otp_msg = (
                            f"⚡️ **Borhan OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 OTP Code: `{extracted_code}`\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"💡 *কোডের ওপর ক্লিক করলে কপি হয়ে যাবে।*"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        group_log = (
                            f"📢 **Borhan OTP Success**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num[:6]}***{num[-2:]}`\n"
                            f"🔑 Code: `{extracted_code}`\n"
                            f"🌐 Service: {service_name}\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        return
        except: pass
        time.sleep(10)

# --- কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"🤖 **Welcome {message.from_user.first_name}!**\n\nবোরহান ওটিপি সার্ভিস থেকে Facebook এবং WhatsApp এর নাম্বার নিন।"
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu(), parse_mode="Markdown")

# --- স্টেপ ১: সার্ভিস সিলেকশন (FB/WA) ---
@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_main_service(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📘 Facebook", callback_data="select_facebook"))
    markup.add(types.InlineKeyboardButton("🟢 WhatsApp", callback_data="select_whatsapp"))
    bot.send_message(m.chat.id, "📱 **কোন সার্ভিসের নাম্বার প্রয়োজন?**", reply_markup=markup)

# --- স্টেপ ২: দেশ সিলেকশন ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def select_country_for_service(call):
    service_type = call.data.split("_")[1]
    bot.edit_message_text(f"⏳ {service_type.capitalize()} এর জন্য সেরা দেশগুলো খোঁজা হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            all_services = res['data']['services']
            target_keywords = ["fb", "facebook"] if service_type == "facebook" else ["wa", "whatsapp"]
            filtered_services = [s for s in all_services if any(k in s['sid'].lower() for k in target_keywords)]
            
            unique_countries = []
            seen_prefixes = set()
            
            for s in filtered_services:
                for r in s['ranges']:
                    prefix = r[:3]
                    if prefix not in seen_prefixes:
                        info = get_country_info(r)
                        unique_countries.append({"name": info['name'], "flag": info['flag'], "range": r, "sid": s['sid']})
                        seen_prefixes.add(prefix)
                    if len(unique_countries) >= 5: break
                if len(unique_countries) >= 5: break

            if not unique_countries:
                bot.edit_message_text(f"❌ বর্তমানে {service_type.capitalize()} এর জন্য কোনো দেশ এভেইলবল নেই।", call.message.chat.id, call.message.message_id)
                return

            markup = types.InlineKeyboardMarkup(row_width=1)
            for item in unique_countries:
                rid = item['range'].replace("XXX", "")
                markup.add(types.InlineKeyboardButton(f"{item['flag']} {item['name']} ({item['range']})", callback_data=f"buy_{item['sid']}_{rid}"))
            
            bot.edit_message_text(f"🌍 **{service_type.capitalize()} এর জন্য দেশ সিলেক্ট করুন:**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "❌ ডাটা লোড করতে সমস্যা হয়েছে।")

# --- স্টেপ ৩: নাম্বার কেনা ---
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
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 New Number", callback_data=f"buy_{sid}_{rid}"))
            markup.add(types.InlineKeyboardButton("📢 Join OTP Group", url=GROUP_LINK))
            
            response_text = (
                f"✅ **নাম্বার পাওয়া গেছে!**\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"🌍 **Country:** {country}\n"
                f"📱 **Number:** `{full_num}`\n"
                f"🧩 **Service:** {sid}\n"
                f"━━━━━━━━━━━━━━\n"
                f"⏳ ওটিপির জন্য অপেক্ষা করুন..."
            )
            bot.edit_message_text(response_text, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(chat_id, clean_num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Stock Out:** {res['message']}", chat_id, call.message.message_id)
    except: pass

# --- অন্যান্য ফাংশন ---
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def check_balance(m):
    bot.reply_to(m, "💳 অ্যাকাউন্টে ব্যালেন্স চেক করতে অ্যাডমিনের সাথে যোগাযোগ করুন।")

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

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan OTP Bot is Starting...")
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
