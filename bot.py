import telebot
import requests
import time
import threading
import re
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8953289994:AAF_s1M9_kcPufc4bmo_FIOcTdiL3YzxNtA'
API_KEY = 'MQGVM5B5OOW'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# ওটিপি গ্রুপ ও লিঙ্ক
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- হেল্পার ফাংশন ---
def extract_fb_code(text):
    # ফেসবুক মেসেজ থেকে শুধু ৬ ডিজিটের কোড বের করার জন্য
    match = re.search(r'\b\d{6}\b', text)
    return match.group(0) if match else text

def mask_number(num):
    # নাম্বারের মাঝের অংশ ঢেকে দেওয়া (নিরাপত্তার জন্য)
    if len(num) > 7:
        return f"{num[:5]}***{num[-2:]}"
    return num

# --- ওয়েব সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Pro is Online"
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
                        raw_msg = o['message']
                        display_msg = extract_fb_code(raw_msg) if "facebook" in service_name.lower() else raw_msg
                        
                        otp_msg = (
                            f"⚡️ **Borhan OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{display_msg}`\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        group_log = (
                            f"📢 **Borhan OTP Success**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{mask_number(num)}`\n"
                            f"🔑 Code: `{display_msg}`\n"
                            f"🌐 Service: {service_name.capitalize()}\n"
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
    bot.send_message(message.chat.id, "🤖 **Welcome to Borhan OTP!**\nসার্ভিস নিতে Get Number এ ক্লিক করুন।", 
                     reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def select_service_screen(m):
    markup = types.InlineKeyboardMarkup()
    btn_fb = types.InlineKeyboardButton("📘 Facebook", callback_data="svc_facebook")
    btn_ig = types.InlineKeyboardButton("📸 Instagram", callback_data="svc_instagram")
    btn_wa = types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_whatsapp")
    markup.row(btn_fb, btn_ig)
    markup.row(btn_wa)
    bot.send_message(m.chat.id, "💎 **Select Service:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("svc_"))
def show_countries(call):
    service_key = call.data.split("_")[1]
    bot.edit_message_text(f"⏳ {service_key.capitalize()} এর দেশসমূহ লোড হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        services = res['data']['services']
        country_options = [s for s in services if service_key in s['sid'].lower()]
        
        if country_options:
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = [types.InlineKeyboardButton(f"🌍 {s['sid'].replace(service_key,'').strip('-').upper()}", callback_data=f"cnt_{s['sid']}") for s in country_options]
            markup.add(*buttons)
            markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="back_main"))
            bot.edit_message_text(f"📍 **{service_key.capitalize()} - Select Country:**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "❌ কানেকশন এরর!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("cnt_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
    selected = next((s for s in res['data']['services'] if s['sid'] == sid), None)
    
    if selected:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for r in selected['ranges']:
            rid = r.replace("XXX", "")
            markup.add(types.InlineKeyboardButton(f"📡 Live Traffic: {r}", callback_data=f"buy_{sid}_{rid}"))
        bot.edit_message_text(f"📍 **Range List for {sid}:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

# --- Change Number ও Buy Process ---
@bot.callback_query_handler(func=lambda call: call.data.startswith(("buy_", "change_")))
def handle_number_request(call):
    action, sid, rid = call.data.split("_")
    user_name = call.from_user.first_name
    
    status_text = "🔄 নতুন নাম্বার নেওয়া হচ্ছে..." if action == "change" else "⏳ নাম্বার চেক হচ্ছে..."
    bot.edit_message_text(status_text, call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num_data = res['data']
            full_num = num_data['full_number']
            clean_num = num_data['no_plus_number']
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            # এখানে Change Number বাটনটি যুক্ত করা হয়েছে
            markup.add(
                types.InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{sid}_{rid}"),
                types.InlineKeyboardButton("🔙 Back to Countries", callback_data=f"svc_{sid.split('-')[0]}")
            )
            markup.add(types.InlineKeyboardButton("📢 Join OTP Group", url=GROUP_LINK))
            
            response_text = (
                f"✅ **নাম্বার পাওয়া গেছে!**\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"🌍 **Country:** {num_data['country']}\n"
                f"📱 **Number:** `{full_num}`\n"
                f"🧩 **Service:** {sid}\n"
                f"━━━━━━━━━━━━━━\n"
                f"⏳ **ওটিপির জন্য অপেক্ষা করুন...**"
            )
            bot.edit_message_text(response_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            threading.Thread(target=poll_otp, args=(call.message.chat.id, clean_num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Stock Out:** {res['message']}", call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, "❌ সার্ভার এরর।")

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_main(call):
    select_service_screen(call.message)

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan OTP Pro is Online...")
    bot.polling(none_stop=True)
