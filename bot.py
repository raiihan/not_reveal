from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        buttons = [
            [InlineKeyboardButton("👤 Add Admin", callback_data="add_admin"),
             InlineKeyboardButton("❌ Remove Admin", callback_data="remove_admin")],
            [InlineKeyboardButton("📜 Admin List", callback_data="list_admins")],
            [InlineKeyboardButton("📂 Batch Upload", callback_data="batch_upload")],
            [InlineKeyboardButton("📈 Bot Stats", callback_data="bot_stats")],
            [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")],
        ]
    else:
        buttons = []
    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    await update.message.reply_text("👋 Welcome to NotRevealBot!", reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        webhook_url=os.getenv("WEBHOOK_URL")
    )