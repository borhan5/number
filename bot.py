import asyncio
import logging
import httpx
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# --- CONFIGURATION ---
API_TOKEN = "8953289994:AAEB7g1t1uu4iIv0Opv6ZT7yy9_jZ-K8qZg"
PANEL_API_KEY = "MQGVM5B5OOW"
GROUP_ID = -1003968881110  # Standard Telegram groups start with -100
BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"

COUNTRY_DATA = {
    "1": {"name": "USA/Canada", "flag": "🇺🇸"}, "7": {"name": "Russia/Kazakhstan", "flag": "🇷🇺"},
    "20": {"name": "Egypt", "flag": "🇪🇬"}, "211": {"name": "South Sudan", "flag": "🇸🇸"},
    "212": {"name": "Morocco", "flag": "🇲🇦"}, "213": {"name": "Algeria", "flag": "🇩🇿"},
    "216": {"name": "Tunisia", "flag": "🇹🇳"}, "218": {"name": "Libya", "flag": "🇱🇾"},
    "220": {"name": "Gambia", "flag": "🇬🇲"}, "221": {"name": "Senegal", "flag": "🇸🇳"},
    "222": {"name": "Mauritania", "flag": "🇲🇷"}, "223": {"name": "Mali", "flag": "🇲🇱"},
    "224": {"name": "Guinea", "flag": "🇬🇳"}, "225": {"name": "Ivory Coast", "flag": "🇨🇮"},
    "226": {"name": "Burkina Faso", "flag": "🇧🇫"}, "227": {"name": "Niger", "flag": "🇳🇪"},
    "228": {"name": "Togo", "flag": "🇹🇬"}, "229": {"name": "Benin", "flag": "🇧🇯"},
    "230": {"name": "Mauritius", "flag": "🇲🇺"}, "231": {"name": "Liberia", "flag": "🇱🇷"},
    "232": {"name": "Sierra Leone", "flag": "🇸🇱"}, "233": {"name": "Ghana", "flag": "🇬🇭"},
    "234": {"name": "Nigeria", "flag": "🇳🇬"}, "235": {"name": "Chad", "flag": "🇹🇩"},
    "236": {"name": "Central Africa", "flag": "🇨🇫"}, "237": {"name": "Cameroon", "flag": "🇨🇲"},
    "238": {"name": "Cape Verde", "flag": "🇨🇻"}, "239": {"name": "Sao Tome", "flag": "🇸🇹"},
    "240": {"name": "Equat. Guinea", "flag": "🇬🇶"}, "241": {"name": "Gabon", "flag": "🇬🇦"},
    "242": {"name": "Congo", "flag": "🇨🇬"}, "243": {"name": "DR Congo", "flag": "🇨🇩"},
    "244": {"name": "Angola", "flag": "🇦🇴"}, "245": {"name": "Guinea-Bissau", "flag": "🇬🇼"},
    "248": {"name": "Seychelles", "flag": "🇸🇨"}, "249": {"name": "Sudan", "flag": "🇸🇩"},
    "250": {"name": "Rwanda", "flag": "🇷🇼"}, "251": {"name": "Ethiopia", "flag": "🇪🇹"},
    "252": {"name": "Somalia", "flag": "🇸🇴"}, "253": {"name": "Djibouti", "flag": "🇩🇯"},
    "254": {"name": "Kenya", "flag": "🇰🇪"}, "255": {"name": "Tanzania", "flag": "🇹🇿"},
    "256": {"name": "Uganda", "flag": "🇺🇬"}, "257": {"name": "Burundi", "flag": "🇧🇮"},
    "258": {"name": "Mozambique", "flag": "🇲🇿"}, "260": {"name": "Zambia", "flag": "🇿🇲"},
    "261": {"name": "Madagascar", "flag": "🇲🇬"}, "262": {"name": "Reunion", "flag": "🇷🇪"},
    "263": {"name": "Zimbabwe", "flag": "🇿🇼"}, "264": {"name": "Namibia", "flag": "🇳🇦"},
    "265": {"name": "Malawi", "flag": "🇲🇼"}, "266": {"name": "Lesotho", "flag": "🇱🇸"},
    "267": {"name": "Botswana", "flag": "🇧🇼"}, "268": {"name": "Eswatini", "flag": "🇸🇿"},
    "269": {"name": "Comoros", "flag": "🇰🇲"}, "27": {"name": "South Africa", "flag": "🇿🇦"},
    "880": {"name": "Bangladesh", "flag": "🇧🇩"}, "91": {"name": "India", "flag": "🇮🇳"},
    "92": {"name": "Pakistan", "flag": "🇵🇰"}, "971": {"name": "UAE", "flag": "🇦🇪"},
    # ... (Other countries from your list)
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

class OrderProcess(StatesGroup):
    selecting_service = State()
    selecting_country = State()
    active_number = State()

# --- HELPER FUNCTIONS ---

async def fetch_panel(endpoint, method="GET", json_data=None):
    headers = {"mauthapi": PANEL_API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(f"{BASE_URL}/{endpoint}", headers=headers)
            else:
                response = await client.post(f"{BASE_URL}/{endpoint}", headers=headers, json=json_data)
            return response.json()
        except Exception as e:
            logging.error(f"API Error: {e}")
            return None

def mask_number(num):
    # Removes 3 digits from middle for group privacy
    if len(num) < 7: return num
    mid = len(num) // 2
    return f"{num[:mid-1]}***{num[mid+2:]}"

def extract_otp(message):
    # Finds 4-8 digit codes in text
    match = re.search(r'\b(\d{4,8})\b', message)
    return match.group(1) if match else "Wait for OTP..."

# --- HANDLERS ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="📱 Get Number", callback_data="get_num")
    await message.answer(
        "✨ *Welcome to Voltx SMS Bot*\nProfessional Virtual Number Service.",
        reply_markup=kb.as_markup(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "get_num")
async def choose_service(callback: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text="Facebook 📘", callback_data="srv_Facebook")
    kb.button(text="Instagram 📸", callback_data="srv_Instagram")
    kb.adjust(2)
    await callback.message.edit_text("Select the service you need:", reply_markup=kb.as_markup())
    await state.set_state(OrderProcess.selecting_service)

@dp.callback_query(F.data.startswith("srv_"))
async def choose_country(callback: types.CallbackQuery, state: FSMContext):
    service = callback.data.split("_")[1]
    await state.update_data(service=service)
    
    # Fetch live traffic to see which countries are active
    data = await fetch_panel("liveaccess")
    active_ranges = []
    
    if data and data.get("meta", {}).get("code") == 200:
        for s in data['data']['services']:
            if service.lower() in s['sid'].lower():
                active_ranges.extend(s['ranges'])

    kb = InlineKeyboardBuilder()
    found_countries = set()
    
    # Match active ranges to our COUNTRY_DATA
    for r in active_ranges:
        prefix = r.replace("XXX", "")
        # Find matching country code
        for code, info in COUNTRY_DATA.items():
            if prefix.startswith(code):
                if code not in found_countries:
                    kb.button(text=f"{info['flag']} {info['name']}", callback_data=f"cnt_{prefix}")
                    found_countries.add(code)

    if not found_countries:
        await callback.answer("No live traffic found for this service. Try later.", show_alert=True)
        return

    kb.adjust(2)
    kb.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="get_num"))
    await callback.message.edit_text(f"Select a Country for {service}:", reply_markup=kb.as_markup())
    await state.set_state(OrderProcess.selecting_country)

@dp.callback_query(F.data.startswith("cnt_"))
async def get_number(callback: types.CallbackQuery, state: FSMContext):
    prefix = callback.data.split("_")[1]
    await callback.message.edit_text("⚡ Allocating number... please wait.")
    
    res = await fetch_panel("getnum", method="POST", json_data={"rid": prefix})
    
    if res and res.get("meta", {}).get("code") == 200:
        num_data = res['data']
        full_num = num_data['full_number']
        
        await state.update_data(active_num=full_num)
        
        kb = InlineKeyboardBuilder()
        kb.button(text="🔄 Change Number", callback_data="get_num")
        kb.button(text="🌍 Change Country", callback_data="get_num")
        kb.adjust(1)

        await callback.message.edit_text(
            f"✅ *Number Allocated*\n\n"
            f"📌 *Service:* Facebook/Insta\n"
            f"📞 *Number:* `{full_num}`\n"
            f"🏳️ *Country:* {num_data['country']}\n\n"
            f"⌛ Waiting for OTP...",
            reply_markup=kb.as_markup(),
            parse_mode="Markdown"
        )
        
        # Start OTP Checking loop for this user
        asyncio.create_task(check_otp_loop(callback.message, full_num, state))
    else:
        await callback.message.edit_text("❌ Out of stock for this range. Try another country.")

async def check_otp_loop(message, phone, state):
    # Check for 5 minutes
    for _ in range(60):
        await asyncio.sleep(5)
        res = await fetch_panel("success-otp")
        if res and res.get("meta", {}).get("code") == 200:
            otps = res['data'].get('otps', [])
            for item in otps:
                # Check if this OTP is for our specific number
                if item['number'] in phone:
                    otp_code = extract_otp(item['message'])
                    
                    # 1. Update user chat
                    await message.edit_text(
                        f"✅ *OTP Received!*\n\n"
                        f"📞 *Number:* `{phone}`\n"
                        f"💬 *Message:* `{item['message']}`\n"
                        f"🔑 *Code:* `{otp_code}`",
                        parse_mode="Markdown"
                    )
                    
                    # 2. Forward to Group with masked number
                    masked = mask_number(phone)
                    group_msg = (
                        f"🔔 *New OTP Logged*\n"
                        f"📱 Number: `{masked}`\n"
                        f"📟 Code: `{otp_code}`\n"
                        f"🌐 Service: FB/Insta"
                    )
                    await bot.send_message(GROUP_ID, group_msg, parse_mode="Markdown")
                    await state.clear()
                    return
    
    await message.answer("⏰ OTP Timeout. No message received.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
