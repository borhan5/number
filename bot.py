import telebot
import requests
import time
from telebot import types

# --- আপনার দেওয়া কনফিগুরেশন ---
API_TOKEN = "8953289994:AAFFdFTn4g-UJKKispB6_qFW5vbJI1KmAbc"
VOLTX_KEY = "MQGVM5B5OOW"
ADMIN_ID = 8250359361
GROUP_ID = -1003968881110 
CHANNEL_LINK = "https://t.me/+3MsGv1ySkEQ2ODBl" # প্রাইভেট লিঙ্কের ক্ষেত্রে চ্যানেলের ইউজারনেম বা আইডি চেক করতে হবে
CHANNEL_USERNAME = "@earntrick_BS" # উদাহরণস্বরূপ, চ্যানেলের ইউজারনেম দিন (শুরুতে @ দিয়ে)
METHOD_LINK = "https://t.me/earntrick_BS"

# VoltxSMS API Base URL (সাধারণত এই ফরম্যাটে থাকে)
VOLTX_API_URL = "https://voltxsms.com/stubs/handler_api.php"

bot = telebot.TeleBot(API_TOKEN)

# --- মেম্বারশিপ চেক ফাংশন ---
def is_subscribed(user_id):
    try:
        # দ্রষ্টব্য: বটকে অবশ্যই ওই চ্যানেলের অ্যাডমিন হতে হবে
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        # যদি ইউজারনেম কাজ না করে তবে আপাতত True রিটার্ন করবে (বটকে অ্যাডমিন করলে কাজ করবে)
        return True 

# --- মেইন মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("💰 ব্যালেন্স চেক")
    btn2 = types.KeyboardButton("📱 নম্বর কিনুন")
    btn3 = types.KeyboardButton("📖 মেথড দেখুন")
    btn4 = types.KeyboardButton("👨‍💻 সাপোর্ট")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("চ্যানেলে জয়েন করুন", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, "❌ আপনাকে প্রথমে আমাদের চ্যানেলে জয়েন করতে হবে। জয়েন করে আবার /start লিখুন।", reply_markup=markup)
        return

    bot.send_message(message.chat.id, "স্বাগতম! VoltxSMS বট দিয়ে আপনি সহজেই ওটিপি নম্বর নিতে পারবেন।", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "💰 ব্যালেন্স চেক":
        response = requests.get(f"{VOLTX_API_URL}?api_key={VOLTX_KEY}&action=getBalance")
        if "ACCESS_BALANCE" in response.text:
            balance = response.text.split(":")[1]
            bot.reply_to(message, f"✅ আপনার বর্তমান ব্যালেন্স: {balance} টাকা")
        else:
            bot.reply_to(message, "❌ ব্যালেন্স চেক করতে সমস্যা হচ্ছে।")

    elif message.text == "📖 মেথড দেখুন":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("মেথড লিঙ্ক", url=METHOD_LINK))
        bot.send_message(message.chat.id, "নিচের লিঙ্কে ক্লিক করে মেথডটি দেখে নিন:", reply_markup=markup)

    elif message.text == "📱 নম্বর কিনুন":
        # সার্ভিস লিস্ট (উদাহরণস্বরূপ Telegram, WhatsApp)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Telegram", callback_data="buy_tg"))
        markup.add(types.InlineKeyboardButton("WhatsApp", callback_data="buy_wa"))
        bot.send_message(message.chat.id, "কোন সার্ভিসের নম্বর নিতে চান?", reply_markup=markup)

    elif message.text == "👨‍💻 সাপোর্ট":
        bot.send_message(message.chat.id, f"যেকোনো সমস্যায় অ্যাডমিনের সাথে যোগাযোগ করুন: [অ্যাডমিন আইডি](tg://user?id={ADMIN_ID})", parse_mode="Markdown")

# --- কলব্যাক হ্যান্ডলার (নম্বর কেনা) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "buy_tg":
        service = "tg" # Telegram service code
        country = "0"  # 0 = Russia, 1 = Ukraine (VoltxSMS এর কান্ট্রি কোড অনুযায়ী পরিবর্তন করুন)
        
        # নম্বর রিকোয়েস্ট
        res = requests.get(f"{VOLTX_API_URL}?api_key={VOLTX_KEY}&action=getNumber&service={service}&country={country}")
        
        if "ACCESS_NUMBER" in res.text:
            # ফরম্যাট: ACCESS_NUMBER:ID:NUMBER
            _, order_id, phone = res.text.split(":")
            
            msg_text = f"📱 নম্বর: `{phone}`\n🆔 অর্ডার আইডি: `{order_id}`\n\nওটিপি-র জন্য অপেক্ষা করুন..."
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("ওটিপি চেক করুন", callback_data=f"get_otp_{order_id}"))
            markup.add(types.InlineKeyboardButton("বাতিল করুন", callback_data=f"cancel_{order_id}"))
            
            bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ এই মুহূর্তে নম্বর নেই।")

    elif call.data.startswith("get_otp_"):
        order_id = call.data.split("_")[2]
        res = requests.get(f"{VOLTX_API_URL}?api_key={VOLTX_KEY}&action=getStatus&id={order_id}")
        
        if "STATUS_OK" in res.text:
            otp = res.text.split(":")[1]
            bot.send_message(call.message.chat.id, f"✅ আপনার ওটিপি হলো: `{otp}`", parse_mode="Markdown")
        elif "STATUS_WAIT_CODE" in res.text:
            bot.answer_callback_query(call.id, "⏳ ওটিপি এখনো আসেনি, দয়া করে অপেক্ষা করুন।", show_alert=True)
        else:
            bot.answer_callback_query(call.id, f"অবস্থা: {res.text}")

    elif call.data.startswith("cancel_"):
        order_id = call.data.split("_")[1]
        # স্ট্যাটাস ৮ মানে অর্ডার ক্যান্সেল/কমপ্লিট
        requests.get(f"{VOLTX_API_URL}?api_key={VOLTX_KEY}&action=setStatus&id={order_id}&status=8")
        bot.edit_message_text("❌ নম্বরটি বাতিল করা হয়েছে।", call.message.chat.id, call.message.message_id)

print("Bot is running...")
bot.polling()
