import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))  # Use default 8000 if not found

# Initialize Telegram Application
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# FastAPI app
app = FastAPI()

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

# ✅ This tells Render to bind the app to a port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
