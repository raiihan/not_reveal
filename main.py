from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    MessageHandler,
    filters
)

import logging
import os
from telegram import Update

app = FastAPI()

# Initialize Telegram Application (Corrected)
telegram_app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()  # Initialize Application

# Set up logging
logger = logging.getLogger(__name__)

# Replace this with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Set up the Telegram application with your token
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Admin check function
def is_admin(user_id):
    return user_id == OWNER_ID

# Function to handle file uploads
# Define the handler to process file uploads
async def handle_file_upload(update: Update, context):
    try:
        file = update.message.document or update.message.photo  # You can extend this to other file types
        if file:
            file_id = file.file_id
            # You can download or process the file as needed here
            logger.info(f"File received with ID: {file_id}")
            await update.message.reply_text("✅ File received!")
        else:
            logger.info("No file found in the message.")
    except Exception as e:
        logger.error(f"❌ Error handling file upload: {e}")

# Add the file upload handler to the application
telegram_app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, handle_file_upload))


@app.on_event("startup")
async def startup():
    logger.info("✅ Telegram bot initialized")
    # Ensure that the bot is correctly initialized before processing updates
    telegram_app.initialize()  # Initialize the bot application properly

# Webhook endpoint for Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()  # Get incoming data from Telegram
        update = Update.de_json(data, telegram_app.bot)  # Convert to Update object
        
        # Process the update with the properly initialized application
        await telegram_app.process_update(update)  # This will now also process file uploads
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
