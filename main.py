import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ChatMemberHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token
TOKEN = "7500136567:AAFJpb-WfsyYMkC2gvYZ1NKKtF0sAFLZACU"

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

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for member in update.message.new_chat_members:
        mention = f"<a href='tg://user?id={member.id}'>{member.full_name}</a>"
        await update.message.reply_html(
            f"👋 Welcome {mention} to the group! 🎉"
        )

async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    member = update.chat_member.old_chat_member.user
    if update.chat_member.old_chat_member.status in ['member', 'restricted'] and update.chat_member.new_chat_member.status == 'left':
        mention = f"<a href='tg://user?id={member.id}'>{member.full_name}</a>"
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"👋 {mention} has left the group.",
            parse_mode="HTML"
        )

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(ChatMemberHandler(goodbye, ChatMemberHandler.MY_CHAT_MEMBER))

    application.run_polling()

if __name__ == "__main__":
    main()
