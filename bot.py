import telebot
import requests
import time
import threading
from flask import Flask
from telebot import types
from waitress import serve
from datetime import datetime

# --- Render Web Server (বটকে ২৪ ঘণ্টা জাগিয়ে রাখার জন্য) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive and Running"
def run_web_server(): serve(app, host='0.0.0.0', port=8080)

# --- কনফিগারেশন ---
# আপনার নতুন টোকেনটি এখানে বসানো হয়েছে
BOT_TOKEN = '8942060883:AAEkcbE5sQuWs9xiAkxftDdONPkTYSuFcr8'
API_KEY = 'MSVB8RMSMQK'
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

# ওটিপি ফরওয়ার্ড করার জন্য আপনার গ্রুপ আইডি
GROUP_ID = 3968881110 

bot = telebot.TeleBot(BOT_TOKEN)
HEADERS = {'mauthapi': API_KEY, 'Content-Type': 'application/json'}

# --- মেইন মেনু (নিচের বাটন) ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📞 Get Number"), types.KeyboardButton("🖥️ Console"),
        types.KeyboardButton("💰 Balance"), types.KeyboardButton("📊 Stats")
    )
    return markup

# চ্যাট আইডি বা গ্রুপ আইডি বের করার কমান্ড
@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(message, f"এই চ্যাটের আইডি হলো: `{message.chat.id}`", parse_mode="Markdown")

# --- ওটিপি পোলিং ও ফরওয়ার্ডিং ফাংশন ---
def poll_otp(chat_id, num, user_name):
    start_time = time.time()
    while time.time() - start_time < 300: # ৫ মিনিট চেক করবে
        try:
            r = requests.get(f"{BASE_URL}/success-otp", headers=HEADERS, timeout=10).json()
            if r['meta']['code'] == 200:
                otps = r['data'].get('otps', [])
                for o in otps:
                    if str(o['number']) == str(num):
                        otp_msg = (
                            f"📩 **New OTP Received!**\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📱 Number: `{num}`\n"
                            f"🔑 Code: `{o['message']}`\n"
                            f"👤 User: {user_name}\n"
                            f"━━━━━━━━━━━━━━"
                        )
                        # ১. ইউজারকে পার্সোনাল মেসেজ পাঠানো
                        bot.send_message(chat_id, otp_msg, parse_mode="Markdown")
                        
                        # ২. নির্দিষ্ট গ্রুপ আইডিতে ফরওয়ার্ড করা
                        try:
                            bot.send_message(GROUP_ID, f"📢 **OTP Forward Log**\n{otp_msg}", parse_mode="Markdown")
                        except Exception as e:
                            print(f"Forwarding Error: {e}")
                        return
        except: pass
        time.sleep(10)

# --- লাইভ কনসোল (Recent Hits) ---
@bot.message_handler(func=lambda m: m.text == "🖥️ Console")
def show_console(m):
    try:
        res = requests.get(f"{BASE_URL}/console", headers=HEADERS, timeout=10).json()
        if res['meta']['code'] == 200:
            hits = res['data'].get('hits', [])
            if not hits:
                bot.send_message(m.chat.id, "📭 বর্তমানে কনসোলে কোনো ডেটা নেই।")
                return
            
            console_text = "🖥️ **Live Global Console**\n━━━━━━━━━━━━━━\n"
            for hit in hits[:6]:
                console_text += f"🔹 **{hit['sid']}** | `{hit['range']}`\n💬 `{hit['message']}`\n━━━━━━━━━━━━━━\n"
            bot.send_message(m.chat.id, console_text, parse_mode="Markdown")
    except:
        bot.send_message(m.chat.id, "⚠️ কনসোল লোড করতে ব্যর্থ।")

# --- অটো রেঞ্জ ও সার্ভিস সিলেকশন ---
@bot.message_handler(func=lambda m: m.text == "📞 Get Number")
def show_services(m):
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS, timeout=10).json()
        if res['meta']['code'] == 200:
            services = res['data']['services']
            if not services:
                bot.send_message(m.chat.id, "❌ বর্তমানে কোনো সার্ভিস খালি নেই।")
                return
            markup = types.InlineKeyboardMarkup(row_width=2)
            for s in services:
                markup.add(types.InlineKeyboardButton(f"📱 {s['sid']}", callback_data=f"ser_{s['sid']}"))
            markup.add(types.InlineKeyboardButton("❌ Close", callback_data="close_menu"))
            bot.send_message(m.chat.id, "🐸 **Choose a service from panel:**", reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(m.chat.id, "⚠️ সার্ভিস লিস্ট লোড হচ্ছে না।")

@bot.callback_query_handler(func=lambda call: call.data.startswith("ser_"))
def show_ranges(call):
    sid = call.data.split("_")[1]
    try:
        res = requests.get(f"{BASE_URL}/liveaccess", headers=HEADERS).json()
        services = res['data']['services']
        selected = next((item for item in services if item['sid'] == sid), None)
        if selected:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for r in selected['ranges']:
                rid = r.replace("XXX", "")
                markup.add(types.InlineKeyboardButton(f"🌍 Range: {r}", callback_data=f"buy_{sid}_{rid}"))
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="back_to_main"))
            bot.edit_message_text(f"🌐 **{sid} Service**\nSelect a range:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_process(call):
    _, sid, rid = call.data.split("_")
    user_name = call.from_user.first_name
    bot.edit_message_text(f"⏳ **Requesting {sid}...** (RID: {rid})", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    try:
        res = requests.post(f"{BASE_URL}/getnum", json={"rid": rid}, headers=HEADERS, timeout=15).json()
        if res['meta']['code'] == 200:
            num = res['data']['no_plus_number']
            bot.edit_message_text(f"✅ **Number Received!**\n📱 `{res['data']['full_number']}`\n⏳ Waiting for OTP...", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
            threading.Thread(target=poll_otp, args=(call.message.chat.id, num, user_name)).start()
        else:
            bot.answer_callback_query(call.id, f"❌ {res['message']}", show_alert=True)
    except: bot.answer_callback_query(call.id, "⚠️ API Error!", show_alert=True)

# বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data in ["close_menu", "back_to_main"])
def simple_calls(call):
    if call.data == "close_menu": bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_services(call.message)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 **The Profit Player Bot Active!**", reply_markup=main_menu(), parse_mode="Markdown")

# --- বট স্টার্ট লুপ (Error/Conflict Handling সহ) ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    print("Bot is starting...")
    while True:
        try:
            bot.remove_webhook() # Conflict দূর করার জন্য
            bot.polling(none_stop=True, interval=0, timeout=40)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(15) # এরর হলে ১৫ সেকেন্ড পর আবার চেষ্টা করবে
