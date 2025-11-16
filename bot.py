# telegram_auto_post_bot.py
# Full Telegram auto-post bot with image rotation, hourly schedule, and custom menus

import asyncio
import nest_asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.error import TelegramError
from datetime import datetime
import logging

nest_asyncio.apply()

# ========================= CONFIG ==============================
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@your_channel_id"  # or -100xxxxxxxxx

# Image list with captions
images = [
    {"url": "https://i.ibb.co/4TQ4tqv/1.png", "cap": """💎 ĐĂNG KÝ NHẬN 68K – NHẬN NGAY 500K!
🪄 Chỉ cần xác minh thông tin cá nhân – nhận tiền liền tay 💰
⚡️ Nhanh tay tham gia – đừng bỏ lỡ cơ hội có tiền free!
🎁 Đăng ký ngay hôm nay để nhận nhiều phần quà hấp dẫn!!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/cQk9bnM/2.png", "cap": """🎰 Slot Fever 200% – Quà Tới Tay, May Tới Liền!
💸 Thưởng 200% nạp lần đầu – lên đến 6,888,000 VND
⚙️ Hoàn tất nạp tiền qua website WINBOOK – nhận thưởng tự động!
⏳ Cơ hội có hạn – tham gia liền tay kẻo lỡ!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/Km0gPqt/3.png", "cap": """⚽ Đặt cược lần đầu – Không sợ mất!
🛡 WINBOOK bảo vệ 100% cho cược đầu tiên
🔥 Chỉ áp dụng tại SABA Sports – trận lớn, kèo hot!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/tHq50fr/4.png", "cap": """💸 Càng nạp càng được – tiền tự nhân lên!
➕ Thưởng 10% mỗi ngày – nhận thưởng 6,000,000 VND
⏱ Cơ hội “đẻ thêm tiền” mỗi 24h tại WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/mGdq8Lv/5.png", "cap": """🔥 NẠP 1 NHẬN 2 – THƯỞNG 100% NGAY!
💵 Thưởng chào mừng 100% – thắng lớn đến 3,888,000 VND
🎮 Áp dụng cho Slots, Bắn Cá, Thể Thao & Live Casino
⚡️ Nhanh tay nạp – cơ hội nhân đôi vốn đang chờ bạn!
🎯 x20 vòng cược rinh ngay 3,888,888 VND
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/NYQg4gw/6.png", "cap": """🎉 Mời bạn bè – Nhận hoàn tiền không giới hạn!
🔗 Dùng mã QR hoặc link giới thiệu để mời người chơi mới
💰 Mỗi lượt mời thành công: nhận hoàn 0.3%
🕓 Hoàn tiền phát lúc 16:00 ngày hôm sau
♾️ Không giới hạn số tiền hoàn!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/h1WhW33/7.png", "cap": """🎁 THƯỞNG NẠP TUẦN 30% – NHẬN QUÀ MỖI TUẦN!
📈 Nhận 30% thưởng nạp – tối đa 6,000,000 VND
⚙️ Chỉ cần nạp tiền & hoàn doanh thu cược hợp lệ
📝 Đăng ký nhanh qua Mẫu Nạp Tiền trên WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/tMr6cM2/8.png", "cap": """💥 THƯỞNG 50% – TRỌN BỘ SLOTS, LIVE & SPORTS!
👤 Thành viên WINBOOK nhận thưởng 1 lần duy nhất
💰 Nhận ngay 50% thưởng – tối đa 500,000 VND
🎰 Slots & Bắn Cá – Thưởng 50%, X5 vòng cược
🎬 Trò Chơi Trực Tiếp – Thưởng 50%, X5 vòng cược
⚽ Thể Thao – Thưởng 50%, X5 vòng cược
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
    {"url": "https://i.ibb.co/4SQ2Fvm/9.png", "cap": """💰 Càng chơi, càng lời – hoàn tới 1.2%!
🔄 Tự động hoàn tiền mỗi ngày – không giới hạn
👑 Chỉ dành cho thành viên WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""},
]

# Buttons
menu_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Đăng ký", url="https://www.winbook1.com"),
        InlineKeyboardButton("Live Chat", url="https://direct.lc.chat/19366399/")
    ],
    [
        InlineKeyboardButton(
            "🖥 MENU HỆ THỐNG CHÍNH THỨC - HỖ TRỢ 24/7",
            web_app=WebAppInfo(url="https://ahyen6688-bit.github.io/winbookmenuhotro-/")
        )
    ]
])

# ================================================================
from telegram.ext import Application, CommandHandler
from flask import Flask
app = Flask(__name__)

async def start(update, context):
    await update.message.reply_text("Bot đang hoạt động bình thường!")

async def sendnow(update, context):
    global current_index
    img = images[current_index]
    await bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=img["url"],
        caption=img["cap"],
        reply_markup=menu_keyboard,
    )
    current_index = (current_index + 1) % len(images)

@app.route('/')
def home():
    return "Bot alive"

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("sendnow", sendnow))
# ================================================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)

current_index = 0

async def post_image_loop():
    global current_index

    while True:
        try:
            img = images[current_index]

            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=img["url"],
                caption=img["cap"],
                reply_markup=menu_keyboard,
            )

            logging.info(f"Đã đăng hình số {current_index + 1} lúc {datetime.now()}")

            current_index = (current_index + 1) % len(images)

        except TelegramError as e:
            logging.error(f"Lỗi khi gửi: {e}")

        await asyncio.sleep(3600)  # wait 1 hour


if __name__ == "__main__":
    import threading

    # Start Flask in its own thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000), daemon=True).start()

    async def main_async():
        # Start Telegram bot without closing event loop
        await application.initialize()
        await application.start()

        # Start auto-post task
        asyncio.create_task(post_image_loop())

        # Keep running forever
        await asyncio.Event().wait()

    asyncio.run(main_async())
