import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

# Load env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))

# FastAPI app
app = FastAPI()

# Telegram app
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# ✅ Define /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Your bot is working!")

# ✅ Add handlers BEFORE initialize
telegram_app.add_handler(CommandHandler("start", start))

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Bot starting...")
    await telegram_app.initialize()
    logger.info("✅ Telegram bot initialized")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
