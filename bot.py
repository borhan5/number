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

# ওটিপি লগের জন্য গ্রুপ ডিটেইলস
GROUP_ID = -1003968881110 
GROUP_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl"

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- বট সচল রাখার জন্য ওয়েব সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Borhan OTP Bot is Active"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# নাম্বার মাস্কিং (প্রাইভেসি)
def mask_number(num_str):
    num_str = str(num_str)
    if len(num_str) > 8:
        return f"{num_str[:5]}***{num_str[-4:]}"
    return num_str

# মেইন মেনু
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("🖥️ Console"),
        types.KeyboardButton("💰 Balance"), types.KeyboardButton("📊 Stats")
    )
    return markup

# ওটিপি পোলিং ফাংশন
def poll_otp(chat_id, num, user_name, service_name):
    start_time = time.time()
    while time.time() - start_time < 600: # ১০ মিনিট চেক করবে
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                otps = r['data'].get('otps', [])
                for o in otps:
                    if str(o['number']) == str(num):
                        # ইউজারকে ওটিপি পাঠানো
                        otp_msg = (
                            f"📩 **Borhan OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"🌐 Service: {service_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        # গ্রুপে মাস্ক করা ওটিপি লগ
                        masked_num = mask_number(num)
                        group_log = (
                            f"📢 **Borhan OTP - New Hit**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{masked_num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"🌐 Service: {service_name}\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        try:
                            bot.send_message(GROUP_ID, group_log, parse_mode="Markdown")
                        except: pass
                        return
        except: pass
        time.sleep(10)

# --- হ্যান্ডলারসমূহ ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        f"🤖 **Welcome to Borhan OTP Bot!**\n\n"
        f"Hello {message.from_user.first_name}, বোরহান ওটিপি সার্ভিস থেকে সার্ভিস সিলেক্ট করুন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def choose_service(m):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # শুধুমাত্র FB, WA, IG বাটন
    markup.add(
        types.InlineKeyboardButton("🔵 Facebook", callback_data="ser_Facebook"),
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="ser_WhatsApp"),
        types.InlineKeyboardButton("🟣 Instagram", callback_data="ser_Instagram")
    )
    bot.send_message(m.chat.id, "🛒 **Borhan OTP - একটি সেবা নির্বাচন করুন:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    bot.answer_callback_query(call.id, "রেঞ্জ চেক করা হচ্ছে...")
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            # সার্ভিস খুঁজে বের করা
            selected = next((item for item in services if item['sid'].lower() == sid.lower()), None)
            
            if selected:
                markup = types.InlineKeyboardMarkup(row_width=1)
                for r in selected['ranges']:
                    rid = r.replace("XXX", "")
                    markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_{sid}_{rid}"))
                bot.edit_message_text(f"🌐 **Borhan OTP - {sid}**\nএকটি রেঞ্জ সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)
            else:
                bot.edit_message_text(f"❌ এই মুহূর্তে **{sid}** এর জন্য কোনো রেঞ্জ নেই।", call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, "❌ API সংযোগ বিচ্ছিন্ন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_number(call):
    _, sid, rid = call.data.split("_")
    user_name = call.from_user.first_name
    bot.edit_message_text(f"⏳ **Borhan OTP** থেকে আপনার নাম্বার রেডি হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS, timeout=20).json()
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            full_num = res['data']['full_number']
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📢 Join Borhan OTP Group", url=GROUP_LINK))
            
            bot.edit_message_text(
                f"✅ **নাম্বার পাওয়া গেছে!**\n\n"
                f"📱 Number: `{full_num}`\n"
                f"🌐 Service: {sid}\n"
                f"⏳ ওটিপির জন্য ১০ মিনিট অপেক্ষা করুন...\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"নিচের বাটনে ক্লিক করে আমাদের গ্রুপে জয়েন করুন।", 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
            
            # ব্যাকগ্রাউন্ডে ওটিপি চেক শুরু
            threading.Thread(target=poll_otp, args=(call.message.chat.id, num, user_name, sid)).start()
        else:
            bot.edit_message_text(f"❌ **Error:** {res.get('message', 'নাম্বার পাওয়া যায়নি')}", call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, f"❌ রিকোয়েস্ট ফেইল হয়েছে।")

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(m):
    bot.reply_to(m, "💰 ব্যালেন্স জানতে অ্যাডমিনের সাথে যোগাযোগ করুন।")

@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def console_view(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            text = "🖥️ **Borhan OTP - Live Hits:**\n\n"
            for h in hits[:5]:
                text += f"🔹 {h['sid']} | Range: `{h['range']}`\n"
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
    except: pass

# --- বট স্টার্ট ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Borhan OTP Bot is Running...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except:
            time.sleep(10)
