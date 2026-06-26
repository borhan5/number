import telebot
import requests
import time
import threading
import re
from flask import Flask
from telebot import types
from waitress import serve

# --- কনফিগারেশন ---
BOT_TOKEN = '8953289994:AAHTHGnduASu43Q5fX4TOXq_ajXEDaNC6f8'
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
    # নাম্বারের মাঝের অংশ ঢেকে দেওয়া (উদাহরণ: 88017***12)
    if len(num) > 7:
        return f"{num[:5]}***{num[-2:]}"
    return num

# --- ওয়েব সার্ভার (বট সচল রাখতে) ---
app = Flask('')
@app.route('/')
def home(): return "Borhan Live Traffic Bot is Running"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- মেইন মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("🎯 Custom Range"),
        types.KeyboardButton("🖥️ Console"), types.KeyboardButton("📊 Stats")
    )
    return markup

# --- ওটিপি চেক ফাংশন ---
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    while time.time() - start_time < 600: # ১০ মিনিট ট্রাই করবে
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                for o in r['data'].get('otps', []):
                    if str(o['number']) == str(num):
                        raw_msg = o['message']
                        # ফেসবুক হলে শুধু কোড, বাকি সব ফুল মেসেজ
                        display_msg = extract_fb_code(raw_msg) if "facebook" in service_name.lower() else raw_msg
                        
                        otp_msg = (
                            f"⚡️ **Borhan OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{display_msg}`\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        # গ্রুপে লগ পাঠানো (মাস্কিং নাম্বার সহ)
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
    bot.send_message(message.chat.id, "🤖 **Welcome to Borhan Live Traffic!**", reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def select_service_screen(m):
    # ফেসবুক এবং ইন্সটাগ্রাম একই রো-তে, হোয়াটসঅ্যাপ নিচে
    markup = types.InlineKeyboardMarkup()
    btn_fb = types.InlineKeyboardButton("📘 Facebook", callback_data="all_facebook")
    btn_ig = types.InlineKeyboardButton("📸 Instagram", callback_data="all_instagram")
    btn_wa = types.InlineKeyboardButton("🟢 WhatsApp", callback_data="all_whatsapp")
    
    markup.row(btn_fb, btn_ig)
    markup.row(btn_wa)
    
    bot.send_message(m.chat.id, "💎 **Select Service (Live Traffic):**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("all_"))
def show_live_traffic_ranges(call):
    service_key = call.data.split("_")[1]
    bot.edit_message_text(f"⏳ {service_key.capitalize()} এর সকল দেশের লাইভ ট্রাফিক চেক হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            # শুধুমাত্র সিলেক্টেড সার্ভিসের (সব দেশ) রেঞ্জগুলো ফিল্টার করা
            filtered_ranges = [s for s in services if service_key in s['sid'].lower()]
            
            if filtered_ranges:
                markup = types.InlineKeyboardMarkup(row_width=1)
                for s in filtered_ranges:
                    for r in s['ranges']:
                        rid = r.replace("XXX", "")
                        # বাটন টেক্সটে রেঞ্জ এবং "Live Traffic" হাইলাইট
                        markup.add(types.InlineKeyboardButton(f"📡 {s['sid']} - Live Traffic: {r}", callback_data=f"buy_{s['sid']}_{rid}"))
                
                bot.edit_message_text(f"📍 **{service_key.capitalize()} - All Country Ranges**\nনিচে থেকে একটি রেঞ্জ সিলেক্ট করুন:", 
                                     call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(f"❌ বর্তমানে {service_key} এর কোনো লাইভ রেঞ্জ নেই।", call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, "❌ ডাটা কানেকশন সমস্যা!")

@bot.callback_query_handler(func=lambda call: call.data.startswith(("buy_", "change_")))
def buy_process(call):
    data = call.data.split("_")
    sid, rid = data[1], data[2]
    user_name = call.from_user.first_name
    
    bot.edit_message_text(f"⏳ **লাইভ নাম্বার চেক হচ্ছে...**", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS).json()
        if res['meta']['code'] == 200:
            num_data = res['data']
            full_num = num_data['full_number']
            clean_num = num_data['no_plus_number']
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{sid}_{rid}"),
                types.InlineKeyboardButton("🔙 Back to Ranges", callback_data=f"all_{sid.lower()}")
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
            
            # ওটিপি ট্র্যাকিং শুরু
            threading.Thread(target=poll_otp, args=(call.message.chat.id, clean_num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Stock Out:** {res['message']}", call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, "❌ সার্ভার এরর।")

# --- বট স্টার্ট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan Full Live Traffic Bot is Starting...")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            time.sleep(10)
