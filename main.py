import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token
TOKEN = "7500136567:AAFJpb-WfsyYMkC2gvYZ1NKKtF0sAFLZACU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        f"🔥 Please join our group for more updates! 🔥\n"
        f"👉 @ccidtalk\n\n"
        f"Use the buttons below to navigate:"
    )
    
    # Create keyboard with 4 buttons
    keyboard = [
        [
            InlineKeyboardButton("📱 Website", url="https://example.com"),
            InlineKeyboardButton("🛒 Shop", url="https://example.com/shop")
        ],
        [
            InlineKeyboardButton("📞 Contact", url="https://example.com/contact"),
            InlineKeyboardButton("ℹ️ About Us", url="https://example.com/about")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select an option:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()