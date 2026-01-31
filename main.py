import requests
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7787473053:AAFCg166nfOqQY6dJUJfQ3ct5Rfc66dxkrI"
CUSTOM_OTP_LINK = "https://t.me/e3hacker_chat"
API_URL = "https://arslan-apis.vercel.app/more/activenumbers"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Get Number", callback_data="get_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_number":
        try:
            response = requests.get(API_URL)
            data = response.json()
            numbers = data.get("result", [])
            if numbers:
                number = random.choice(numbers)  # random number from the list
            else:
                number = "No numbers available"
        except Exception as e:
            number = "Error fetching number"

        keyboard = [
            [
                InlineKeyboardButton("Refresh Number", callback_data="get_number"),
                InlineKeyboardButton("OTP", url=CUSTOM_OTP_LINK)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📱 Number: {number}", reply_markup=reply_markup)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
