from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from flask import Flask
from threading import Thread
import traceback
import asyncio
import time

# =========================
# CONFIG
# =========================
BOT_TOKEN = "8395409278:AAHCHBKTw_ic877ow3Gx1cX8B7O000eQKFQ"
CHAT_ID = -10029801886562
DELAY = 120  # giây

# =========================
# CAPTIONS  (GIỮ NGUYÊN)
# =========================
CAPTION_1 = """💎 ĐĂNG KÝ NHẬN 68K – NHẬN NGAY 500K!
🪄 Chỉ cần xác minh thông tin cá nhân – nhận tiền liền tay 💰
⚡️ Nhanh tay tham gia – đừng bỏ lỡ cơ hội có tiền free!
🎁 Đăng ký ngay hôm nay để nhận nhiều phần quà hấp dẫn!!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_2 = """🎰 Slot Fever 200% – Quà Tới Tay, May Tới Liền!
💸 Thưởng 200% nạp lần đầu – lên đến 6,888,000 VND
⚙️ Hoàn tất nạp tiền qua website WINBOOK – nhận thưởng tự động!
⏳ Cơ hội có hạn – tham gia liền tay kẻo lỡ!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_3 = """⚽ Đặt cược lần đầu – Không sợ mất!
🛡 WINBOOK bảo vệ 100% cho cược đầu tiên
🔥 Chỉ áp dụng tại SABA Sports – trận lớn, kèo hot!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_4 = """💸 Càng nạp càng được – tiền tự nhân lên!
➕ Thưởng 10% mỗi ngày – nhận thưởng 6,000,000 VND
⏱ Cơ hội “đẻ thêm tiền” mỗi 24h tại WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_5 = """🔥 NẠP 1 NHẬN 2 – THƯỞNG 100% NGAY!
💵 Thưởng chào mừng 100% – thắng lớn đến 3,888,000 VND
🎮 Áp dụng cho Slots, Bắn Cá, Thể Thao & Live Casino
⚡️ Nhanh tay nạp – cơ hội nhân đôi vốn đang chờ bạn!
🎯 x20 vòng cược rinh ngay 3,888,888 VND
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_6 = """🎉 Mời bạn bè – Nhận hoàn tiền không giới hạn!
🔗 Dùng mã QR hoặc link giới thiệu để mời người chơi mới
💰 Mỗi lượt mời thành công: nhận hoàn 0.3%
🕓 Hoàn tiền phát lúc 16:00 ngày hôm sau
♾️ Không giới hạn số tiền hoàn!
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_7 = """🎁 THƯỞNG NẠP TUẦN 30% – NHẬN QUÀ MỖI TUẦN!
📈 Nhận 30% thưởng nạp – tối đa 6,000,000 VND
⚙️ Chỉ cần nạp tiền & hoàn doanh thu cược hợp lệ
📝 Đăng ký nhanh qua Mẫu Nạp Tiền trên WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_8 = """💥 THƯỞNG 50% – TRỌN BỘ SLOTS, LIVE & SPORTS!
👤 Thành viên WINBOOK nhận thưởng 1 lần duy nhất
💰 Nhận ngay 50% thưởng – tối đa 500,000 VND
🎰 Slots & Bắn Cá – Thưởng 50%, X5 vòng cược
🎬 Trò Chơi Trực Tiếp – Thưởng 50%, X5 vòng cược
⚽ Thể Thao – Thưởng 50%, X5 vòng cược
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

CAPTION_9 = """💰 Càng chơi, càng lời – hoàn tới 1.2%!
🔄 Tự động hoàn tiền mỗi ngày – không giới hạn
👑 Chỉ dành cho thành viên WINBOOK
💬 Liên hệ các kênh bên dưới 👇 để được hỗ trợ nhanh nhất."""

# =========================
# IMAGES  (GIỮ NGUYÊN)
# =========================
images = [
    {"img": "https://i.ibb.co/4TQ4tqv/1.png", "cap": CAPTION_1},
    {"img": "https://i.ibb.co/cQk9bnM/2.png", "cap": CAPTION_2},
    {"img": "https://i.ibb.co/Km0gPqt/3.png", "cap": CAPTION_3},
    {"img": "https://i.ibb.co/tHq50fr/4.png", "cap": CAPTION_4},
    {"img": "https://i.ibb.co/mGdq8Lv/5.png", "cap": CAPTION_5},
    {"img": "https://i.ibb.co/NYQg4gw/6.png", "cap": CAPTION_6},
    {"img": "https://i.ibb.co/h1WhW33/7.png", "cap": CAPTION_7},
    {"img": "https://i.ibb.co/tMr6cM2/8.png", "cap": CAPTION_8},
    {"img": "https://i.ibb.co/4SQ2Fvm/9.png", "cap": CAPTION_9},
]

# =========================
# MENU  (GIỮ NGUYÊN)
# =========================
menu = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🖥 MENU HỆ THỐNG CHÍNH THỨC - HỖ TRỢ 24/7",
            web_app=WebAppInfo(url="https://ahyen6688-bit.github.io/winbookmenuhotro-/")
        )
    ]
])

# =========================
# FLASK SERVER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running OK"

def run_flask():
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# =========================
# HELPER: gửi ảnh (dùng app.bot trực tiếp)
# =========================
async def send_image_by_index(app_obj, idx):
    try:
        data = images[idx]
        await app_obj.bot.send_photo(
            chat_id=CHAT_ID,
            photo=data["img"],
            caption=data["cap"],
            reply_markup=menu
        )
        print(f"Đã gửi ảnh số: {idx+1} tại {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception:
        print(traceback.format_exc())

# =========================
# BACKGROUND AUTO POST (THAY THẾ job_queue)
# =========================
async def auto_poster(app_obj):
    # Gửi lần đầu sau 5s (giống behavior trước)
    await asyncio.sleep(5)
    while True:
        try:
            idx = app_obj.bot_data.get("i", 0)
            await send_image_by_index(app_obj, idx)
            app_obj.bot_data["i"] = (idx + 1) % len(images)
        except Exception:
            print("Lỗi khi auto_poster:")
            print(traceback.format_exc())
        # chờ DELAY giây rồi lặp
        await asyncio.sleep(DELAY)

# =========================
# COMMANDS
# =========================
async def start(update, context):
    await update.message.reply_text("Bot đang chạy!", reply_markup=menu)

async def sendnow(update, context):
    idx = context.application.bot_data.get("i", 0)
    data = images[idx]

    await update.message.reply_photo(
        photo=data["img"],
        caption=data["cap"],
        reply_markup=menu
    )

# =========================
# MAIN (ĐÃ FIX: không dùng job_queue)
# =========================
async def main():
    Thread(target=run_flask, daemon=True).start()

    appTG = ApplicationBuilder().token(BOT_TOKEN).build()

    # khởi tạo index
    appTG.bot_data["i"] = 0

    # handlers
    appTG.add_handler(CommandHandler("start", start))
    appTG.add_handler(CommandHandler("sendnow", sendnow))

    # tạo background task auto_poster (thay job_queue.run_repeating)
    # schedule task sau khi appTG khởi chạy
    # ta start run_polling as coroutine, và song song tạo task auto_poster
    # để dễ quản lý, tạo task trước khi run_polling và nó sẽ chạy trên cùng loop
    asyncio.create_task(auto_poster(appTG))

    print("BOT RUNNING…")
    await appTG.run_polling()

# =========================
# SAFE ENTRYPOINT (KHÔNG DÙNG asyncio.run trực tiếp)
# =========================
if __name__ == "__main__":
    loop = None
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        loop.create_task(main())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
    else:
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            pass
