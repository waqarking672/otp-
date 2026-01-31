import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== SET YOUR BOT TOKEN HERE ======
BOT_TOKEN = "7787473053:AAFCg166nfOqQY6dJUJfQ3ct5Rfc66dxkrI"
# =====================================

# Custom OTP link (جو آپ چاہتے ہیں یہاں لگائیں)
CUSTOM_OTP_LINK = "https://yourcustomlink.com/otp"

# API URL
API_URL = "https://arslan-apis.vercel.app/more/activenumbers"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Get Number", callback_data="get_number")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Callback handler for buttons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "get_number":
        # Fetch number from API
        try:
            response = requests.get(API_URL)
            data = response.json()
            number = data.get("number", "No number found")
        except Exception as e:
            number = "Error fetching number"

        # Buttons under number
        keyboard = [
            [
                InlineKeyboardButton("Refresh Number", callback_data="get_number"),
                InlineKeyboardButton("OTP", url=CUSTOM_OTP_LINK)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📱 Number: {number}", reply_markup=reply_markup)

# Main function to run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
