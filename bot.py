import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Telegram app
application = Application.builder().token(BOT_TOKEN).build()

# Start handler
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

# Add handler
application.add_handler(CommandHandler("start", start))

# FastAPI for Render + Webhook
app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.error("❌ Webhook error: %s", e)
        return {"ok": False, "error": str(e)}

# Only for local dev, not needed on Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
