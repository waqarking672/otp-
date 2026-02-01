import asyncio
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder

# ================= CONFIG =================
BOT_TOKEN = "8373740550:AAF2Ig-eVD_vTOGdfKVgxVtdXtbOuhOkozw"           # 🔴 BotFather se NEW token
TARGET_CHAT = "@arslanmdotp"            # group / channel username

OTP_API = "https://arslan-apis.vercel.app/more/liveotp2"
POLL_INTERVAL = 3                         # seconds

CHANNEL_BUTTON_TEXT = "🔔 Join Official Channel"
CHANNEL_BUTTON_URL  = "https://t.me/e3hacker"   # tumhara channel link

# ================= MEMORY =================
seen = set()

# ================= OTP LOOP =================
async def otp_loop(app):
    while True:
        try:
            r = requests.get(OTP_API, timeout=20)
            data = r.json()

            if not data.get("status") or "result" not in data:
                await asyncio.sleep(POLL_INTERVAL)
                continue

            for otp in data["result"]:
                key = f"{otp['number']}-{otp['otp']}"
                if key in seen:
                    continue

                seen.add(key)
                asyncio.create_task(clean_key(key))

                msg = (
                    "📩 *OTP RECEIVED*\n\n"
                    f"📞 *Number:* `{otp['number']}`\n"
                    f"🔐 *OTP:* *{otp['otp']}*\n"
                    f"🛠 *Service:* {otp.get('service','')}\n"
                    f"⏰ *Time:* {otp.get('received_at','')}\n\n"
                    "Powered by *ArslanMD Official* 🇵🇰"
                )

                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(CHANNEL_BUTTON_TEXT, url=CHANNEL_BUTTON_URL)]
                ])

                await app.bot.send_message(
                    chat_id=TARGET_CHAT,
                    text=msg,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )

        except Exception as e:
            print("BOT ERROR:", e)

        await asyncio.sleep(POLL_INTERVAL)

async def clean_key(key):
    await asyncio.sleep(30 * 60)
    seen.discard(key)

# ================= POST INIT =================
async def post_init(app):
    asyncio.create_task(otp_loop(app))

# ================= MAIN =================
def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    print("🤖 Auto OTP Receiver Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
