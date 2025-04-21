import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

# ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Create FastAPI app
app = FastAPI()

# Init telegram app
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Start command handler
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

telegram_app.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
    return {"ok": True}

# Startup hook for Render
@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    logger.info("✅ Telegram application initialized")
