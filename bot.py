import telebot
import requests
import time
import threading
from flask import Flask
from telebot import types
from waitress import serve

# --- Render Web Server (Keep-alive) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive and Running 24/7"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- কনফিগারেশন ---
BOT_TOKEN = '8942060883:AAFkMA0cLr0-d38PlR2_kJ1oZagTGPs6PQ0'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- ১. নিচের মেইন মেনু বাটন ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("🗃️ Stock Number"),
        types.KeyboardButton("🛡️ Get 2FA"), types.KeyboardButton("📄 Extract OTP"),
        types.KeyboardButton("📊 Stats"), types.KeyboardButton("💰 Balance")
    )
    return markup

# --- ২. সার্ভিস সিলেক্ট করার মেনু ---
def service_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    # এখানে আপনার জনপ্রিয় সার্ভিসগুলো যোগ করা হয়েছে
    services = [
        ("🔵 Facebook", "ser_fb"), 
        ("🟢 WhatsApp", "ser_wa"),
        ("🟣 Instagram", "ser_ig"), 
        ("🔵 Telegram", "ser_tg")
    ]
    for name, data in services:
        markup.add(types.InlineKeyboardButton(name, callback_data=data))
    markup.add(types.InlineKeyboardButton("❌ Close", callback_data="close_menu"))
    return markup

# --- ৩. দেশ সিলেক্ট করার মেনু (আপনার স্ক্রিনশটের RID অনুযায়ী) ---
def country_menu(service_tag):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # আপনার স্ক্রিনশট থেকে পাওয়া আসল RID গুলো এখানে দেওয়া হলো
    countries = [
        ("🇧🇯 Benin", f"buy_{service_tag}_26134"),
        ("🇬🇳 Guinea", f"buy_{service_tag}_22465"),
        ("🇨🇮 Ivory Coast", f"buy_{service_tag}_2250787"),
        ("🇨🇫 Central African Rep.", f"buy_{service_tag}_23672"),
        ("🇲🇱 Mali", f"buy_{service_tag}_2236")
    ]
    for name, data in countries:
        markup.add(types.InlineKeyboardButton(name, callback_data=data))
    
    markup.add(
        types.InlineKeyboardButton("🔄 Refresh", callback_data=f"ser_{service_tag}"),
        types.InlineKeyboardButton("⬅️ Back", callback_data="back_to_services")
    )
    return markup

# --- কমান্ড ও টেক্সট হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    text = f"🤖 **The Profit Player** | 👋 Hello, {name}!\n✅ **Select a service from the buttons below:**"
    bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_text(m):
    if m.text == "📞 Get Number":
        bot.send_message(m.chat.id, "🐸 **Choose a service:**", reply_markup=service_menu())
    elif m.text == "💰 Balance":
        bot.send_message(m.chat.id, "💳 **Checking balance...**")
        # ব্যালেন্স দেখানোর এপিআই এখানে কল করতে পারেন

# --- ইনলাইন বাটন হ্যান্ডলার ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "close_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    elif call.data == "back_to_services":
        bot.edit_message_text("🐸 **Choose a service:**", call.message.chat.id, call.message.message_id, reply_markup=service_menu())

    elif call.data.startswith("ser_"):
        service_tag = call.data.split("_")[1]
        service_name = service_tag.upper()
        text = f"🌐 **{service_name} Service**\n━━━━━━━━━━━━━━\n•ʟɪᴠᴇ **Countries available**\n\n🍰 *Select a country to get number:*"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=country_menu(service_tag), parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        _, service, rid = call.data.split("_")
        bot.edit_message_text(f"⏳ **Requesting number...**\nService: `{service.upper()}` | RID: `{rid}`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        try:
            # API Call
            res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS, timeout=15).json()
            if res['meta']['code'] == 200:
                num = res['data']['no_plus_number']
                full_num = res['data']['full_number']
                country = res['data']['country']
                
                success_text = (
                    f"✅ **Number Received!**\n\n"
                    f"📱 Number: `{full_num}`\n"
                    f"🌍 Country: {country}\n"
                    f"━━━━━━━━━━━━━━\n"
                    f"⏳ Waiting for OTP... (Auto-checks for 5 mins)"
                )
                bot.edit_message_text(success_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
                
                # OTP চেক করার জন্য আলাদা থ্রেড শুরু
                threading.Thread(target=poll_otp, args=(call.message.chat.id, num)).start()
            else:
                bot.answer_callback_query(call.id, f"❌ Error: {res['message']}", show_alert=True)
                bot.edit_message_text(f"❌ **Failed to get number.**\nReason: {res['message']}", call.message.chat.id, call.message.message_id)
        except:
            bot.answer_callback_query(call.id, "⚠️ API Server Error!", show_alert=True)

def poll_otp(chat_id, num):
    start_time = time.time()
    while time.time() - start_time < 300: # ৫ মিনিট চেক করবে
        try:
            response = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if response['meta']['code'] == 200:
                for item in response['data'].get('otps', []):
                    if str(item['number']) == str(num):
                        bot.send_message(
                            chat_id, 
                            f"📩 **New OTP Received!**\n\n📱 Number: `{num}`\n🔑 Code: `{item['message']}`", 
                            parse_mode="Markdown"
                        )
                        return
        except: pass
        time.sleep(10) # প্রতি ১০ সেকেন্ড অন্তর চেক

# --- রান করার মেইন ফাংশন ---
if __name__ == "__main__":
    # Web server চালু করা (Render এর জন্য)
    threading.Thread(target=run_web_server).start()
    
    # বট পোলিং (২৪ ঘণ্টা সচল রাখার জন্য লুপ)
    while True:
        try:
            print("Bot is Polling...")
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=0, timeout=40)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
@bot.message_handler(commands=['get'])
def buy_number(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ সঠিক নিয়ম: `/get 26134`", parse_mode="Markdown")
        return

    rid = args[1]
    status_msg = bot.reply_to(message, "🔍 নাম্বার খোঁজা হচ্ছে...")

    try:
        response = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS, timeout=15)
        res_data = response.json()

        if res_data['meta']['code'] == 200:
            num_info = res_data['data']
            number = num_info['no_plus_number']
            full_num = num_info['full_number']
            country = num_info['country']

            bot.edit_message_text(
                f"✅ **নাম্বার পাওয়া গেছে!**\n📱 `{full_num}`\n🌍 {country}\n\n⏳ OTP আসলে মেসেজ দেওয়া হবে (৫ মিনিট চেক করবে)...",
                message.chat.id, status_msg.message_id, parse_mode="Markdown"
            )
            
            # OTP চেক করার জন্য আলাদা থ্রেড শুরু
            threading.Thread(target=poll_otp, args=(message.chat.id, number)).start()
        else:
            bot.edit_message_text(f"❌ এরর: {res_data.get('message', 'ব্যালেন্স নেই')}", message.chat.id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"⚠️ সার্ভার সমস্যা। আবার চেষ্টা করুন।", message.chat.id, status_msg.message_id)

def poll_otp(chat_id, target_number):
    start_time = time.time()
    while time.time() - start_time < 300: # ৫ মিনিট
        try:
            response = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10)
            data = response.json()
            if data['meta']['code'] == 200:
                otps = data['data'].get('otps', [])
                for item in otps:
                    if str(item['number']) == str(target_number):
                        bot.send_message(chat_id, f"📩 **OTP এসে গেছে!**\n📱 নাম্বার: `{target_number}`\n🔑 কোড: `{item['message']}`", parse_mode="Markdown")
                        return
        except: pass
        time.sleep(10)
    bot.send_message(chat_id, f"⏰ সময় শেষ! `{target_number}`-এ কোনো OTP আসেনি।")

# --- ২৪ ঘণ্টা চালানোর লুপ ---
def start_bot():
    while True:
        try:
            print("Bot is polling...")
            bot.remove_webhook() # Conflict মেটানোর জন্য
            bot.polling(none_stop=True, interval=0, timeout=40)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Web server চালু করা (Render এর জন্য)
    threading.Thread(target=run_web_server).start()
    # বট চালু করা
    start_bot()
