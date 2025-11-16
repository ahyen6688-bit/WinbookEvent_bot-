from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@WinbookEvent"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DELAY = 120  # mỗi 120 giây gửi 1 ảnh

# =========================
# CAPTIONS (GIỮ NGUYÊN 100%)
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
# IMAGES
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
# MENU (GIỮ NGUYÊN)
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
# TELEGRAM APP (WEBHOOK)
# =========================
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đang chạy!", reply_markup=menu)

bot_app.add_handler(CommandHandler("start", start))

# =========================
# AUTO POST (SCHEDULER)
# =========================
index = 0

def auto_send():
    global index
    data = images[index]

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        params={
            "chat_id": CHANNEL_ID,
            "photo": data["img"],
            "caption": data["cap"]
        }
    )
    print("Đã gửi:", data["img"])
    index = (index + 1) % len(images)

scheduler = BackgroundScheduler()
scheduler.add_job(auto_send, "interval", seconds=DELAY)
scheduler.start()

# =========================
# FLASK SERVER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "BOT OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, bot_app.bot)
    bot_app.update_queue.put_nowait(update)
    return "OK"

# =========================
# START APP
# =========================
if __name__ == "__main__":
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
        params={"url": WEBHOOK_URL}
    )
    print("Webhook:", WEBHOOK_URL)

    app.run(host="0.0.0.0", port=8080)
