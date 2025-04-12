import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ChatMemberHandler
)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get token from environment (for Railway deployment)
TOKEN = os.getenv("TOKEN")  # Or directly paste token for local: TOKEN = "YOUR_TOKEN"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

# Button press handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

# Handle new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    messages = []
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
        mention = f"<a href='tg://user?id={member.id}'>{member.full_name}</a>"
        messages.append(f"👋 Welcome {mention} to the group! 🎉")

    if messages:
        await update.message.reply_html('\n'.join(messages))

# Handle left/removed members
async def member_status_change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    old_status = update.chat_member.old_chat_member.status
    new_status = update.chat_member.new_chat_member.status
    user = update.chat_member.old_chat_member.user

    if user.id == context.bot.id:
        return  # Ignore bot updates

    # Detect left or kicked
    if old_status in ['member', 'restricted'] and new_status in ['left', 'kicked']:
        mention = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"👋 {mention} has left or was removed from the group.",
            parse_mode="HTML"
        )

# Main
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(ChatMemberHandler(member_status_change, ChatMemberHandler.CHAT_MEMBER))

    application.run_polling()

if __name__ == "__main__":
    main()
