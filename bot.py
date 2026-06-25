import telebot
import requests
import time
import threading
from flask import Flask

# --- Render-এর জন্য Web Server (Keep-alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- কনফিগারেশন (আপনার নতুন টোকেন ও এপিআই কী) ---
BOT_TOKEN = '8942060883:AAFkMA0cLr0-d38PlR2_kJ1oZagTGPs6PQ0'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {
    'mauthapi': API_KEY,
    'Content-Type': 'application/json'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 **VoltxSMS Bot Active!**\n\n"
        "নাম্বার কিনতে নিচের কমান্ডটি দিন:\n"
        "`/get rid_নাম্বার` (যেমন: `/get 26134`)\n\n"
        "💡 ব্যালেন্স বা RID চেক করতে সাইটের ড্যাশবোর্ড দেখুন।"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

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
