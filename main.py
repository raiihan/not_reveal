from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    MessageHandler,
    filters,
CommandHandler
)

import logging
import os
import math
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


async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Hello! I'm ready to receive your files.")

# Helper to format bytes to human-readable size
def human_readable_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    return f"{round(size_bytes / p, 2)} {size_name[i]}"



# Function to handle file uploads
# Define the handler to process file uploads
async def handle_file_upload(update: Update, context: CallbackContext):
    try:
        message = update.message
        bot = context.bot

        file = message.document or message.video or (message.photo[-1] if message.photo else None)

        # Default values
        file_name = "Unknown"
        file_size = "Unknown"
        file_type = "Unknown"

        # Detect file type and extract info
        if message.document:
            file_name = message.document.file_name
            file_size = human_readable_size(message.document.file_size)
            file_type = "Document"
        elif message.video:
            file_name = message.video.file_name or "Unnamed Video"
            file_size = human_readable_size(message.video.file_size)
            file_type = "Video"
        elif message.photo:
            file_name = "Photo.jpg"
            file_size = human_readable_size(message.photo[-1].file_size)
            file_type = "Photo"

        # ✅ Forward the file to private channel
        sent = await bot.forward_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )

        # ✅ Create deep link using forwarded message ID
        deep_link = f"https://t.me/{bot.username}?start={sent.message_id}"

        # ✅ Send formatted response to user
        response_text = f"""✅ File Uploaded!

📁 Name: `{file_name}`
📦 Size: `{file_size}`
📂 Type: `{file_type}`

🔗 Access anytime:
{deep_link}
"""

        await message.reply_text(response_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Error handling file: {e}")
        await update.message.reply_text("❌ Something went wrong while processing the file.")


# Add the file upload handler to the application
telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, handle_file_upload))


@app.on_event("startup")
async def startup():
    logger.info("✅ Telegram bot initialized")
    await telegram_app.initialize()  # Properly await initialization

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
