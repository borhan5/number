import os
import asyncio
import logging
import requests
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from flask import Flask
from threading import Thread

# --- RENDER WEB SERVER (For 24/7 Hosting) ---
app = Flask('')
@app.route('/')
def home():
    return "VOLTX Bot is Live!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
API_TOKEN = '8953289994:AAHalks0v_QNWta40jorqobnfwS1trW8pJQ' 
PANEL_API_KEY = 'MSVB8RMSMQK' 
OTP_GROUP_ID = -1003968881110 
BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
headers = {'mauthapi': PANEL_API_KEY}

# --- EXTENSIVE COUNTRY FLAG MAP ---
COUNTRY_FLAGS = {
    "Afghanistan": "🇦🇫", "Albania": "🇦🇱", "Algeria": "🇩🇿", "Andorra": "🇦🇩", "Angola": "🇦🇴", "Argentina": "🇦🇷",
    "Armenia": "🇦🇲", "Australia": "🇦🇺", "Austria": "🇦🇹", "Azerbaijan": "🇦🇿", "Bahamas": "🇧🇸", "Bahrain": "🇧🇭",
    "Bangladesh": "🇧🇩", "Barbados": "🇧🇧", "Belarus": "🇧🇾", "Belgium": "🇧🇪", "Belize": "🇧🇿", "Benin": "🇧🇯",
    "Bhutan": "🇧🇹", "Bolivia": "🇧🇴", "Bosnia and Herzegovina": "🇧🇦", "Botswana": "🇧🇼", "Brazil": "🇧🇷", "Brunei": "🇧🇳",
    "Bulgaria": "🇧🇬", "Burkina Faso": "🇧🇫", "Burundi": "🇧🇮", "Cambodia": "🇰🇭", "Cameroon": "🇨🇲", "Canada": "🇨🇦",
    "Cape Verde": "🇨🇻", "Central African Republic": "🇨🇫", "Chad": "🇹🇩", "Chile": "🇨🇱", "China": "🇨🇳", "Colombia": "🇨🇴",
    "Comoros": "🇰🇲", "Congo": "🇨🇬", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷", "Cuba": "🇨🇺", "Cyprus": "🇨🇾", "Czech Republic": "🇨🇿",
    "Denmark": "🇩🇰", "Djibouti": "🇩🇯", "Dominica": "🇩🇲", "Dominican Republic": "🇩🇴", "Ecuador": "🇪🇨", "Egypt": "🇪🇬",
    "El Salvador": "🇸🇻", "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷", "Estonia": "🇪🇪", "Ethiopia": "🇪🇹", "Fiji": "🇫🇯",
    "Finland": "🇫🇮", "France": "🇫🇷", "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Georgia": "🇬🇪", "Germany": "🇩🇪", "Ghana": "🇬🇭",
    "Greece": "🇬🇷", "Grenada": "🇬🇩", "Guatemala": "🇬🇹", "Guinea": "🇬🇳", "Guyana": "🇬🇾", "Haiti": "🇭🇹", "Honduras": "🇭🇳",
    "Hungary": "🇭🇺", "Iceland": "🇮🇸", "India": "🇮🇳", "Indonesia": "🇮🇩", "Iran": "🇮🇷", "Iraq": "🇮🇶", "Ireland": "🇮🇪",
    "Israel": "🇮🇱", "Italy": "🇮🇹", "Ivory Coast": "🇨🇮", "Jamaica": "🇯🇲", "Japan": "🇯🇵", "Jordan": "🇯🇴", "Kazakhstan": "🇰🇿",
    "Kenya": "🇰🇪", "Kiribati": "🇰🇮", "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬", "Laos": "🇱🇦", "Latvia": "🇱🇻", "Lebanon": "🇱🇧",
    "Lesotho": "🇱🇸", "Liberia": "🇱🇷", "Libya": "🇱🇾", "Liechtenstein": "🇱🇮", "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺",
    "Madagascar": "🇲🇬", "Malawi": "🇲🇼", "Malaysia": "🇲🇾", "Maldives": "🇲🇻", "Mali": "🇲🇱", "Malta": "🇲🇹", "Mauritania": "🇲🇷",
    "Mauritius": "🇲🇺", "Mexico": "🇲🇽", "Moldova": "🇲🇩", "Monaco": "🇲🇨", "Mongolia": "🇲🇳", "Montenegro": "🇲🇪",
    "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Myanmar": "🇲🇲", "Namibia": "🇳🇦", "Nauru": "🇳🇷", "Nepal": "🇳🇵", "Netherlands": "🇳🇱",
    "New Zealand": "🇳🇿", "Nicaragua": "🇳🇮", "Niger": "🇳🇪", "Nigeria": "🇳🇬", "North Korea": "🇰🇵", "Norway": "🇳🇴",
    "Oman": "🇴🇲", "Pakistan": "🇵🇰", "Palau": "🇵🇼", "Palestine": "🇵🇸", "Panama": "🇵🇦", "Papua New Guinea": "🇵🇬",
    "Paraguay": "🇵🇾", "Peru": "🇵🇪", "Philippines": "🇵🇭", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦", "Romania": "🇷🇴",
    "Russia": "🇷🇺", "Rwanda": "🇷🇼", "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳", "Serbia": "🇷🇸", "Seychelles": "🇸🇨",
    "Sierra Leone": "🇸🇱", "Singapore": "🇸🇬", "Slovakia": "🇸🇰", "Slovenia": "🇸🇮", "Solomon Islands": "🇸🇧", "Somalia": "🇸🇴",
    "South Africa": "🇿🇦", "South Korea": "🇰🇷", "South Sudan": "🇸🇸", "Spain": "🇪🇸", "Sri Lanka": "🇱🇰", "Sudan": "🇸🇩",
    "Suriname": "🇸🇷", "Swaziland": "🇸🇿", "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "Syria": "🇸🇾", "Taiwan": "🇹🇼",
    "Tajikistan": "🇹🇯", "Tanzania": "🇹🇿", "Thailand": "🇹🇭", "Togo": "🇹🇬", "Tonga": "🇹🇴", "Trinidad and Tobago": "🇹🇹",
    "Tunisia": "🇹🇳", "Turkey": "🇹🇷", "Turkmenistan": "🇹🇲", "Tuvalu": "🇹🇻", "Uganda": "🇺🇬", "Ukraine": "🇺🇦",
    "United Arab Emirates": "🇦🇪", "United Kingdom": "🇬🇧", "USA": "🇺🇸", "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿",
    "Vanuatu": "🇻🇺", "Venezuela": "🇻🇪", "Vietnam": "🇻🇳", "Yemen": "🇾🇪", "Zambia": "🇿🇲", "Zimbabwe": "🇿🇼"
}

# --- HELPER FUNCTIONS ---

def get_live_ranges(service_name):
    try:
        response = requests.get(f"{BASE_URL}/liveaccess", headers=headers)
        data = response.json()
        if data['meta']['code'] == 200:
            for s in data['data']['services']:
                if s['sid'].lower() == service_name.lower():
                    return s['ranges']
        return []
    except:
        return []

def mask_number(num):
    s = str(num)
    # Masks 3 digits in the middle (e.g., 447404333228 -> 4474***33228)
    if len(s) > 6:
        return f"{s[:4]}***{s[7:]}"
    return s

async def check_otp_loop(msg_obj, number, service):
    # Check every 5 seconds for up to 5 minutes
    for _ in range(60):
        await asyncio.sleep(5)
        try:
            res = requests.get(f"{BASE_URL}/success-otp", headers=headers)
            otp_data = res.json()
            if otp_data['meta']['code'] == 200:
                for item in otp_data['data']['otps']:
                    if str(item['number']) == str(number):
                        raw_msg = item['message']
                        
                        # Extract only digits for Facebook codes
                        if service == "Facebook":
                            otp_code = "".join(re.findall(r'\d+', raw_msg))
                        else:
                            otp_code = raw_msg
                        
                        await msg_obj.edit_text(f"✅ **OTP SUCCESS**\n\nNumber: `+{number}`\nCode: `{otp_code}`", parse_mode="Markdown")
                        
                        # Forward to Group with Masked Number
                        masked = mask_number(number)
                        group_text = (f"🔔 **NEW OTP ALERT**\n"
                                     f"Service: {service}\n"
                                     f"Number: +{masked}\n"
                                     f"OTP Code: `{otp_code}`")
                        await bot.send_message(OTP_GROUP_ID, group_text, parse_mode="Markdown")
                        return
        except:
            pass

# --- BOT HANDLERS ---

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("📞 Get Number", callback_data="main"))
    await message.answer("✨ **Welcome to VOLTX SMS**\nGet fast OTPs for global services.", reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == "main")
async def show_services(cb: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📘 Facebook", callback_data="srv_Facebook"),
        InlineKeyboardButton("📸 Instagram", callback_data="srv_Instagram"),
        InlineKeyboardButton("🟢 WhatsApp", callback_data="srv_WhatsApp")
    )
    await bot.edit_message_text("💎 **Select Service:**", cb.from_user.id, cb.message.message_id, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data.startswith("srv_"))
async def display_ranges(cb: types.CallbackQuery):
    service = cb.data.split('_')[1]
    ranges = get_live_ranges(service)
    
    if not ranges:
        await cb.answer("No live ranges available right now.", show_alert=True)
        return

    kb = InlineKeyboardMarkup(row_width=2)
    for r in ranges[:12]:
        rid = r.replace('XXX', '')
        kb.add(InlineKeyboardButton(f"📡 Range {r}", callback_data=f"buy_{service}_{rid}"))
    kb.add(InlineKeyboardButton("🔙 Back", callback_data="main"))
    
    await bot.edit_message_text(f"Select a live range for **{service}**:", cb.from_user.id, cb.message.message_id, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def buy_process(cb: types.CallbackQuery):
    _, service, rid = cb.data.split('_')
    
    # Post request to allocate number
    res = requests.post(f"{BASE_URL}/getnum", headers=headers, json={"rid": rid}).json()
    
    if res['meta']['code'] == 200:
        data = res['data']
        num = data['no_plus_number']
        country = data['country']
        flag = COUNTRY_FLAGS.get(country, "🏳️") # Default to white flag if unknown
        
        msg_body = (f"✅ **Number Ready**\n\n"
                   f"🌍 Country: {flag} {country}\n"
                   f"🔢 Number: `+{num}`\n"
                   f"🏷 Service: {service}\n\n"
                   f"⏳ Waiting for OTP code...")
        
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🔄 Change Number", callback_data=f"buy_{service}_{rid}"),
            InlineKeyboardButton("🌍 Change Country", callback_data="main")
        )
        
        sent = await bot.edit_message_text(msg_body, cb.from_user.id, cb.message.message_id, reply_markup=kb, parse_mode="Markdown")
        
        # Start checking for OTP in background
        asyncio.create_task(check_otp_loop(sent, num, service))
    else:
        await cb.answer("❌ Out of stock! Try another range.", show_alert=True)

if __name__ == '__main__':
    Thread(target=run_web).start() 
    executor.start_polling(dp, skip_updates=True)
