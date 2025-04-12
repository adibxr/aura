import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
)

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
    
    keyboard = [
        [
            InlineKeyboardButton("🗂️ RESOURCES", url="https://tinyurl.com/resourcespackadi"),
            InlineKeyboardButton("👨🏻‍💻 CODES", url="https://adibxr.github.io/code")
        ],
        [
            InlineKeyboardButton("🎬 UI/UX", url="https://uiverse.io"),
            InlineKeyboardButton("🌐 WEBSITE", url="https://adi.immortaladi.live")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select an option:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

async def welcome_or_left(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome/goodbye messages on member changes."""
    result = update.chat_member
    old_status = result.old_chat_member.status
    new_status = result.new_chat_member.status
    user = result.new_chat_member.user

    mention = f"[{user.first_name}](tg://user?id={user.id})"

    # New user joined
    if old_status in ['left', 'kicked'] and new_status == 'member':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 Welcome {mention} to the group!",
            parse_mode="Markdown"
        )
    # User left or was removed
    elif new_status in ['left', 'kicked']:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 {mention} has left the group. Goodbye!",
            parse_mode="Markdown"
        )

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(ChatMemberHandler(welcome_or_left, ChatMemberHandler.CHAT_MEMBER))

    application.run_polling()

if __name__ == "__main__":
    main()
